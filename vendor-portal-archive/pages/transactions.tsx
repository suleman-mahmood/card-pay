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
import { doc, getDoc, onSnapshot } from 'firebase/firestore';
import { FirebaseError } from 'firebase/app';

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

	const formatTimestamp = (timestamp: string | number): string => {
		const date = new Date(timestamp);
		const options: Intl.DateTimeFormatOptions = {
			weekday: 'long',
			year: 'numeric',
			month: 'long',
			day: 'numeric',
			hour: 'numeric',
			minute: 'numeric',
		};

		return date.toLocaleDateString('en-US', options);
	};

	const showTransactions = () => {
		const transactions = userData?.transactions.map((v) => {
			const d = new Date(v.timestamp);
			return { ...v, timestamp: d.getTime() };
		});

		if (transactions === undefined) {
			return;
		}

		transactions.sort((obj1, obj2) => obj2.timestamp - obj1.timestamp);

		const lastReconcile = [];
		for (let i = 0; i < transactions.length; i++) {
			const t = transactions[i];

			if (t.senderName === userData?.fullName) {
				break;
			}

			lastReconcile.push(t);
		}

		return lastReconcile.map((v, i) => (
			<tr key={i}>
				<th>{v.senderName}</th>
				<th>{v.amount}</th>
				<th>{formatTimestamp(v.timestamp)}</th>
			</tr>
		));
	};

	/*
		Pre order stuff
	*/
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
						<h1 className='mb-4 text-5xl font-bold'>
							Transactions
						</h1>

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

						<p>{userData?.fullName}</p>
						<p className='mb-8'>Balance: {userData?.balance}</p>

						<div className='w-full overflow-x-auto'>
							<table className='table w-full'>
								<thead>
									<tr>
										<th>Sender Name</th>
										<th>Amount</th>
										<th>Timestamp</th>
									</tr>
								</thead>
								<tbody>{showTransactions()}</tbody>
							</table>
						</div>
					</div>
				</div>
			</div>
		</div>
	);
};

export default Transactions;
