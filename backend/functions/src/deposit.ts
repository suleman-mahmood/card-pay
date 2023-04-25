import axios from 'axios';
import * as functions from 'firebase-functions';
import { checkUserAuthAndDoc } from './helpers';
import { admin, db } from './initialize';
import { getTimestamp, oneHourInMs, throwError } from './utils';
import { amountAbove500, amountValidated } from './validations';

type Status = 'pending' | 'successful' | 'cancelled';
const pendingStatus: Status = 'pending';
const successfulStatus: Status = 'successful';

// export const PAYPRO_BASE_URL = 'https://api.PayPro.com.pk';
// export const USERNAME = 'Card_Pay';
// const CLIENT_ID = 'T5u0mKpCH4cV98J';
// const CLIENT_SECRET = 'vHIXolKNjB4zNIa';

export const PAYPRO_BASE_URL = 'https://api.PayPro.com.pk';
export const USERNAME = 'Card_Tech';
const CLIENT_ID = 'nZe98DIdpegfEpR';
const CLIENT_SECRET = 'OI5venNO0VdClBD';

interface depositRequestData {
	amount: string;
}

export const addDepositRequest = functions
	.region('asia-south1')
	.https.onCall(async (data: depositRequestData, context) => {
		/*
			This function calls the PayPro API to create an order for the
			amount provided for the invocation user
		*/

		functions.logger.info('Args:', data);
		const { uid, usersRef, userSnapshot } = await checkUserAuthAndDoc(
			context
		);

		return addDepositRequestHelper(data, uid, usersRef, userSnapshot);
	});

const addDepositRequestHelper = async (
	data: depositRequestData,
	uid: string,
	usersRef: FirebaseFirestore.DocumentReference<FirebaseFirestore.DocumentData>,
	userSnapshot: FirebaseFirestore.DocumentSnapshot<FirebaseFirestore.DocumentData>
) => {
	amountValidated(data.amount);
	amountAbove500(data.amount);

	const timestamp = getTimestamp();
	const amount = parseInt(data.amount);

	const transactionsRef = db.collection('transactions').doc();
	const transactionId = transactionsRef.id;

	/*
		Handle transaction gateway to PayPro API
	*/
	const authToken = await getPayProAuthToken();

	const dateHourLater = new Date(timestamp);
	dateHourLater.setTime(dateHourLater.getTime() + oneHourInMs);

	const orderConfig = {
		method: 'post',
		url: PAYPRO_BASE_URL + '/v2/ppro/co',
		headers: {
			token: authToken,
		},
		data: [
			{
				MerchantId: USERNAME,
			},
			{
				OrderNumber: transactionId,
				OrderAmount: amount,
				OrderDueDate: dateHourLater.toISOString(), // A due date of an hour
				OrderType: 'Service',
				IssueDate: timestamp,
				OrderExpireAfterSeconds: 60 * 60, // Expiry of an hour
				CustomerName: userSnapshot.data()!.fullName,
				CustomerMobile: userSnapshot.data()!.phoneNumber,
				CustomerEmail: userSnapshot.data()!.email,
				CustomerAddress: '',
			},
		],
	};

	// Send order request to PayPro
	let ppOrderRes: any;
	try {
		ppOrderRes = await axios(orderConfig);
	} catch (e) {
		throwError(
			'invalid-argument',
			'Couldnt create order request in PayPro. Retry again!'
		);
	}

	const responseData = ppOrderRes.data[1];
	const paymentUrl: string = responseData['Click2Pay'];

	// Save state into Firestore
	const depositRequestsRef = db
		.collection('deposit_requests')
		.doc(transactionId);

	functions.logger.info(
		'PayPro Order creation API completed: ',
		responseData
	);

	await depositRequestsRef.create({
		depositerUid: uid,
		status: pendingStatus,
		cancellationReason: '',
		payProMetadata: JSON.stringify(ppOrderRes.data),
		orderNumber: responseData['OrderNumber'],
		orderAmount: responseData['OrderAmount'],
		orderDueDate: orderConfig.data[1].OrderDueDate,
		orderType: orderConfig.data[1].OrderType,
		issueDate: orderConfig.data[1].IssueDate,
		orderExpireAfterSeconds: responseData['Order_Expire_After_Seconds'],
		customerName: orderConfig.data[1].CustomerName,
		customerMobile: orderConfig.data[1].CustomerMobile,
		customerEmail: orderConfig.data[1].CustomerEmail,
		customerAddress: orderConfig.data[1].CustomerAddress,
		description: responseData['Description'],
		createdOn: responseData['Created_on'],
		click2Pay: responseData['Click2Pay'],
		payProId: responseData['PayProId'],
	});

	await usersRef.update({
		pendingDeposits: true,
	});

	return {
		status: 'success',
		message: 'Deposit request was successfully placed',
		paymentUrl: paymentUrl,
		orderNumber: responseData['OrderNumber'],
		payProId: responseData['PayProId'],
	};
};

export const handleDepositSuccess = functions
	.region('asia-south1')
	.https.onCall(async (_, context) => {
		/*
			This function verifies the order against the provided PayPro id
			and deposits the amount if payment was made.
			Should be idempotent: Doesn't matter how many times it is called
		*/

		functions.logger.info('Args:');

		const { uid, usersRef, userSnapshot } = await checkUserAuthAndDoc(
			context
		);
		const authToken = await getPayProAuthToken();

		/*
			Get all pending deposit requests for this user
		*/
		const ppPromises: Promise<any>[] = [];

		const orderRequestsRef = db
			.collection('deposit_requests')
			.where('depositerUid', '==', uid)
			.where('status', '==', pendingStatus);
		const querySnapshot = await orderRequestsRef.get();

		if (querySnapshot.empty) {
			// There are no pending deposit requests
			// i.e all are either completed or cancelled
			await usersRef.update({
				pendingDeposits: false,
			});
			return;
		}

		querySnapshot.forEach((doc) => {
			// // Get order's due date and check if the order has expired
			// const orderDueDateIsoString = doc.data().orderDueDate;
			// const orderDueDate = new Date(orderDueDateIsoString);
			// const nowDate = new Date();

			// if (nowDate >= orderDueDate) {
			//   return;
			// }

			if (
				doc.data().isRaastaPayment !== undefined &&
				doc.data().isRaastaPayment
			) {
				// If this is a raasta payment then ignore
				return;
			}

			const config = {
				method: 'get',
				url: PAYPRO_BASE_URL + '/v2/ppro/ggos',
				headers: {
					token: authToken,
					'Content-Type': 'application/json',
				},
				data: JSON.stringify({
					Username: USERNAME,
					cpayId: doc.data().payProId,
				}),
			};
			ppPromises.push(axios(config));
		});

		const orderRequestsPromises: Promise<any>[] = [];
		const transactionsPromises: Promise<any>[] = [];
		const userTransactions: any[] = [];

		let anyPendingOrder = false;
		let totalAmount = 0;

		// Query the PayPro API and check the status of each order
		let ppResponses: any;
		try {
			ppResponses = await Promise.all(ppPromises);
		} catch (e) {
			throwError('internal', 'Couldnt verify orders from PayPro API', e);
		}
		ppResponses.forEach((res: any) => {
			const isPaid = res.data[1]['OrderStatus'] === 'PAID';
			const amount: number = res.data[1]['AmountPayable'];
			const orderNumber: string = res.data[1]['OrderNumber'];

			if (!isPaid) {
				// There is at least an order that is incomplete
				anyPendingOrder = true;
				return;
			}

			/*
				Handle transaction success!
			*/
			totalAmount += amount;

			// Add the transaction to the transactions collection
			const transactionData = {
				id: orderNumber,
				timestamp: getTimestamp(),
				senderId: 'PayPro',
				senderName: 'PayPro Payment Gateway',
				recipientId: uid,
				recipientName: userSnapshot.data()!.fullName,
				amount: amount,
				status: 'successful',
			};
			const transactionsRef = db
				.collection('transactions')
				.doc(orderNumber);
			transactionsPromises.push(transactionsRef.create(transactionData));

			// Add the transaction to the user's transaction history
			// Increment the balance by the amount for the user
			const userTransactionData = {
				id: transactionData.id,
				timestamp: transactionData.timestamp,
				senderName: transactionData.senderName,
				recipientName: transactionData.recipientName,
				amount: transactionData.amount,
				status: transactionData.status,
			};
			userTransactions.push(userTransactionData);

			// Set all deposit requests to completed
			const ref = db.collection('deposit_requests').doc(orderNumber);
			orderRequestsPromises.push(
				ref.update({
					status: successfulStatus,
				})
			);
		});

		if (totalAmount === 0) {
			return {
				status: 'success',
				message: 'There are pending deposits',
			};
		}

		await Promise.all(orderRequestsPromises);
		await Promise.all(transactionsPromises);

		await usersRef.update({
			transactions: admin.firestore.FieldValue.arrayUnion(
				...userTransactions
			),
			balance: admin.firestore.FieldValue.increment(totalAmount),
			pendingDeposits: anyPendingOrder,
		});

		return {
			status: 'success',
			message: 'Deposit(s) successful',
		};
	});

export const getPayProAuthToken = async (): Promise<string> => {
	const authConfig = {
		method: 'post',
		url: PAYPRO_BASE_URL + '/v2/ppro/auth',
		headers: {},
		data: {
			clientid: CLIENT_ID,
			clientsecret: CLIENT_SECRET,
		},
	};

	// Send auth request to PayPro
	let ppAuthRes: any;
	try {
		ppAuthRes = await axios(authConfig);
	} catch (e) {
		throwError('internal', 'Couldnt get paypro auth token', e);
	}
	const authToken = ppAuthRes.headers.token;

	functions.logger.info('PayPro authentication API completed: ', {
		token: authToken,
		metadata: ppAuthRes.data,
	});

	return authToken;
};

interface addRaastaDepositRequestData {
	amount: string;
	rollNumber: string;
}

export const addRaastaDepositRequest = functions
	.region('asia-south1')
	.https.onCall(async (data: addRaastaDepositRequestData) => {
		/*
			This function calls the PayPro API to create an order for the
			amount provided for the invocation user
		*/

		functions.logger.info('Args:', data);

		// Get the user details from Firestore
		const sendersQueryRef = db
			.collection('users')
			.where('rollNumber', '==', data.rollNumber);
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
		const uid = senderSnapshot.docs[0].id;
		const usersRef = db.collection('users').doc(uid);
		const userSnapshot = await usersRef.get();

		const response = await addDepositRequestHelper(
			{ amount: data.amount },
			uid,
			usersRef,
			userSnapshot
		);

		await db
			.collection('deposit_requests')
			.doc(response.orderNumber)
			.update({
				isRaastaPayment: true,
			});

		return response;
	});
