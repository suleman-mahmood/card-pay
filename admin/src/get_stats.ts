import { db } from './init_firebase';
import { Transaction, UserDoc } from './types';

export const getTransactionsSum = async () => {
	const ref = db.collection('users');
	const querySnapshot = await ref.get();
	let totalSum = 0;

	querySnapshot.forEach(async doc => {
		const docData = doc.data() as UserDoc;
		let sum = 0;

		docData.transactions.map(t => {
			if (t.senderName !== t.recipientName) {
				if (t.senderName === docData.fullName) {
					sum -= t.amount;
				} else {
					sum += t.amount;
				}
			}
		});

		if (sum !== 0) {
			console.log(docData.fullName, docData.email, sum);
		}
		totalSum += sum;
	});

	console.log('Total Sum:', totalSum);
};

export const getBalanceTillTime = async (rollNumber: string, isoDate: Date) => {
	// Configuration parameters

	// const isoDate = new Date('2022-10-10T22:30:00.000Z'); // Enter time in PKT

	// Go transactions from last five hours
	isoDate.setHours(isoDate.getHours() - 5);

	const ref = db.collection('users');
	const q = ref.where('rollNumber', '==', rollNumber);
	const querySnapshot = await q.get();

	if (querySnapshot.size !== 1) {
		throw new Error(
			`Multiple people with the same roll number: ${querySnapshot.size}`
		);
	}

	querySnapshot.forEach(async doc => {
		const docData = doc.data() as UserDoc;

		Object.keys(docData).map(k => {
			if (k === 'transactions') {
				const trans: Array<Transaction> = docData[k];

				let sum = 0;

				trans.forEach(t => {
					const nowDate = new Date(t.timestamp);

					if (nowDate >= isoDate) {
						console.log(t.timestamp, t.amount);
						sum += t.amount;
					}
				});
				console.log('Transactions then to now:', sum);
				console.log(
					'Previous balance at the given timestamp',
					docData.balance - sum
				);
			}
		});
	});
};

export const getAllBalances = async () => {
	const ref = db.collection('users');
	const querySnapshot = await ref.get();

	querySnapshot.forEach(async doc => {
		const docData = doc.data() as UserDoc;

		if (docData.balance !== 0) {
			console.log('Transactions count: ', docData.transactions.length);
			console.log(docData.fullName, docData.rollNumber, docData.balance);
			console.log('');
		}
	});
};

export const getUserDoc = async (rollNumber: string) => {
	const ref = db.collection('users');
	const q = ref.where('rollNumber', '==', rollNumber);
	const querySnapshot = await q.get();

	if (querySnapshot.size !== 1) {
		throw new Error(
			`Multiple people with the same roll number: ${querySnapshot.size}`
		);
	}

	querySnapshot.forEach(async doc => {
		const docData = doc.data();

		Object.keys(docData).map(k => {
			if (k === 'transactions') {
				console.log(k, ':', docData[k].length);
				console.log('Last transaction:');
				console.log(docData[k][docData[k].length - 1]);
			} else {
				console.log(k, ':', docData[k]);
			}
		});
	});
};
