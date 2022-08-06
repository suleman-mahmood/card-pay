import * as functions from "firebase-functions";
import {admin, db} from "./initialize";
import { getTimestamp } from "./utils";

interface transferData {
  amount: string;
  recipientRollNumber: string;
}

export const transfer = functions.https.onCall(async (
    data: transferData,
    context
) => {
  /*
    This function transfers the amount from the caller's id
    to the recipient's roll number in the argument

    param: data = {
      amount: string;
      recipientRollNumber: string;
    }
   */

  if (!context.auth) {
    throw new functions.https.HttpsError(
        "unauthenticated", "The user is not authenticated"
    );
  }

  const amount = parseInt(data.amount);
  const recipientRollNumber = data.recipientRollNumber;

  if (amount < 1) {
    throw new functions.https.HttpsError(
        "invalid-argument", "Amount must be greater than 0"
    );
  }

  // TODO: add more validation for recipientRollNumber
  if (recipientRollNumber.length !== 8) {
    throw new functions.https.HttpsError(
        "invalid-argument", "Sender roll number must be 8 digits long"
    );
  }
  if (/^[0-9]+$/.test(recipientRollNumber) === false) {
    throw new functions.https.HttpsError(
        "invalid-argument", "Sender roll number must contain digits only"
    );
  }

  const sendersUid: string = context.auth.uid;

  // Get the sender details from Firestore
  const sendersRef = db.collection("users").doc(sendersUid);
  const senderSnapshot = await sendersRef.get();

  if (!senderSnapshot.exists) {
    throw new functions.https.HttpsError(
        "not-found", "Sender does not exist in Firestore"
    );
  }

  // Check if the sender has the sufficient balance
  if (senderSnapshot.data()!.balance < amount) {
    throw new functions.https.HttpsError(
        "failed-precondition", "Sender does not have sufficient balance"
    );
  }

  // Get the recipient details from Firestore
  const recipientsQueryRef = db.collection("users")
      .where("rollNumber", "==", recipientRollNumber);
  const recipientSnapshot = await recipientsQueryRef.get();
  if (recipientSnapshot.empty) {
    throw new functions.https.HttpsError(
        "not-found", "Recipient does not exist in Firestore"
    );
  }
  if (recipientSnapshot.docs.length > 1) {
    throw new functions.https.HttpsError(
        "internal",
        "Multiple recipients with the same roll number exists in Firestore"
    );
  }
  const recipientDoc = recipientSnapshot.docs[0].data();
  const recipientUid = recipientSnapshot.docs[0].id;

  /*
  Handle transaction success!
  */

  // Add the transaction to the transactions collection
  const transactionsRef = db.collection("transactions").doc();
  const transaction = {
    id: transactionsRef.id,
    timestamp: getTimestamp(),
    senderId: sendersUid,
    senderName: senderSnapshot.data()!.fullName,
    recipientId: recipientUid,
    recipientName: recipientDoc.fullName,
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
  const sendersDocRef = db.collection("users").doc(sendersUid);
  await sendersDocRef.update({
    transactions: admin.firestore.FieldValue.arrayUnion(userTransaction),
    balance: admin.firestore.FieldValue.increment(-1 * amount),
  });

  // Add the transaction to the recipient's transaction history
  // Increment the balance by the amount for the recipient
  const recipientsDocRef = db.collection("users").doc(recipientUid);
  await recipientsDocRef.update({
    transactions: admin.firestore.FieldValue.arrayUnion(userTransaction),
    balance: admin.firestore.FieldValue.increment(amount),
  });

  return {
    status: "success",
    message: "Transfer was successful",
  };
});
