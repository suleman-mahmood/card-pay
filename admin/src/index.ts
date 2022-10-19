import { initializeApp, applicationDefault } from 'firebase-admin/app';
import { getAuth } from 'firebase-admin/auth';
import { getFirestore, WriteResult } from 'firebase-admin/firestore';
import { getFunctions } from 'firebase-admin/functions';

import fs from 'fs';
import path from 'path';

const app = initializeApp({
	credential: applicationDefault(),
});

// Initialize Auth
const auth = getAuth(app);

// Initialize Firestore
const db = getFirestore(app);

// Initialize functions with emulator
const functions = getFunctions(app);

interface Transaction {
	amount: number;
	id: string;
	timestamp: string;
	senderName: string;
	recipientName: string;
	status: string;
}

type UserRole = 'student' | 'vendor' | 'admin';

interface UserDoc {
	id: string;
	fullName: string;
	personalEmail: string;
	email: string;
	pendingDeposits: boolean;
	pin: string;
	phoneNumber: string;
	rollNumber: string;
	verified: boolean;
	role: UserRole;
	balance: number;
	transactions: Array<Transaction>;
}

const reversingTransactions = async () => {
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

const saveFirestoreState = async () => {
	interface DbInterface {
		[id: string]: {
			[id: string]: Object;
		};
	}
	const database: DbInterface = {};

	const ref = await db.listCollections();

	for await (const col of ref) {
		const docs = await col.get();

		const collectionName = col.path;
		database[collectionName] = {};

		docs.forEach(d => {
			database[collectionName][d.id] = d.data();
		});
	}

	const now = new Date().toISOString().replace(/T/, ' ').replace(/\..+/, '');
	const fileName = `${now}_DBState.json`;
	writeToLocalStorage(database, fileName);
};

const deleteFirestore = async () => {
	interface DbInterface {
		[id: string]: Array<string>;
	}
	const database: DbInterface = {};

	const ref = await db.listCollections();

	for await (const col of ref) {
		const docs = await col.get();

		const collectionName = col.path;
		database[collectionName] = [];

		docs.forEach(d => {
			database[collectionName].push(d.id);
		});
	}

	Object.keys(database).map(async colName => {
		const ref = db.collection(colName);

		for await (const id of database[colName]) {
			await ref.doc(id).delete();
		}
	});
};

const writeToLocalStorage = (data: Object, fileName: string) => {
	fs.writeFile(fileName, JSON.stringify(data), err => {
		if (err) return console.log(err);
		console.log('Data written to file system');
	});
};

const restoreDbFromFile = async () => {
	const filePath = path.join(
		'/home/soul/Projects/card-pay/temp/',
		'2022-10-08 01:00:05_DBState.json'
	);
	fs.readFile(filePath, { encoding: 'utf-8' }, async (err, data) => {
		if (err) console.log(err);
		else {
			const dbData = JSON.parse(data);

			for await (const collectionName of Object.keys(dbData)) {
				const colRef = db.collection(collectionName);

				for await (const docId of Object.keys(dbData[collectionName])) {
					await colRef
						.doc(docId)
						.create(dbData[collectionName][docId]);
				}
			}
		}
	});
};

const topUp = async () => {
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

const getUserDoc = async () => {
	// Configuration parameters
	const rollNumber = '23110240';

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

const TrimSpacesInFullNameOfAllUsers = async () => {
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

const getBalanceTillTime = async () => {
	// Configuration parameters
	const rollNumber = '';
	const isoDate = new Date('2022-10-10T22:30:00.000Z'); // Enter time in PKT
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

const createGenesisTransactions = async () => {};

const makeVendorAccount = async () => {
	const docId = '';
	const userData: UserDoc = {
		id: docId,
		fullName: '',
		personalEmail: '',
		email: '',
		pendingDeposits: false,
		pin: '',
		phoneNumber: '',
		rollNumber: '',
		verified: false,
		role: 'vendor',
		balance: 0,
		transactions: [],
	} 

	const ref = db.collection('users').doc(docId);
	await ref.create(userData);
};

const getTransactionsSum =async () => {
	const ref = db.collection('users');
	const querySnapshot = await ref.get();
	let totalSum = 0

	querySnapshot.forEach(async doc => {
		const docData = doc.data() as UserDoc;
		let sum = 0;

		docData.transactions.map(t => {
			if (t.senderName !== t.recipientName) {
				if(t.senderName === docData.fullName) {
					sum -= t.amount;
				}
				else {
					sum += t.amount;
				}	
			}
		});

		if(sum !== 0) {
			console.log(docData.fullName, docData.email, sum);
		}
		totalSum += sum;
	});

	console.log("Total Sum:", totalSum);
}

const forceTransaction =async () => {
	const amount = 0;
	const senderRollNumber = '';
	const recipientRollNumber = '';
  
	// Get the recipient details from Firestore
	const recipientsQueryRef = db.collection("users")
		.where("rollNumber", "==", recipientRollNumber);
	const recipientSnapshot = await recipientsQueryRef.get();
	const recipientDoc = recipientSnapshot.docs[0].data();
	const recipientUid = recipientSnapshot.docs[0].id;

	// Get the sender details from Firestore
	const sendersQueryRef = db.collection("users")
		.where("rollNumber", "==", senderRollNumber);
	const senderSnapshot = await sendersQueryRef.get();
	const senderDoc = senderSnapshot.docs[0].data();
	const senderUid = senderSnapshot.docs[0].id;
  
	/*
	Handle transaction success!
	*/
  
	// Add the transaction to the transactions collection
	const transactionsRef = db.collection("transactions").doc();
	const transaction = {
	  id: transactionsRef.id,
	  timestamp: new Date().toISOString(),
	  senderId: senderUid,
	  senderName: senderDoc.fullName,
	  recipientId: recipientUid,
	  recipientName: recipientDoc.fullName,
	  amount: amount,
	  status: "successful",
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
	const sendersDocRef = db.collection("users").doc(senderUid);
	const newSenderTrans = senderDoc.transactions;
	newSenderTrans.push(userTransaction); 
	await sendersDocRef.update({
	  transactions:  newSenderTrans, // admin.firestore.FieldValue.arrayUnion(userTransaction),
	  balance: senderDoc.balance - amount // admin.firestore.FieldValue.increment(-1 * amount),
	});
  
	// Add the transaction to the recipient's transaction history
	// Increment the balance by the amount for the recipient
	const recipientsDocRef = db.collection("users").doc(recipientUid);
	const newRecipientTrans = recipientDoc.transactions;
	newRecipientTrans.push(userTransaction); 
	await recipientsDocRef.update({
	  transactions: newRecipientTrans, // admin.firestore.FieldValue.arrayUnion(userTransaction),
	  balance: recipientDoc.balance + amount // admin.firestore.FieldValue.increment(amount),
	});

	console.log("Transaction was successfull");
}

const getAllBalances =async () => {
	const ref = db.collection('users');
	const querySnapshot = await ref.get();

	querySnapshot.forEach(async doc => {
		const docData = doc.data() as UserDoc;
		
		if(docData.balance !== 0) {			
			console.log(docData.fullName, docData.rollNumber, docData.balance);
		}		
	});
}

/*
	DB Backup and restore
*/
// restoreDbFromFile();
// deleteFirestore();
// saveFirestoreState();

// reversingTransactions();
// topUp(); // Deprecated
// TrimSpacesInFullNameOfAllUsers();
// makeVendorAccount();
// forceTransaction();

// getBalanceTillTime();
// getUserDoc();
// getTransactionsSum();
// getAllBalances();