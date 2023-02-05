import * as functions from 'firebase-functions';
import { checkUserAuthAndDoc } from './helpers';
import { admin, db } from './initialize';
import { getTimestamp } from './utils';

interface transferData {
	amount: string;
	recipientRollNumber: string;
	pin: string;
}

export const transfer = functions
	.region('asia-south1')
	.https.onCall(async (data: transferData, context) => {
		/*
    This function transfers the amount from the caller's id
    to the recipient's roll number in the argument

    param: data = {
      amount: string;
      recipientRollNumber: string;
    }
   */

		const { uid, userSnapshot } = await checkUserAuthAndDoc(context);
		const sendersUid = uid;
		const senderSnapshot = userSnapshot;

		const amount = parseInt(data.amount);
		const recipientRollNumber = data.recipientRollNumber;

		if (amount < 1) {
			throw new functions.https.HttpsError(
				'invalid-argument',
				'Amount must be greater than 0'
			);
		}
		if (data.pin.length !== 4) {
			throw new functions.https.HttpsError(
				'invalid-argument',
				'Pin must be 4-digits long'
			);
		}
		if (userSnapshot.data()!.pin !== data.pin) {
			throw new functions.https.HttpsError(
				'invalid-argument',
				'Incorrect pin! User pin does not match'
			);
		}

		if (recipientRollNumber.length !== 8) {
			throw new functions.https.HttpsError(
				'invalid-argument',
				'Sender roll number must be 8 digits long'
			);
		}
		if (/^[0-9]+$/.test(recipientRollNumber) === false) {
			throw new functions.https.HttpsError(
				'invalid-argument',
				'Sender roll number must contain digits only'
			);
		}

		// Check if the sender has the sufficient balance
		if (senderSnapshot.data()!.balance < amount) {
			throw new functions.https.HttpsError(
				'failed-precondition',
				'Sender does not have sufficient balance'
			);
		}

		// Self transfer is invalid
		if (senderSnapshot.data()!.rollNumber === recipientRollNumber) {
			throw new functions.https.HttpsError(
				'failed-precondition',
				'You cannot send money to yourself'
			);
		}

		// Get the recipient details from Firestore
		const recipientsQueryRef = db
			.collection('users')
			.where('rollNumber', '==', recipientRollNumber);
		const recipientSnapshot = await recipientsQueryRef.get();
		if (recipientSnapshot.empty) {
			throw new functions.https.HttpsError(
				'not-found',
				'Recipient does not exist in Firestore'
			);
		}
		if (recipientSnapshot.docs.length > 1) {
			throw new functions.https.HttpsError(
				'internal',
				'Multiple recipients with the same roll number exists in Firestore'
			);
		}
		const recipientDoc = recipientSnapshot.docs[0].data();
		const recipientUid = recipientSnapshot.docs[0].id;

		/*
			Handle transaction success!
		*/

		// Add the transaction to the transactions collection
		const transactionsRef = db.collection('transactions').doc();
		const transaction = {
			id: transactionsRef.id,
			timestamp: getTimestamp(),
			senderId: sendersUid,
			senderName: senderSnapshot.data()!.fullName,
			recipientId: recipientUid,
			recipientName: recipientDoc.fullName,
			amount: amount,
			status: 'successful',
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
		const sendersDocRef = db.collection('users').doc(sendersUid);
		await sendersDocRef.update({
			transactions:
				admin.firestore.FieldValue.arrayUnion(userTransaction),
			balance: admin.firestore.FieldValue.increment(-1 * amount),
		});

		// Add the transaction to the recipient's transaction history
		// Increment the balance by the amount for the recipient
		const recipientsDocRef = db.collection('users').doc(recipientUid);
		await recipientsDocRef.update({
			transactions:
				admin.firestore.FieldValue.arrayUnion(userTransaction),
			balance: admin.firestore.FieldValue.increment(amount),
		});

		return {
			status: 'success',
			message: 'Transfer was successful',
		};
	});
