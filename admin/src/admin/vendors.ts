import { db } from '../init_firebase';
import { Transaction, UserDoc } from '../types';

export const getAllVendors = async (): Promise<Array<UserDoc>> => {
	const ref = db.collection('users').where('role', '==', 'vendor');
	const querySnapshot = await ref.get();

	const vendors: Array<UserDoc> = [];

	querySnapshot.forEach(doc => {
		const docData = doc.data() as UserDoc;
		vendors.push(docData);
	});

	return vendors;
};

export const makeVendorAccount = async () => {
	const docId = 'j4lFpFk51rgQcipHvss8GucqzPV2';
	const userData: UserDoc = {
		id: docId,
		fullName: 'JJ Kitchen',
		personalEmail: '',
		email: 'fkabli@gmail.com',
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
};
