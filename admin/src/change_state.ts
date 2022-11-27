import { WriteResult } from 'firebase-admin/firestore';
import { db } from './init_firebase';
import { Transaction, UserDoc } from './types';

export const reversingTransactions = async () => {
	const ref = db.collection('users');
	const q = ref.where('fullName', '==', 'The Bunker');
	const querySnapshot = await q.get();

	const deleteTrans: Array<Transaction> = [];

	for await (const v of querySnapshot.docs) {
		const data = v.data() as UserDoc;
		const BunkerId = v.id;
		let sumTill = 0;

		data.transactions.forEach(v => {
			sumTill += v.amount;

			if (sumTill <= 1335) {
				deleteTrans.push(v);
			}
		});

		interface UserTransObj {
			[senderName: string]: Array<Transaction>;
		}
		const userTrans: UserTransObj = {};

		deleteTrans.forEach(trans => {
			if (trans.senderName in userTrans) {
				userTrans[trans.senderName].push(trans);
			} else {
				userTrans[trans.senderName] = [trans];
			}
		});

		interface UserBalances {
			[senderName: string]: number;
		}
		const userBalances: UserBalances = {};
		Object.keys(userTrans).map(senderName => {
			userBalances[senderName] = 0;

			userTrans[senderName].map(v => {
				userBalances[senderName] += v.amount;
			});
		});

		for await (const senderName of Object.keys(userTrans)) {
			const ref = db.collection('users');
			const q = ref.where('fullName', '==', senderName);
			const querySnapshot = await q.get();

			for await (const u of querySnapshot.docs) {
				const id = u.id;
				const docData = u.data() as UserDoc;
				const oldTrans = docData.transactions;
				const oldBalance = docData.balance;
				const tranIdsToDelete = userTrans[senderName].map(v => v.id);

				const newTrans = oldTrans.filter(
					v => !tranIdsToDelete.includes(v.id)
				);
				const newBalance = oldBalance + userBalances[senderName];

				console.log('New Users Transactions:', newTrans.length);
				console.log('New Users Balance:', newBalance);
				let sum = 0;
				newTrans.forEach(t => {
					if (t.senderName === senderName) sum -= t.amount;
					else sum += t.amount;
				});
				console.log('Trans sum', sum);

				await db.collection('users').doc(id).update({
					balance: newBalance,
					transactions: newTrans,
				});
			}
		}
		const docSnapshot = await db.collection('users').doc(BunkerId).get();
		const docData = docSnapshot.data() as UserDoc;
		const oldTrans = docData.transactions;
		const oldBalance = docData.balance;
		const tranIdsToDelete = deleteTrans.map(d => d.id);

		const newTrans = oldTrans.filter(v => !tranIdsToDelete.includes(v.id));
		const newBalance = oldBalance - 1335;

		console.log('ID:', BunkerId);
		console.log('New Bunkers Transactions:', newTrans.length);
		console.log('New Bunkers Balance:', newBalance);
		let sum = 0;
		newTrans.forEach(t => {
			if (t.senderName === 'The Bunker') sum -= t.amount;
			else sum += t.amount;
		});
		console.log('Trans sum', sum);

		await db.collection('users').doc(BunkerId).update({
			balance: newBalance,
			transactions: newTrans,
		});

		const transactionsDeleteRef = db.collection('transactions');

		for await (const id of tranIdsToDelete) {
			await transactionsDeleteRef.doc(id).delete();
		}
	}
};

export const topUp = async () => {
	// Configuration parameters
	const rollNumber = '23110240';
	const topUpAmount = 50000;

	const ref = db.collection('users');
	const q = ref.where('rollNumber', '==', rollNumber);
	const querySnapshot = await q.get();

	if (querySnapshot.size !== 1) {
		throw new Error(
			`Multiple people with the same roll number: ${querySnapshot.size}`
		);
	}

	const doc = querySnapshot.docs[0];
	const id = doc.id;
	const docData = doc.data() as UserDoc;
	const newBalance = docData.balance + topUpAmount;

	await db.collection('users').doc(id).update({
		balance: newBalance,
	});

	console.log(
		'Deposited',
		topUpAmount,
		'into',
		docData.fullName,
		docData.rollNumber
	);
};

export const TrimSpacesInFullNameOfAllUsers = async () => {
	const querySnapshot = await db.collection('users').get();

	const promiseList: Array<Promise<WriteResult>> = [];

	querySnapshot.forEach(doc => {
		const id = doc.id;
		const data = doc.data() as UserDoc;

		if (data.fullName) {
			console.log(data.fullName.trim(), data.fullName.trim().length);
			console.log(data.fullName, data.fullName.length);
			console.log('');

			const pr = db.collection('users').doc(id).update({
				fullName: data.fullName.trim(),
			});

			promiseList.push(pr);
		}
	});
	await Promise.all(promiseList);
};

export const forceTransaction = async () => {
	const amount = 0;
	const senderRollNumber = '';
	const recipientRollNumber = '';

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

	console.log('Transaction was successfull');
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
