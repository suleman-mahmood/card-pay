import axios from "axios";
import * as functions from "firebase-functions";
import {checkUserAuthAndDoc} from "./helpers";
import {admin, db} from "./initialize";
import {getTimestamp, oneHourInMs} from "./utils";

type Status = "pending" | "successful" | "cancelled";
const pendingStatus: Status = "pending";
const successfulStatus: Status = "successful";

interface depositRequestData {
  amount: string;
  fullName: string;
  email: string;
}

export const addDepositRequest = functions.https.onCall(async (
    data: depositRequestData,
    context
) => {
  /*
    This function calls the PayPro API to create an order for the
    amount provided for the invocation user
   */

  const timestamp = getTimestamp();
  const amount = parseInt(data.amount);


  // TODO: Add checks on other parameters
  if (amount < 1) {
    throw new functions.https.HttpsError(
        "invalid-argument", "Amount must be greater than 0"
    );
  }

  const {uid, usersRef} = await checkUserAuthAndDoc(context);

  const transactionsRef = db.collection("transactions").doc();
  const transactionId = transactionsRef.id;

  /*
  Handle transaction gateway to PayPro API
  */
  const authToken = await getPayProAuthToken();

  const dateHourLater = new Date(timestamp);
  dateHourLater.setTime(dateHourLater.getTime() + oneHourInMs);

  const orderConfig = {
    method: "post",
    url: "https://demoapi.paypro.com.pk/v2/ppro/co",
    headers: {
      "token": authToken,
    },
    data: [
      {
        "MerchantId": "Card_Pay",
      },
      {
        "OrderNumber": transactionId,
        "OrderAmount": amount,
        "OrderDueDate": dateHourLater.toISOString(), // A due date of an hour
        "OrderType": "Service",
        "IssueDate": timestamp,
        "OrderExpireAfterSeconds": 60*60, // Expiry of an hour
        "CustomerName": data.fullName,
        "CustomerMobile": "",
        "CustomerEmail": data.email,
        "CustomerAddress": "",
      },
    ],
  };

  // Send order request to PayPro
  const ppOrderRes = await axios(orderConfig);
  const responseData = ppOrderRes.data[1];
  const paymentUrl: string = responseData["Click2Pay"];

  // Save state into Firestore
  const depositRequestsRef = db
      .collection("deposit_requests")
      .doc(transactionId);

  await depositRequestsRef.create({
    depositerUid: uid,
    status: pendingStatus,
    cancellationReason: "",
    payProMetadata: JSON.stringify(ppOrderRes.data),
    orderNumber: responseData["OrderNumber"],
    orderAmount: responseData["OrderAmount"],
    orderDueDate: orderConfig.data[1].OrderDueDate,
    orderType: orderConfig.data[1].OrderType,
    issueDate: orderConfig.data[1].IssueDate,
    orderExpireAfterSeconds: responseData["Order_Expire_After_Seconds"],
    customerName: orderConfig.data[1].CustomerName,
    customerMobile: orderConfig.data[1].CustomerMobile,
    customerEmail: orderConfig.data[1].CustomerEmail,
    customerAddress: orderConfig.data[1].CustomerAddress,
    description: responseData["Description"],
    createdOn: responseData["Created_on"],
    click2Pay: responseData["Click2Pay"],
    payProId: responseData["PayProId"],
  });

  await usersRef.update({
    pendingDeposits: true,
  });

  return {
    status: "success",
    message: "Deposit request was successfully placed",
    paymentUrl: paymentUrl,
    orderNumber: responseData["OrderNumber"],
    payProId: responseData["PayProId"],
  };
});


export const handleDepositSuccess = functions.https.onCall(async (
    _,
    context
) => {
  /*
    This function verifies the order against the provided PayPro id
    and deposits the amount if payment was made.
    Should be idempotent: Doesn't matter how many times it is called
  */

  const {uid, usersRef, userSnapshot} = await checkUserAuthAndDoc(context);
  const authToken = await getPayProAuthToken();

  /*
  Get all pending deposit requests for this user
  */
  const ppPromises: Promise<any>[] = [];

  const orderRequestsRef = db
      .collection("deposit_requests")
      .where("depositerUid", "==", uid)
      .where("status", "==", pendingStatus);
  const querySnapshot = await orderRequestsRef.get();

  if (querySnapshot.empty) {
    // There are no pending deposit requests
    // i.e all are either completed or cancelled
    await usersRef.update({
      pendingDeposits: false,
    });
    return;
  }

  querySnapshot.forEach((doc) => {
    const config = {
      method: "get",
      url: "https://demoapi.paypro.com.pk/v2/ppro/ggos",
      headers: {
        "token": authToken,
        "Content-Type": "application/json",
      },
      data: JSON.stringify({
        "Username": "Card_Pay",
        "cpayId": doc.data().payProId,
      }),
    };
    ppPromises.push(axios(config));
  });

  const orderRequestsPromises: Promise<any>[] = [];
  const transactionsPromises: Promise<any>[] = [];
  const userTransactions: any[] = [];

  let anyPendingOrder = false;
  let totalAmount = 0;

  // Query the PayPro API and check the status of each order
  const ppResponses = await Promise.all(ppPromises);
  ppResponses.forEach((res) => {
    const isPaid = res.data[1]["OrderStatus"] === "PAID";
    const amount: number = res.data[1]["AmountPayable"];
    const orderNumber: string = res.data[1]["OrderNumber"];

    if (!isPaid) {
      // There is at least an order that is incomplete
      anyPendingOrder = true;
      return;
    }

    /*
    Handle transaction success!
    */
    totalAmount += amount;

    // Add the transaction to the transactions collection
    const transactionData = {
      id: orderNumber,
      timestamp: getTimestamp(),
      senderId: "PayPro",
      senderName: "PayPro Payment Gateway",
      recipientId: uid,
      recipientName: userSnapshot.data()!.fullName,
      amount: amount,
      status: "successful",
    };
    const transactionsRef = db.collection("transactions").doc(orderNumber);
    transactionsPromises.push(transactionsRef.create(transactionData));

    // Add the transaction to the user's transaction history
    // Increment the balance by the amount for the user
    const userTransactionData = {
      id: transactionData.id,
      timestamp: transactionData.timestamp,
      senderName: transactionData.senderName,
      recipientName: transactionData.recipientName,
      amount: transactionData.amount,
      status: transactionData.status,
    };
    userTransactions.push(userTransactionData);

    // Set all deposit requests to completed
    const ref = db.collection("deposit_requests").doc(orderNumber);
    orderRequestsPromises.push(ref.update({
      status: successfulStatus,
    }));
  });

  await Promise.all(orderRequestsPromises);
  await Promise.all(transactionsPromises);

  await usersRef.update({
    transactions: admin.firestore.FieldValue.arrayUnion(...userTransactions),
    balance: admin.firestore.FieldValue.increment(totalAmount),
    pendingDeposits: anyPendingOrder,
  });

  return {
    status: "success",
    message: "Deposit(s) successful",
  };
});

const getPayProAuthToken = async (): Promise<string> => {
  const authConfig = {
    method: "post",
    url: "https://demoapi.paypro.com.pk/v2/ppro/auth",
    headers: { },
    data: {
      "clientid": "pf5Cns3hQrJbvHh",
      "clientsecret": "t3yxHEQYGZJHY0m",
    },
  };

  // Send auth request to PayPro
  const ppAuthRes = await axios(authConfig);
  const authToken = ppAuthRes.headers.token;

  return authToken;
};
