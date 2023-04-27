import axios from 'axios';
import * as functions from 'firebase-functions';
import { getPayProAuthToken, MAIN_USERNAME, PAYPRO_BASE_URL } from './deposit';
import { admin, db } from './initialize';
import { transactionMain } from './makeTransaction';
import { denyPickupOrderHelper } from './pre-order/order';
import { getTimestamp, throwError } from './utils';

const MILLISECONDS_IN_ONE_MIN = 60000;
const ORDER_EXPIRY = MILLISECONDS_IN_ONE_MIN * 5;
const RAASTA_UID = 'OJooBExFuDPQ4jecskrcxuD515c2';

export const houseKeeper = functions.pubsub
	.schedule('every 5 minutes')
	.onRun(async () => {
		functions.logger.info(
			'House Keeper initiated which will run every 5 minutes!'
		);

		await handlePickupOrdersExpiry();

		await handleRaastaPayments();

		return;
	});

const handleRaastaPayments = async () => {
	// Get all Raasta pending transactions
	const depostRequestsSnapshot = await db
		.collection('deposit_requests')
		.where('status', '==', 'pending')
		.where('isRaastaPayment', '==', true)
		.get();

	const ppPromises: Promise<any>[] = [];
	const authToken = await getPayProAuthToken(true);
	const orderNumberUserData: {
		[orderNumber: string]: {
			uid: string;
			fullName: string;
		};
	} = {};

	// For each pending transaction
	depostRequestsSnapshot.forEach((docSnapshot) => {
		const docData = docSnapshot.data();

		const orderNumber = docData.orderNumber;
		const depositerUid = docData.depositerUid;
		const customerName = docData.customerName;

		orderNumberUserData[orderNumber] = {
			uid: depositerUid,
			fullName: customerName,
		};

		// Check if the transaction is complete
		const config = {
			method: 'get',
			url: PAYPRO_BASE_URL + '/v2/ppro/ggos',
			headers: {
				token: authToken,
				'Content-Type': 'application/json',
			},
			data: JSON.stringify({
				Username: MAIN_USERNAME,
				cpayId: docData.payProId,
			}),
		};
		ppPromises.push(axios(config));
	});

	// Query the PayPro API and check the status of each order
	let ppResponses: any;
	try {
		ppResponses = await Promise.all(ppPromises);
	} catch (e) {
		throwError('internal', 'Couldnt verify orders from PayPro API', e);
	}

	const transactionsPromises: Promise<any>[] = [];
	const userTransactionsPromises: Promise<any>[] = [];
	const orderRequestsPromises: Promise<any>[] = [];

	const raastaTransactionsList: Array<{
		senderUid: string;
		recipientUid: string;
		amount: number;
	}> = [];

	ppResponses.forEach((res: any) => {
		const isPaid = res.data[1]['OrderStatus'] === 'PAID';
		const amount: number = res.data[1]['AmountPayable'];
		const orderNumber: string = res.data[1]['OrderNumber'];

		if (!isPaid) {
			// Return if the transaction is not paid
			return;
		}

		/*
			Handle transaction success!
		*/

		const uid = orderNumberUserData[orderNumber].uid;
		const fullName = orderNumberUserData[orderNumber].fullName;

		raastaTransactionsList.push({
			senderUid: uid,
			recipientUid: RAASTA_UID,
			amount: amount,
		});

		// Create a PayPro transaction that deposits money into users account
		// Set this transaction to confirmed

		// Add the transaction to the transactions collection
		const transactionData = {
			id: orderNumber,
			timestamp: getTimestamp(),
			senderId: 'PayPro',
			senderName: 'PayPro Payment Gateway',
			recipientId: uid,
			recipientName: fullName,
			amount: amount,
			status: 'successful',
		};
		const transactionsRef = db.collection('transactions').doc(orderNumber);
		transactionsPromises.push(transactionsRef.create(transactionData));

		// Add the transaction to the user's transaction history
		const userTransactionData = {
			id: transactionData.id,
			timestamp: transactionData.timestamp,
			senderName: transactionData.senderName,
			recipientName: transactionData.recipientName,
			amount: transactionData.amount,
			status: transactionData.status,
		};
		const usersRef = db.collection('users').doc(uid);
		userTransactionsPromises.push(
			usersRef.update({
				balance: admin.firestore.FieldValue.increment(1 * amount),
				transactions:
					admin.firestore.FieldValue.arrayUnion(userTransactionData),
			})
		);

		// Set all deposit requests to completed
		const depositReqRef = db
			.collection('deposit_requests')
			.doc(orderNumber);
		orderRequestsPromises.push(
			depositReqRef.update({
				status: 'successful',
			})
		);
	});

	try {
		await Promise.all(transactionsPromises);
	} catch (e) {
		throwError(
			'internal',
			'Couldnt add doc into transactions collection',
			e
		);
	}
	try {
		await Promise.all(userTransactionsPromises);
	} catch (e) {
		throwError(
			'internal',
			'Couldnt add doc into users transactions collection',
			e
		);
	}
	try {
		await Promise.all(orderRequestsPromises);
	} catch (e) {
		throwError(
			'internal',
			'Couldnt change status of order requests from pending to confirmed',
			e
		);
	}

	/*
		Create a Raasta transcation that transfer the amount from user to raasta
	*/
	await Promise.all(
		raastaTransactionsList.map((t) =>
			transactionMain(t.senderUid, t.recipientUid, t.amount.toString())
		)
	);

	return;
};

const handlePickupOrdersExpiry = async () => {
	const snapshot = await db.collection('new_order_requests').get();
	const ordersToDelete: Promise<void>[] = [];

	snapshot.docs.forEach((doc) => {
		const data = doc.data();
		const restaurantId = doc.id;

		if (Object.keys(data.orders).length === 0) {
			// No pending orders
			return;
		}

		Object.keys(data.orders).map((userUid) => {
			const orderDetails = data.orders[userUid];
			const timestamp = orderDetails.timestamp;
			const nowTimestamp = new Date().getTime();

			if (nowTimestamp - timestamp >= ORDER_EXPIRY) {
				// Order expired so deny this automatically
				ordersToDelete.push(
					denyPickupOrderHelper({
						cart: [],
						customerUid: userUid,
						orderId: orderDetails.orderId,
						restaurantId: restaurantId,
						reason: 'Order expired! Restaurant didnt accept within window',
					})
				);
			}
		});
	});

	await Promise.all(ordersToDelete);

	return;
};
