import { onAuthStateChanged } from 'firebase/auth';
import type { NextPage } from 'next';
import { useRouter } from 'next/router';
import React, { useEffect, useState } from 'react';
import TextField from '../components/text-field';
import { auth, db, functions } from '../services/initialize-firebase';
import { User as FirebaseUser } from 'firebase/auth';
import Navbar from '../components/navbar';
import { httpsCallable } from 'firebase/functions';
import Swal from 'sweetalert2';
import Loader from '../components/loader';
import {
	collection,
	doc,
	getDoc,
	getDocs,
	onSnapshot,
	query,
	where,
} from 'firebase/firestore';
import { FirebaseError } from 'firebase/app';

enum ORDER_STATUS_ENUM {
	pending = 'pending',
	confirmed = 'confirmed',
	denied = 'denied',
	expired = 'expired',
	insufficient_funds = 'insufficient_funds',
}

interface PreOrdersDoc {
	userUid: string;
	orderId: string;
	cart: Array<{
		restaurantId: string;
		name: string;
		price: number;
		quantity: number;
	}>;
	status: ORDER_STATUS_ENUM;
	restaurantId: string;
	specialInstructions: string;
	isDelivery: boolean;
	customerName: string;
	customerRollNumber: string;
	contactNumber: string;
	deliveryAddress: string;
	timestamp: number;
}

interface userDataDoc {
	balance: number;
	email: string;
	fullName: string;
	id: string;
	role: string;
	rollNumber: string;
	verified: boolean;
	transactions: Array<{
		amount: number;
		id: string;
		recipientName: string;
		senderName: string;
		status: string;
		timestamp: string;
	}>;
}

const Transactions: NextPage = () => {
	const router = useRouter();

	const [loading, setLoading] = useState(true);
	const [errorMessage, setErrorMessage] = useState('');

	const [preOrders, setPreOrders] = useState<Array<PreOrdersDoc> | null>(
		null
	);

	const [user, setUser] = useState<FirebaseUser | null>(null);
	const [userData, setUserData] = useState<userDataDoc | null>(null);
	const [playAudio, setPlayAudio] = useState(false);
	const [intervalId, setIntervalId] = useState<NodeJS.Timer>();
	const [order, setOrder] = useState<{
		[uid: string]: {
			orderId: string;
			cart: Array<{
				restaurantId: string;
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
			timestamp: number;
		};
	}>();

	useEffect(() => {
		return onAuthStateChanged(auth, (user) => {
			if (user) {
				console.log(user.uid);
				fetchPreOrders(user.uid);
			} else {
				router.push('/');
			}
		});
	}, []);

	const fetchPreOrders = async (uid: string) => {
		const now = Date.now();
		const twoHours = 2 * 60 * 60 * 1000;
		const twoHoursAgo = now - twoHours;

		const colRef = collection(db, 'pre-orders');
		const q = query(
			colRef,
			where('restaurantId', '==', uid),
			where('timestamp', '>=', twoHoursAgo),
			where('status', '==', 'confirmed')
		);
		const querySnapshot = await getDocs(q);

		if (querySnapshot.empty) {
			console.log('Could not find user document');
		} else {
			const docs = querySnapshot.docs.map(
				(d) => d.data() as PreOrdersDoc
			);
			setPreOrders(docs.reverse());
		}

		setLoading(false);
	};

	/*
		Pre order stuff
	*/

	useEffect(() => {
		return onAuthStateChanged(auth, (user) => {
			if (user) {
				setUser(user);
				fetchUserData(user.uid);
			} else {
				router.push('/');
			}
		});
	}, []);

	const fetchUserData = async (uid: string) => {
		const docRef = doc(db, 'users', uid);
		const docSnap = await getDoc(docRef);

		if (docSnap.exists()) {
			setUserData(docSnap.data() as userDataDoc);
		} else {
			console.log('Could not find user document');
		}

		setLoading(false);
	};

	useEffect(() => {
		if (user === null) {
			return;
		}
		const restaurantId = user.uid;
		return onSnapshot(
			doc(db, 'new_order_requests', restaurantId),
			async (d) => {
				if (Object.keys(d.data()?.orders).length !== 0) {
					setPlayAudio(true);
				} else {
					setPlayAudio(false);
				}
				setOrder(d.data()?.orders);
				console.log(d.data()?.orders);
			}
		);
	}, [user]);

	useEffect(() => {
		// Play audio
		const play = async () => {
			let audio = new Audio(
				'https://assets.mixkit.co/active_storage/sfx/940/940-preview.mp3'
			);

			await audio.play();
			let id = setInterval(async () => {
				await audio.play();
			}, 1500);
			setIntervalId(id);
		};

		if (playAudio) {
			play();
		} else {
			clearInterval(intervalId);
		}
	}, [playAudio]);

	const handleOpenOrderRequest = async (uid: string) => {
		setPlayAudio(false);

		if (order === undefined || user == null) {
			return;
		}
		const restaurantId = user.uid;
		const orderType = order[uid].isDelivery ? 'Delivery' : 'Pick-up';
		const amount = getBalance(order[uid].cart);
		const n = order[uid].customerName;
		const r = order[uid].customerRollNumber;

		let textData = `<p>${n} ${r}</p>`;
		textData += `<p>Order type: ${orderType}</p>`;

		if (order[uid].isDelivery) {
			textData += `<p>Contact: ${order[uid].contactNumber}</p>`;
			textData += `<p>Address: ${order[uid].deliveryAddress}</p>`;
		}

		const itemsList = order[uid].cart
			.map((i) => `${i.name}: ${i.quantity}`)
			.join(`</p><p>`);
		textData += `<p>${itemsList}</p>`;
		textData += `<p>Total: ${amount}</p>`;

		const si = order[uid].specialInstructions;
		if (si.length !== 0) {
			textData += `<p>Special instructions: ${si}</p>`;
		}

		const res = await Swal.fire({
			title: 'Order Details',
			html: textData,
			showDenyButton: true,
			confirmButtonText: 'Accept',
			denyButtonText: `Reject`,
		});

		if (res.isConfirmed) {
			try {
				const confirmPickupOrder = httpsCallable(
					functions,
					'confirmPickupOrder'
				);
				await confirmPickupOrder({
					cart: order[uid].cart,
					orderId: order[uid].orderId,
					restaurantId: restaurantId,
					customerUid: uid,
				});
				Swal.fire({
					icon: 'success',
					title: 'Order Accpeted',
				});
			} catch (error) {
				const message = (error as FirebaseError).message;
				setErrorMessage(message);
				console.log(error);
				Swal.fire({
					icon: 'error',
					title: 'Order Declined',
					text: message,
				});
			}
		}
		if (res.isDenied) {
			try {
				const denyPickupOrder = httpsCallable(
					functions,
					'denyPickupOrder'
				);
				await denyPickupOrder({
					cart: order[uid].cart,
					orderId: order[uid].orderId,
					restaurantId: restaurantId,
					customerUid: uid,
				});
			} catch (error) {
				setErrorMessage((error as FirebaseError).message);
				console.log(error);
			}
		}
	};

	const getBalance = (
		cart: Array<{
			quantity: number;
			price: number;
		}>
	): number => {
		let balance = 0;

		cart.forEach((c) => {
			balance += c.quantity * c.price;
		});

		return balance;
	};

	return loading ? (
		<Loader />
	) : (
		<div className='min-h-screen flex flex-col'>
			<Navbar />
			<div className='hero flex-grow'>
				<div className='w-full hero-content text-center'>
					<div className='w-full'>
						<h1 className='mb-4 text-5xl font-bold'>Pre Orders</h1>

						{/* Pre order stuff */}
						<div className='stack'>
							{order !== undefined
								? Object.keys(order).map((uid) => (
										<div
											className='mb-4 card bg-white text-black shadow-xl'
											onClick={() =>
												handleOpenOrderRequest(uid)
											}
											key={uid}
										>
											<div className='card-body'>
												{order[uid].cart.map(
													(item, i) => (
														<p key={i}>
															{item.name}:{' '}
															{item.quantity}
														</p>
													)
												)}
											</div>
										</div>
								  ))
								: null}
						</div>

						{/* Error dialogue box */}
						{errorMessage === '' ? null : (
							<div className='mt-6 alert alert-error shadow-lg'>
								<div>
									<svg
										xmlns='http://www.w3.org/2000/svg'
										className='stroke-current flex-shrink-0 h-6 w-6'
										fill='none'
										viewBox='0 0 24 24'
									>
										<path
											strokeLinecap='round'
											strokeLinejoin='round'
											strokeWidth='2'
											d='M10 14l2-2m0 0l2-2m-2 2l-2-2m2 2l2 2m7-2a9 9 0 11-18 0 9 9 0 0118 0z'
										/>
									</svg>
									<span>Error! {errorMessage}</span>
								</div>
							</div>
						)}

						<h2 className='text-2xl my-4'>Delivery orders</h2>
						<div className='w-full overflow-x-auto'>
							<table className='table w-full'>
								<thead>
									<tr>
										<th>Customer Name</th>
										<th>Customer Roll Number</th>
										<th>Cart</th>
										<th>Contact Number</th>
										<th>Delivery Address</th>
										<th>Special Instructions</th>
									</tr>
								</thead>
								<tbody>
									{preOrders
										?.filter((v) => v.isDelivery)
										.map((v, i) => (
											<tr key={i}>
												<th>{v.customerName}</th>
												<th>{v.customerRollNumber}</th>
												<th>
													{v.cart.map((items, i) => (
														<p key={i}>
															{items.name}:{' '}
															{items.quantity}
														</p>
													))}
												</th>
												<th>{v.contactNumber}</th>
												<th>{v.deliveryAddress}</th>
												<th>{v.specialInstructions}</th>
												{/* <th>
													{formatTimestamp(
														v.timestamp
													)}
												</th> */}
											</tr>
										))}
								</tbody>
							</table>
						</div>

						<h2 className='text-2xl my-4'>Pickup orders</h2>
						<div className='w-full overflow-x-auto'>
							<table className='table w-full'>
								<thead>
									<tr>
										<th>Customer Name</th>
										<th>Customer Roll Number</th>
										<th>Cart</th>
										<th>Special Instructions</th>
									</tr>
								</thead>
								<tbody>
									{preOrders
										?.filter((v) => !v.isDelivery)
										.map((v, i) => (
											<tr key={i}>
												<th>{v.customerName}</th>
												<th>{v.customerRollNumber}</th>
												<th>
													{v.cart.map((items, i) => (
														<p key={i}>
															{items.name}:{' '}
															{items.quantity}
														</p>
													))}
												</th>
												<th>{v.specialInstructions}</th>
												{/* <th>
													{formatTimestamp(
														v.timestamp
													)}
												</th> */}
											</tr>
										))}
								</tbody>
							</table>
						</div>
					</div>
				</div>
			</div>
		</div>
	);
};

export default Transactions;
