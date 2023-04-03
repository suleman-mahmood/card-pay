import * as functions from 'firebase-functions';
import { db } from './initialize';
import { denyPickupOrderHelper } from './pre-order/order';

const MILLISECONDS_IN_ONE_MIN = 60000;
const ORDER_EXPIRY = MILLISECONDS_IN_ONE_MIN * 5;

export const houseKeeper = functions.pubsub
	.schedule('every 5 minutes')
	.onRun(async () => {
		functions.logger.info(
			'House Keeper initiated which will run every 5 minutes!'
		);

		await handlePickupOrdersExpiry();

		return;
	});

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
