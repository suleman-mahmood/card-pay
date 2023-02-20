import { auth } from 'firebase-admin';
import * as functions from 'firebase-functions';
import { admin, db } from '../initialize';
import { UserDoc } from '../types';
import { throwError } from '../utils';
import {
	amountValidated,
	emailValidated,
	passwordValidated,
	uidValidated,
} from '../validations';
import { adminCheck, CARDPAY_ROLLNUMBER } from './utils';

export const getAllVendors = functions
	.region('asia-south1')
	.https.onCall(async (_, context) => {
		adminCheck(context);

		/* Success */

		const ref = db.collection('users').where('role', '==', 'vendor');
		const querySnapshot = await ref.get();

		const vendors: Array<UserDoc> = [];

		querySnapshot.forEach((doc) => {
			const docData = doc.data() as UserDoc;
			vendors.push(docData);
		});

		return vendors;
	});

interface MakeVendorAccountData {
	email: string;
	password: string;
	name: string;
}

export const makeVendorAccount = functions
	.region('asia-south1')
	.https.onCall(async (data: MakeVendorAccountData, context) => {
		functions.logger.info('Args:', data);

		adminCheck(context);
		passwordValidated(data.password);
		emailValidated(data.email);

		/* Success */

		const userRecord = await auth().createUser({
			email: data.email,
			password: data.password,
			emailVerified: true,
			displayName: data.name,
		});

		const docId = userRecord.uid;
		const userData: UserDoc = {
			id: docId,
			fullName: data.name,
			personalEmail: '',
			email: data.email,
			pendingDeposits: false,
			pin: '',
			phoneNumber: '',
			rollNumber: '',
			referralRollNumber: '',
			verified: false,
			role: 'vendor',
			balance: 0,
			transactions: [],
		};

		const ref = db.collection('users').doc(docId);
		await ref.create(userData);
	});

interface reconcileVendorData {
	vendorUid: string; // vendor's uid
	amount: string; // the amount to reconcile
}

export const reconcileVendor = functions
	.region('asia-south1')
	.https.onCall(async (data: reconcileVendorData, context) => {
		functions.logger.info('Args:', data);

		adminCheck(context);
		amountValidated(data.amount);
		uidValidated(data.vendorUid);

		const amount = parseInt(data.amount);
		const recipientRollNumber = CARDPAY_ROLLNUMBER;

		// Get the recipient details from Firestore
		const recipientsQueryRef = db
			.collection('users')
			.where('rollNumber', '==', recipientRollNumber);
		const recipientSnapshot = await recipientsQueryRef.get();
		const recipientDoc = recipientSnapshot.docs[0].data();
		const recipientUid = recipientSnapshot.docs[0].id;

		// Get the sender details from Firestore
		const sendersQueryRef = db.collection('users').doc(data.vendorUid);
		const senderSnapshot = await sendersQueryRef.get();
		const senderDoc = senderSnapshot.data()!;
		const senderUid = data.vendorUid;

		if (!senderSnapshot.exists) {
			throwError('not-found', 'Cannot find vendor document');
		}

		// Check if the sender is a vendor
		if (senderDoc.role !== 'vendor') {
			throwError('permission-denied', 'Can only reconcile from vendors');
		}
		if (recipientSnapshot.size !== 1) {
			throwError(
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
			message: 'Reconcilation was successfull',
		};
	});
