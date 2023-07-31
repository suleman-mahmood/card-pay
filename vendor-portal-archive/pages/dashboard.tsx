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
import DashboardLayout from '../components/layouts/DashboardLayout';
import { doc, onSnapshot } from 'firebase/firestore';
import { FirebaseError } from 'firebase/app';

const KEY_PAD_CONFIG = [
	[1, 2, 3],
	[4, 5, 6],
	[7, 8, 9],
	['.', 0, '.'],
];

// Item not available
// Delivery not available
// Closing time
// Not operational

const FOCUS_DELAY = 500;

const Transactions: NextPage = () => {
	const router = useRouter();

	const [loading, setLoading] = useState(true);
	const [user, setUser] = useState<FirebaseUser | null>(null);
	const [amount, setAmount] = useState(0);
	const [rollNumber, setRollNumber] = useState(0);
	const [errorMessage, setErrorMessage] = useState('');
	const [shouldFocus, setShouldFocus] = useState(true);

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

	const getRandomInteger = (): number => {
		return Math.floor(Math.random() * 10000);
	};

	useEffect(() => {
		return onAuthStateChanged(auth, (user) => {
			if (user) {
				setUser(user);
				setLoading(false);
			} else {
				router.push('/');
			}
		});
	}, []);

	useEffect(() => {
		if (!shouldFocus) {
			return;
		}

		const intervalId = setInterval(() => {
			const elem = document.getElementById(
				'roll-number-input'
			) as HTMLInputElement;
			if (elem) {
				elem.readOnly = true;
				elem.focus();
				elem.readOnly = false;
			}
		}, FOCUS_DELAY);

		return () => clearInterval(intervalId);
	}, [shouldFocus]);

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

	const handleSubmit = async (e: React.FormEvent) => {
		e.preventDefault();
		setErrorMessage('');
		setShouldFocus(false);
		setLoading(true);
		setAmount(0);

		const cleanedRollNumber = rollNumber.toString().substring(4);

		const { value: userPin } = await Swal.fire({
			title: `Transaction for Rs.${amount}`,
			input: 'password',
			inputLabel: 'Input your 4-digit pin',
			inputPlaceholder: 'Enter your pin',
			inputAttributes: {
				maxLength: '4',
				pattern: '^[0-9]{4}$',
			},
		});

		if (!userPin) {
			setErrorMessage('Please enter pin');
			setShouldFocus(true);
			setLoading(false);
			Swal.fire({
				icon: 'error',
				title: `Transaction wasn't successful`,
				text: 'Please enter pin',
			});
			return;
		}

		const makeTransaction = httpsCallable(functions, 'makeTransaction');

		makeTransaction({
			amount: amount,
			senderRollNumber: cleanedRollNumber,
			pin: userPin,
		})
			.then((result) => {
				setShouldFocus(true);
				setLoading(false);

				Swal.fire({
					icon: 'success',
					title: 'Transaction was successful',
				});
			})
			.catch((error) => {
				setErrorMessage(error.message);
				setShouldFocus(true);
				setLoading(false);

				Swal.fire({
					icon: 'error',
					title: `Transaction wasn't successful`,
					text: error.message,
				});
			});
	};

	const handleAmountClick = (value: number) => {
		setAmount((oldAmount) => {
			const newAmount = oldAmount.toString() + value.toString();
			return parseInt(newAmount);
		});
	};

	const handleBackspace = () => {
		setAmount((oldAmount) => {
			const oldAmountStr = oldAmount.toString();
			if (oldAmountStr.length <= 1) {
				return 0;
			}
			const newAmount = oldAmountStr.slice(0, -1);
			return parseInt(newAmount);
		});
	};

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
		<DashboardLayout>
			<div className='min-h-screen flex flex-col'>
				<Navbar />
				<div className='hero flex-grow'>
					<div className='w-full hero-content text-center'>
						<div className='w-full flex flex-col items-center'>
							<h1 className='mb-4 text-5xl font-bold'>
								Dashboard
							</h1>

							<div className='w-3/4 flex flex-col items-center'>
								<div className='stack'>
									{order !== undefined
										? Object.keys(order).map((uid) => (
												<div
													className='mb-4 card bg-white text-black shadow-xl'
													onClick={() =>
														handleOpenOrderRequest(
															uid
														)
													}
													key={uid}
												>
													<div className='card-body'>
														{order[uid].cart.map(
															(item, i) => (
																<p key={i}>
																	{item.name}:{' '}
																	{
																		item.quantity
																	}
																</p>
															)
														)}
													</div>
												</div>
										  ))
										: null}
								</div>

								{KEY_PAD_CONFIG.map((k, i) => {
									return (
										<div
											key={getRandomInteger()}
											className='w-full flex flex-row justify-center mb-4'
										>
											{k.map((value) => {
												return (
													<div
														key={getRandomInteger()}
														className='w-1/4 px-2'
													>
														<button
															className='w-full text-2xl h-12 btn'
															onClick={() =>
																value != '.'
																	? handleAmountClick(
																			value as number
																	  )
																	: null
															}
														>
															{value}
														</button>
													</div>
												);
											})}
										</div>
									);
								})}
							</div>

							<div className='my-4 flex flex-row justify-center'>
								<button
									className='btn btn-primary mr-4'
									onClick={handleBackspace}
								>
									Delete
								</button>

								<button
									className='btn btn-secondary'
									onClick={() => setAmount(0)}
								>
									Clear amount
								</button>
							</div>

							<div className='flex flex-col items-center'>
								<form
									onSubmit={handleSubmit}
									className='form-control w-full max-w-xs'
								>
									<TextField
										inputType='number'
										labelText='Amount:'
										placeholder='xxxx'
										currentVal={amount}
										valueSetter={setAmount}
										readOnly={true}
									/>
									<TextField
										id='roll-number-input'
										inputType='password'
										labelText='Roll Number:'
										placeholder='00000000'
										valueSetter={setRollNumber}
									/>

									<button
										type='submit'
										className='mt-6 btn btn-outline btn-primary hidden'
									>
										Transact!
									</button>

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
												<span>
													Error! {errorMessage}
												</span>
											</div>
										</div>
									)}
								</form>
							</div>
						</div>
					</div>
				</div>
			</div>
		</DashboardLayout>
	);
};

export default Transactions;
