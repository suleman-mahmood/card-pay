import { auth } from 'firebase-admin';
import * as functions from 'firebase-functions';
import { db } from '../initialize';
import { transactionMain } from '../makeTransaction';
import { UserDoc } from '../types';
import { throwError } from '../utils';
import {
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
	vendorUid: string;
}

export const reconcileVendor = functions
	.region('asia-south1')
	.https.onCall(async (data: reconcileVendorData, context) => {
		functions.logger.info('Args:', data);

		adminCheck(context);
		uidValidated(data.vendorUid);

		const recipientRollNumber = CARDPAY_ROLLNUMBER;

		// Get the recipient details from Firestore
		const recipientsQueryRef = db
			.collection('users')
			.where('rollNumber', '==', recipientRollNumber);
		const recipientSnapshot = await recipientsQueryRef.get();
		const recipientUid = recipientSnapshot.docs[0].id;

		// Check if only one roll number exists for the recipient
		if (recipientSnapshot.size !== 1) {
			throwError(
				'invalid-argument',
				'Multiple or no documents exists for recipient'
			);
		}

		// Get the sender details from Firestore
		const sendersQueryRef = db.collection('users').doc(data.vendorUid);
		const senderSnapshot = await sendersQueryRef.get();
		const senderDoc = senderSnapshot.data() as UserDoc;
		const senderUid = data.vendorUid;

		if (!senderSnapshot.exists) {
			throwError('not-found', 'Cannot find vendor document');
		}

		// Check if the sender is a vendor
		if (senderDoc.role !== 'vendor') {
			throwError('permission-denied', 'Can only reconcile from vendors');
		}

		/*
			Handle transaction success!
		*/

		transactionMain(senderUid, recipientUid, senderDoc.balance.toString());
	});
