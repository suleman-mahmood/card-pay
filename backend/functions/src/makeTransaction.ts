import * as functions from "firebase-functions";
import {checkUserAuthAndDoc} from "./helpers";
import {admin, db} from "./initialize";
import {getTimestamp} from "./utils";

interface makeTransactionData {
  amount: string;
  senderRollNumber: string;
  pin: string;
}

export const makeTransaction = functions.https.onCall(async (
    data: makeTransactionData,
    context
) => {
  /*
    This function makes a new transaction which deducts the amount
    from the sender's id passed in the argument and adds the amount to the
    vendor calling this function.

    param: data = {
      amount: string;
      senderRollNumber: string;
    }
   */

  const {uid, userSnapshot} = await checkUserAuthAndDoc(context);
  const vendorUid = uid;
  const vendorSnapshot = userSnapshot;

  const amount = parseInt(data.amount);
  const senderRollNumber = data.senderRollNumber;

  if (amount < 1) {
    throw new functions.https.HttpsError(
        "invalid-argument", "Amount must be greater than 0"
    );
  }

  // TODO: add more validation for senderRollNumber
  if (senderRollNumber.length !== 8) {
    throw new functions.https.HttpsError(
        "invalid-argument", "Sender roll number must be 8 digits long"
    );
  }
  if (/^[0-9]+$/.test(senderRollNumber) === false) {
    throw new functions.https.HttpsError(
        "invalid-argument", "Sender roll number must contain digits only"
    );
  }

  // Check if the caller is a vendor
  if (vendorSnapshot.data()!.role !== "vendor") {
    throw new functions.https.HttpsError(
        "permission-denied", "Only vendors can call this function"
    );
  }

  // Get the sender details from Firestore
  const sendersQueryRef = db.collection("users")
      .where("rollNumber", "==", senderRollNumber);
  const senderSnapshot = await sendersQueryRef.get();
  if (senderSnapshot.empty) {
    throw new functions.https.HttpsError(
        "not-found", "Sender does not exist in Firestore"
    );
  }
  if (senderSnapshot.docs.length > 1) {
    throw new functions.https.HttpsError(
        "internal",
        "Multiple senders with the same roll number exists in Firestore"
    );
  }
  const senderDoc = senderSnapshot.docs[0].data();
  const senderUid = senderSnapshot.docs[0].id;

  // Check if the sender has the sufficient balance
  if (senderDoc.balance < amount) {
    throw new functions.https.HttpsError(
        "failed-precondition", "Sender does not have sufficient balance"
    );
  }

  // Check if the pin was correct
  if (senderDoc.pin !== data.pin) {
    throw new functions.https.HttpsError(
        "failed-precondition", "Sender pin is incorrect"
    );
  }

  /*
  Handle transaction success!
  */

  // Add the transaction to the transactions collection
  const transactionsRef = db.collection("transactions").doc();
  const transaction = {
    id: transactionsRef.id,
    timestamp: getTimestamp(),
    senderId: senderUid,
    senderName: senderDoc.fullName,
    recipientId: vendorUid,
    recipientName: vendorSnapshot.data()!.fullName,
    amount: amount,
    status: "successful",
  };
  await transactionsRef.create(transaction);

  const userTransaction = {
    id: transaction.id,
    timestamp: transaction.timestamp,
    senderName: transaction.senderName,
    recipientName: transaction.recipientName,
    amount: transaction.amount,
    status: transaction.status,
  };

  // Add the transaction to the sender's transaction history
  // Decrement the balance by the amount for the sender
  const sendersDocRef = db.collection("users").doc(senderUid);
  await sendersDocRef.update({
    transactions: admin.firestore.FieldValue.arrayUnion(userTransaction),
    balance: admin.firestore.FieldValue.increment(-1 * amount),
  });

  // Add the transaction to the recipient's transaction history
  // Increment the balance by the amount for the recipient
  const recipientsDocRef = db.collection("users").doc(vendorUid);
  await recipientsDocRef.update({
    transactions: admin.firestore.FieldValue.arrayUnion(userTransaction),
    balance: admin.firestore.FieldValue.increment(amount),
  });

  return {
    status: "success",
    message: "Transaction was successful",
  };
});
