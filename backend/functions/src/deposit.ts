import * as functions from "firebase-functions";
import {admin, db} from "./initialize";
import { getTimestamp } from "./utils";

interface DepositData {
  amount: string;
  cardNumber: string;
  cvv: string;
  expiryDate: string;
}

export const deposit = functions.https.onCall(async (
    data: DepositData,
    context
) => {
  /*
    This function calls the PayPro API to make a payment for the
    credentials provided and deposits the requested amount to the
    user's account

    param: data = {
      amount: number;
      cardNumber: string;
      cvv: string;
      expiryDate: string;
    }
   */

  const amount = parseInt(data.amount);

  if (!context.auth) {
    throw new functions.https.HttpsError(
        "unauthenticated", "User is not authenticated"
    );
  }

  if (amount < 1) {
    throw new functions.https.HttpsError(
        "invalid-argument", "Amount must be greater than 0"
    );
  }

  const uid: string = context.auth.uid;

  // Get the user details from Firestore
  const usersRef = db.collection("users").doc(uid);
  const userSnapshot = await usersRef.get();

  if (!userSnapshot.exists) {
    throw new functions.https.HttpsError(
        "not-found", "User does not exist in Firestore"
    );
  }

  // TODO: Handle transaction gateway to PayPro API

  /*
  Handle transaction success!
  */

  // Add the transaction to the transactions collection
  const transactionsRef = db.collection("transactions").doc();
  const transaction = {
    id: transactionsRef.id,
    timestamp: getTimestamp(),
    senderId: "PayPro",
    senderName: "PayPro Payment Gateway",
    recipientId: uid,
    recipientName: userSnapshot.data()!.fullName,
    amount: amount,
    status: "successful",
  };
  await transactionsRef.create(transaction);

  // Add the transaction to the user's transaction history
  // Increment the balance by the amount for the user
  const userTransaction = {
    id: transaction.id,
    timestamp: transaction.timestamp,
    senderName: transaction.senderName,
    recipientName: transaction.recipientName,
    amount: transaction.amount,
    status: transaction.status,
  };
  await usersRef.update({
    transactions: admin.firestore.FieldValue.arrayUnion(userTransaction),
    balance: admin.firestore.FieldValue.increment(amount),
  });

  return {
    status: "success",
    message: "Deposit successful",
  };
});
