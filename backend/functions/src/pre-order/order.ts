import * as functions from 'firebase-functions';
import { checkUserAuthAndDoc } from '.././helpers';
import { db } from '.././initialize';
import { sendEmail, throwError } from '.././utils';
import { UserDoc } from '../types';
import { transactionMain } from '../makeTransaction';

const MAX_ORDER_AMOUNT = 5000;

export enum TRANSACTION_TYPE {
	pre_order_pickup = 'pre_order_pickup',
	pre_order_delivery = 'pre_order_delivery',
	top_up = 'top_up',
	payment_gateway = 'payment_gateway',
	p2p_transfer = 'p2p_transfer',
	pos = 'pos',
}

enum ORDER_STATUS_ENUM {
	pending = 'pending',
	confirmed = 'confirmed',
	denied = 'denied',
	expired = 'expired',
	insufficient_funds = 'insufficient_funds',
}
interface NewOrderRequests {
	orders: {
		[uid: string]: {
			order_id: string;
			cart: Array<{
				restaurant_id: string;
				name: string;
				price: number;
				quantity: number;
			}>;
			specialInstructions: string;
			isDelivery: boolean;
			customerName: string;
			customerRollNumber: string;
			contactNumber: string;
			deliveryAddress: string;
		};
	};
}

interface PreOrders {
	user_uid: string;
	order_id: string;
	cart: Array<{
		restaurant_id: string;
		name: string;
		price: number;
		quantity: number;
	}>;
	status: ORDER_STATUS_ENUM;
	restaurant_id: string;
	specialInstructions: string;
	isDelivery: boolean;
	customerName: string;
	customerRollNumber: string;
	contactNumber: string;
	deliveryAddress: string;
}

interface CreatePickupOrderData {
	cart: Array<{
		name: string;
		price: number;
		restaurant_id: string;
		quantity: number;
	}>;
	specialInstructions: string;
	isDelivery: boolean;
	customerName: string;
	customerRollNumber: string;
	contactNumber: string;
	deliveryAddress: string;
}

export const createPickupOrder = functions
	.region('asia-south1')
	.https.onCall(async (data: CreatePickupOrderData, context) => {
		/*
			This function creates an order request
		*/

		functions.logger.info('Args:', data);

		const { uid, userSnapshot } = await checkUserAuthAndDoc(context);
		const userData = userSnapshot.data() as UserDoc;

		let orderAmount = 0;
		data.cart.forEach((c) => {
			orderAmount += c.quantity * c.price;
		});

		if (orderAmount >= MAX_ORDER_AMOUNT) {
			throwError(
				'invalid-argument',
				'Order amount exceeds max order limit'
			);
		}

		if (userData.balance < orderAmount) {
			throwError('invalid-argument', 'User has insufficient balance');
		}

		if (data.cart.length === 0) {
			throwError('invalid-argument', 'No items in cart');
		}

		const restaurant_id = data.cart[0].restaurant_id;
		let different_restaurants = false;
		data.cart.forEach((c) => {
			if (c.restaurant_id !== restaurant_id) {
				different_restaurants = true;
			}
		});

		if (different_restaurants) {
			throwError(
				'invalid-argument',
				'Can only order from the same restaurant'
			);
		}

		let order_id = '';

		await db.runTransaction(async (transaction) => {
			const ref = db.collection('new_order_requests').doc(restaurant_id);
			const pre_order_ref = db.collection('pre-orders').doc();
			order_id = pre_order_ref.id;

			const doc = await transaction.get(ref);
			const docData = doc.data() as NewOrderRequests;

			if (uid in docData.orders) {
				throwError('failed-precondition', 'Order already exists');
			}

			docData.orders[uid] = {
				cart: data.cart,
				order_id: order_id,
				specialInstructions: data.specialInstructions,
				isDelivery: data.isDelivery,
				customerName: data.customerName,
				customerRollNumber: data.customerRollNumber,
				contactNumber: data.contactNumber,
				deliveryAddress: data.deliveryAddress,
			};

			transaction.update(ref, { orders: docData.orders });

			transaction.create(pre_order_ref, {
				user_uid: uid,
				order_id: order_id,
				restaurant_id: restaurant_id,
				cart: docData.orders[uid].cart,
				status: ORDER_STATUS_ENUM.pending,
				specialInstructions: data.specialInstructions,
				isDelivery: data.isDelivery,
				customerName: data.customerName,
				customerRollNumber: data.customerRollNumber,
				contactNumber: data.contactNumber,
				deliveryAddress: data.deliveryAddress,
			});
		});

		return { order_id: order_id };
	});

interface ConfirmPickupOrderData {
	cart: Array<{
		name: string;
		price: number;
		restaurant_id: string;
		quantity: number;
	}>;
	order_id: string;
	restaurant_id: string;
	customer_uid: string;
}

export const confirmPickupOrder = functions
	.region('asia-south1')
	.https.onCall(async (data: ConfirmPickupOrderData, context) => {
		/*
			This function confirms an order
		*/

		functions.logger.info('Args:', data);

		const { userSnapshot } = await checkUserAuthAndDoc(context);
		if (userSnapshot.data()!.role !== 'vendor') {
			throwError(
				'permission-denied',
				'Only vendors can call this function'
			);
		}

		let docDataPreOrder: PreOrders = {
			cart: [],
			customerName: '',
			customerRollNumber: '',
			isDelivery: false,
			order_id: '',
			restaurant_id: '',
			specialInstructions: '',
			status: ORDER_STATUS_ENUM.pending,
			user_uid: '',
			contactNumber: '',
			deliveryAddress: '',
		};

		await db.runTransaction(async (transaction) => {
			const new_order_requests_ref = db
				.collection('new_order_requests')
				.doc(data.restaurant_id);
			const pre_order_ref = db
				.collection('pre-orders')
				.doc(data.order_id);

			const docPreOrder = await transaction.get(pre_order_ref);
			docDataPreOrder = docPreOrder.data() as PreOrders;

			const docNewOrderRequest = await transaction.get(
				new_order_requests_ref
			);
			const docDataNewOrderRequest =
				docNewOrderRequest.data() as NewOrderRequests;

			if (docDataPreOrder.status !== ORDER_STATUS_ENUM.pending) {
				throwError(
					'failed-precondition',
					'Order is not in pending state'
				);
			}

			if (!(data.customer_uid in docDataNewOrderRequest.orders)) {
				throwError('failed-precondition', 'Order doesnt exist');
			}

			// Remove this from the order map
			delete docDataNewOrderRequest.orders[data.customer_uid];

			transaction.update(new_order_requests_ref, {
				orders: docDataNewOrderRequest.orders,
			});

			transaction.update(pre_order_ref, {
				status: ORDER_STATUS_ENUM.confirmed,
			});
		});

		let orderAmount = 0;
		data.cart.forEach((c) => {
			orderAmount += c.quantity * c.price;
		});

		try {
			await transactionMain(
				data.customer_uid,
				data.restaurant_id,
				orderAmount.toString(),
				docDataPreOrder.isDelivery
					? TRANSACTION_TYPE.pre_order_delivery
					: TRANSACTION_TYPE.pre_order_pickup
			);
		} catch (error) {
			db.collection('pre-orders').doc(data.order_id).update({
				status: ORDER_STATUS_ENUM.insufficient_funds,
			});
			throw error;
		}

		// Send email confirmation for order
		const studentEmail = `${docDataPreOrder.customerRollNumber}@lums.edu.pk`;
		const subject = 'CardPay | Order Confirmation';
		const orderType = docDataPreOrder.isDelivery ? 'Delivery' : 'Pick-up';

		let amount = 0;
		docDataPreOrder.cart.forEach((c) => {
			amount += c.quantity * c.price;
		});

		const n = docDataPreOrder.customerName;
		const r = docDataPreOrder.customerRollNumber;

		let textData = `<p>Your order was accepted by the restaurant</p>`;
		textData += `<p>${n} ${r}</p>`;
		textData += docDataPreOrder.cart
			.map((i) => `${i.name}: ${i.quantity}`)
			.join(`</p><p>`);
		textData = `<p>${textData}</p>`;
		textData += `<p>Total: ${amount}</p><p>Order type: ${orderType}</p>`;
		return sendEmail(studentEmail, subject, textData, textData);
	});

interface DenyPickupOrderData {
	cart: Array<{
		name: string;
		price: number;
		restaurant_id: string;
		quantity: number;
	}>;
	order_id: string;
	restaurant_id: string;
	customer_uid: string;
}

export const denyPickupOrder = functions
	.region('asia-south1')
	.https.onCall(async (data: DenyPickupOrderData, context) => {
		/*
			This function denys an order request
		*/

		functions.logger.info('Args:', data);

		const { userSnapshot } = await checkUserAuthAndDoc(context);
		if (userSnapshot.data()!.role !== 'vendor') {
			throwError(
				'permission-denied',
				'Only vendors can call this function'
			);
		}

		let docDataPreOrder: PreOrders = {
			cart: [],
			customerName: '',
			customerRollNumber: '',
			isDelivery: false,
			order_id: '',
			restaurant_id: '',
			specialInstructions: '',
			status: ORDER_STATUS_ENUM.pending,
			user_uid: '',
			contactNumber: '',
			deliveryAddress: '',
		};

		await db.runTransaction(async (transaction) => {
			const new_order_requests_ref = db
				.collection('new_order_requests')
				.doc(data.restaurant_id);
			const pre_order_ref = db
				.collection('pre-orders')
				.doc(data.order_id);

			const docPreOrder = await transaction.get(pre_order_ref);
			docDataPreOrder = docPreOrder.data() as PreOrders;

			const docNewOrderRequest = await transaction.get(
				new_order_requests_ref
			);
			const docDataNewOrderRequest =
				docNewOrderRequest.data() as NewOrderRequests;

			if (docDataPreOrder.status !== ORDER_STATUS_ENUM.pending) {
				throwError(
					'failed-precondition',
					'Order is not in pending state'
				);
			}

			if (!(data.customer_uid in docDataNewOrderRequest.orders)) {
				throwError('failed-precondition', 'Order doesnt exist');
			}

			// Remove this from the order map
			delete docDataNewOrderRequest.orders[data.customer_uid];

			transaction.update(new_order_requests_ref, {
				orders: docDataNewOrderRequest.orders,
			});

			transaction.update(pre_order_ref, {
				status: ORDER_STATUS_ENUM.denied,
			});
		});

		// Send email confirmation for order
		const studentEmail = `${docDataPreOrder.customerRollNumber}@lums.edu.pk`;
		const subject = 'CardPay | Order Denial';
		const orderType = docDataPreOrder.isDelivery ? 'Delivery' : 'Pick-up';

		let amount = 0;
		docDataPreOrder.cart.forEach((c) => {
			amount += c.quantity * c.price;
		});

		const n = docDataPreOrder.customerName;
		const r = docDataPreOrder.customerRollNumber;

		let textData = `<p>Your order was denied by the restaurant</p>`;
		textData += `<p>${n} ${r}</p>`;
		textData += docDataPreOrder.cart
			.map((i) => `${i.name}: ${i.quantity}`)
			.join(`</p><p>`);
		textData = `<p>${textData}</p>`;
		textData += `<p>Total: ${amount}</p><p>Order type: ${orderType}</p>`;
		return sendEmail(studentEmail, subject, textData, textData);
	});
