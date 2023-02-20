import * as functions from 'firebase-functions';
import { checkUserAuthAndDoc } from './helpers';
import { admin, db } from './initialize';
import { getTimestamp, throwError } from './utils';
import {
	amountValidated,
	fourDigitPinValidated,
	rollNumberValidated,
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

		const amount = parseInt(data.amount);
		const senderRollNumber = data.senderRollNumber;

		const { uid, userSnapshot } = await checkUserAuthAndDoc(context);
		const vendorUid = uid;
		const vendorSnapshot = userSnapshot;
    const vendorDoc = vendorSnapshot.data()!;

		// Check if the caller is a vendor
		if (vendorDoc.role !== 'vendor') {
			throwError(
				'permission-denied',
				'Only vendors can call this function'
			);
		}

		// Get the sender details from Firestore
		const sendersQueryRef = db
			.collection('users')
			.where('rollNumber', '==', senderRollNumber);
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
		const senderDoc = senderSnapshot.docs[0].data();
		const senderUid = senderSnapshot.docs[0].id;

		// Check if the sender has the sufficient balance
		if (senderDoc.balance < amount) {
			throwError(
				'failed-precondition',
				'Sender does not have sufficient balance'
			);
		}

		// Check if the pin was correct
		if (senderDoc.pin !== data.pin) {
			throwError('failed-precondition', 'Sender pin is incorrect');
		}

		/*
			Handle transaction success!
		*/

		const sendersDocRef = db.collection('users').doc(senderUid);
		const recipientsDocRef = db.collection('users').doc(vendorUid);

		// Remove extra transactions if it exceeds the size of document
		if (senderDoc.transactions.length >= MAX_TRANSACTIONS_IN_ONE_DOC) {
			await sendersDocRef.update({
				transactions: senderDoc.transactions.slice(
					MAX_TRANSACTIONS_IN_ONE_DOC / 2
				),
			});
		}

		// Remove extra transactions if it exceeds the size of document
		if (vendorDoc.transactions.length >= MAX_TRANSACTIONS_IN_ONE_DOC) {
			await recipientsDocRef.update({
				transactions: vendorDoc.transactions.slice(
					MAX_TRANSACTIONS_IN_ONE_DOC / 2
				),
			});
		}

		// Add the transaction to the transactions collection
		const transactionsRef = db.collection('transactions').doc();
		const transaction = {
			id: transactionsRef.id,
			timestamp: getTimestamp(),
			senderId: senderUid,
			senderName: senderDoc.fullName,
			recipientId: vendorUid,
			recipientName: vendorSnapshot.data()!.fullName,
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
		await sendersDocRef.update({
			transactions:
				admin.firestore.FieldValue.arrayUnion(userTransaction),
			balance: admin.firestore.FieldValue.increment(-1 * amount),
		});

		// Add the transaction to the recipient's transaction history
		// Increment the balance by the amount for the recipient
		await recipientsDocRef.update({
			transactions:
				admin.firestore.FieldValue.arrayUnion(userTransaction),
			balance: admin.firestore.FieldValue.increment(amount),
		});

		return {
			status: 'success',
			message: 'Transaction was successful',
		};
	});
