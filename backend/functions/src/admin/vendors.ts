import { auth } from 'firebase-admin';
import * as functions from 'firebase-functions';
import { db } from '../initialize';
import { UserDoc } from '../types';

const ADMIN_UIDS: Array<string> = [
	'xe2YEIpAr6XUbAu1SNfUY55Eutf1', // Suleman
	'2PfhS8wU3EMnu0fVNTa2piqQIla2', // Tayyab
	'CZi8ek4SxMORpuY92Rs2O0iRqmu2', // Shamsi
];

const adminCheck = (context: functions.https.CallableContext) => {
	// Check is user is authenticated
	if (!context.auth) {
		throw new functions.https.HttpsError(
			'unauthenticated',
			'User is not authenticated'
		);
	}

	// Get the user's uid
	const uid: string = context.auth.uid;

	if (!ADMIN_UIDS.includes(uid)) {
		throw new functions.https.HttpsError(
			'unauthenticated',
			'Only authorized admins can call this request'
		);
	}
};

export const getAllVendors = functions
	.region('asia-south1')
	.https.onCall(async (_, context) => {
		adminCheck(context);

		/* Success */

		const ref = db.collection('users').where('role', '==', 'vendor');
		const querySnapshot = await ref.get();

		const vendors: Array<UserDoc> = [];

		querySnapshot.forEach(doc => {
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
		adminCheck(context);

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
			verified: false,
			role: 'vendor',
			balance: 0,
			transactions: [],
		};

		const ref = db.collection('users').doc(docId);
		await ref.create(userData);
	});
