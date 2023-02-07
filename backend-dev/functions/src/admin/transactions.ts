import * as functions from 'firebase-functions';
import { db } from '../initialize';
import { adminCheck, CARDPAY_ROLLNUMBER } from './utils';

interface topUpUserVirtualCashData {
	rollNumber: string; // vendor's roll number
	amount: string; // the amount to reconcile
}

export const topUpUserVirtualCash = functions
	.region('asia-south1')
	.https.onCall(async (data: topUpUserVirtualCashData, context) => {
		adminCheck(context);

		return topUpUserVirtualCashHelper(data);
	});

export const topUpUserVirtualCashHelper = async (
	data: topUpUserVirtualCashData
) => {
	const amount = parseInt(data.amount);
	if (amount < 1) {
		throw new functions.https.HttpsError(
			'invalid-argument',
			'Amount must be greater than 0'
		);
	}

	const recipientRollNumber = data.rollNumber;
	const senderRollNumber = CARDPAY_ROLLNUMBER;

	// Get the recipient details from Firestore
	const recipientsQueryRef = db
		.collection('users')
		.where('rollNumber', '==', recipientRollNumber);
	const recipientSnapshot = await recipientsQueryRef.get();
	const recipientDoc = recipientSnapshot.docs[0].data();
	const recipientUid = recipientSnapshot.docs[0].id;

	// Get the sender details from Firestore
	const sendersQueryRef = db
		.collection('users')
		.where('rollNumber', '==', senderRollNumber);
	const senderSnapshot = await sendersQueryRef.get();
	const senderDoc = senderSnapshot.docs[0].data();
	const senderUid = senderSnapshot.docs[0].id;

	if (recipientRollNumber.length !== 8) {
		throw new functions.https.HttpsError(
			'invalid-argument',
			'Recipient roll number must be 8 digits long'
		);
	}
	if (/^[0-9]+$/.test(recipientRollNumber) === false) {
		throw new functions.https.HttpsError(
			'invalid-argument',
			'Recipient roll number must contain digits only'
		);
	}
	if (senderSnapshot.size !== 1) {
		throw new functions.https.HttpsError(
			'invalid-argument',
			'Multiple or no documents exists for sender'
		);
	}
	if (recipientSnapshot.size !== 1) {
		throw new functions.https.HttpsError(
			'invalid-argument',
			'Multiple or no documents exists for recipient'
		);
	}

	/*
		Handle transaction success!
		*/

	// Add the transaction to the transactions collection
	const transactionsRef = db.collection('transactions').doc();
	const transaction = {
		id: transactionsRef.id,
		timestamp: new Date().toISOString(),
		senderId: senderUid,
		senderName: senderDoc.fullName,
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
	const sendersDocRef = db.collection('users').doc(senderUid);
	const newSenderTrans = senderDoc.transactions;
	newSenderTrans.push(userTransaction);
	await sendersDocRef.update({
		transactions: newSenderTrans, // admin.firestore.FieldValue.arrayUnion(userTransaction),
		balance: senderDoc.balance - amount, // admin.firestore.FieldValue.increment(-1 * amount),
	});

	// Add the transaction to the recipient's transaction history
	// Increment the balance by the amount for the recipient
	const recipientsDocRef = db.collection('users').doc(recipientUid);
	const newRecipientTrans = recipientDoc.transactions;
	newRecipientTrans.push(userTransaction);
	await recipientsDocRef.update({
		transactions: newRecipientTrans, // admin.firestore.FieldValue.arrayUnion(userTransaction),
		balance: recipientDoc.balance + amount, // admin.firestore.FieldValue.increment(amount),
	});

	functions.logger.info('Top Up was successfull');

	return {
		status: 'success',
		message: 'Top Up was successfull',
	};
};
