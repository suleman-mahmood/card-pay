import * as functions from 'firebase-functions';
import { checkUserAuthAndDoc } from './helpers';
import { admin, db } from './initialize';
import { UserDoc } from './types';
import { getTimestamp, throwError } from './utils';
import {
	amountValidated,
	fourDigitPinValidated,
	rollNumberValidated,
	uidValidated,
} from './validations';

const MAX_TRANSACTIONS_IN_ONE_DOC = 2000;

interface makeTransactionData {
	amount: string;
	senderRollNumber: string;
	pin: string;
}

export const makeTransaction = functions
	.region('asia-south1')
	.https.onCall(async (data: makeTransactionData, context) => {
		/*
			This function makes a new transaction which deducts the amount
			from the sender's id passed in the argument and adds the amount to the
			vendor calling this function.
		*/

		functions.logger.info('Args:', data);

		fourDigitPinValidated(data.pin);
		amountValidated(data.amount);
		rollNumberValidated(data.senderRollNumber);

		const { uid, userSnapshot } = await checkUserAuthAndDoc(context);
		const vendorUid = uid;
		const vendorSnapshot = userSnapshot;
		const vendorModel = vendorSnapshot.data() as UserDoc;

		// Check if the caller is a vendor
		if (vendorModel.role !== 'vendor') {
			throwError(
				'permission-denied',
				'Only vendors can call this function'
			);
		}

		// Get the sender details from Firestore
		const sendersQueryRef = db
			.collection('users')
			.where('rollNumber', '==', data.senderRollNumber);
		const senderSnapshot = await sendersQueryRef.get();
		if (senderSnapshot.empty) {
			throwError('not-found', 'Sender does not exist in Firestore');
		}
		if (senderSnapshot.docs.length > 1) {
			throwError(
				'internal',
				'Multiple senders with the same roll number exists in Firestore'
			);
		}
		const senderModel = senderSnapshot.docs[0].data() as UserDoc;
		const senderUid = senderSnapshot.docs[0].id;

		// Check if the pin was correct
		if (senderModel.pin !== data.pin) {
			throwError('failed-precondition', 'Sender pin is incorrect');
		}

		/*
			Handle transaction success!
		*/

		return transactionMain(senderUid, vendorUid, data.amount);
	});

export const transactionMain = async (
	senderUid: string,
	recipientUid: string,
	amountStr: string
) => {
	/*
		This function makes a new transaction which deducts the amount
		from the sender's id passed in the argument and adds the amount to the
		vendor calling this function.
	*/

	amountValidated(amountStr);
	uidValidated(recipientUid);
	uidValidated(senderUid);

	const amount = parseInt(amountStr);

	return db.runTransaction(async (transaction) => {
		const senderDocRef = db.collection('users').doc(senderUid);
		const recipientDocRef = db.collection('users').doc(recipientUid);

		const senderDoc = await transaction.get(senderDocRef);
		const recipientDoc = await transaction.get(recipientDocRef);

		if (!senderDoc.exists || !recipientDoc.exists) {
			throwError(
				'failed-precondition',
				'Either recipient or sender doc doesnt exist'
			);
		}

		const senderModel = senderDoc.data() as UserDoc;
		const recipientModel = recipientDoc.data() as UserDoc;

		if (senderModel.balance < amount || senderModel.balance <= 0) {
			throwError(
				'failed-precondition',
				'Sender does not have sufficient balance'
			);
		}

		/*
			Handle transaction success!
		*/

		// Remove extra transactions if it exceeds the size of document
		if (senderModel.transactions.length >= MAX_TRANSACTIONS_IN_ONE_DOC) {
			await transaction.update(senderDocRef, {
				transactions: senderModel.transactions.slice(
					MAX_TRANSACTIONS_IN_ONE_DOC / 2
				),
			});
		}

		// Remove extra transactions if it exceeds the size of document
		if (recipientModel.transactions.length >= MAX_TRANSACTIONS_IN_ONE_DOC) {
			await transaction.update(recipientDocRef, {
				transactions: recipientModel.transactions.slice(
					MAX_TRANSACTIONS_IN_ONE_DOC / 2
				),
			});
		}

		// Add the transaction to the transactions collection
		const transactionsRef = db.collection('transactions').doc();
		const transactionData = {
			id: transactionsRef.id,
			timestamp: getTimestamp(),
			senderId: senderUid,
			senderName: senderModel.fullName,
			recipientId: recipientUid,
			recipientName: recipientModel.fullName,
			amount: amount,
			status: 'successful',
		};
		await transaction.create(transactionsRef, transactionData);

		const userTransaction = {
			id: transactionData.id,
			timestamp: transactionData.timestamp,
			senderName: transactionData.senderName,
			recipientName: transactionData.recipientName,
			amount: transactionData.amount,
			status: transactionData.status,
		};

		// Add the transaction to the sender's transaction history
		// Decrement the balance by the amount for the sender
		await transaction.update(senderDocRef, {
			transactions:
				admin.firestore.FieldValue.arrayUnion(userTransaction),
			balance: admin.firestore.FieldValue.increment(-1 * amount),
		});

		// Add the transaction to the recipient's transaction history
		// Increment the balance by the amount for the recipient
		await transaction.update(recipientDocRef, {
			transactions:
				admin.firestore.FieldValue.arrayUnion(userTransaction),
			balance: admin.firestore.FieldValue.increment(amount),
		});

		return {
			status: 'success',
			message: 'Transaction was successful',
		};
	});
};
