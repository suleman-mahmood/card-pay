import type { NextPage } from 'next';
import { useEffect, useState } from 'react';
import BackButton from '../../../components/buttons/BackButton';
import ErrorAlert from '../../../components/cards/ErrorAlert';
import DashboardLayout from '../../../components/layouts/DashboardLayout';
import BoxLoading from '../../../components/loaders/BoxLoading';
import { db, functions } from '../../../services/initialize-firebase';
import { httpsCallable } from 'firebase/functions';
import { FirebaseError } from 'firebase/app';
import { doc, onSnapshot } from 'firebase/firestore';
import SuccessAlert from '../../../components/cards/SuccessAlert';
import { useDispatch, useSelector } from 'react-redux';
import { selectUser } from '../../../store/store';
import TextField from '../../../components/inputs/TextField';
import {
	decrementItemsCount,
	incrementItemsCount,
} from '../../../store/cartSlice';

const restaurant_map = new Map<string, string>([
	['kJsH8JZUXWM8inVd4K3rl2BMzZ32', 'The Bunkers'],
	['x9YRwWaAjEhGaqqFrK8UN5ulfWJ3', 'Delish'],
	['g6lwpLs9e5PkLGksluN8GMk3GLg2', 'Chop Chop'],
	['7h2Oo2aLVBgcYF9u4PIsGZZkLYB2', 'Juice Zone'],
	['2V2NmkCJyMd9AtQYg6q4ES51q1o1', 'Frooti'],
	['2BTm3kcTW6ar1WfVAWoUysHuAkn2', 'Baradari'],
	['ZSNSJzaE6hg0K9XueSvuy2qltc82', 'JJ Kitchen Food'],
	['j4lFpFk51rgQcipHvss8GucqzPV2', 'JJ Kitchen Drinks & Desserts'],
]);

const DigitalCard: NextPage = () => {
	const { userState } = useSelector(selectUser);
	const dispatch = useDispatch();

	const [errorMessage, setErrorMessage] = useState('');
	const [successMessage, setSuccessMessage] = useState('');

	const [isLoading, setIsLoading] = useState(false);

	const [hideModal, setHideModal] = useState(false);
	const [isDelivery, setIsDelivery] = useState(false);
	const [specialInstructions, setSpecialInstructions] = useState('');
	const [contactNumber, setContactNumber] = useState('');
	const [address, setAddress] = useState('');

	const [cart, setCart] = useState<
		Array<{
			name: string;
			price: number;
			restaurantId: string;
			quantity: number;
		}>
	>();

	useEffect(() => {
		const cartString = localStorage.getItem('cart');

		if (cartString) {
			const cart = JSON.parse(cartString) as Array<{
				name: string;
				price: number;
				restaurantId: string;
				quantity: number;
			}>;

			setCart(cart);
		}
	}, []);

	const decreaseQuantity = (index: number) => {
		dispatch(decrementItemsCount());

		const cartString = localStorage.getItem('cart');

		const cart = JSON.parse(cartString!) as Array<{
			name: string;
			price: number;
			restaurantId: string;
			quantity: number;
		}>;

		cart[index].quantity--;

		if (cart[index].quantity <= 0) {
			cart.splice(index, 1);
		}

		setCart(cart);
		localStorage.setItem('cart', JSON.stringify(cart));
	};

	const increaseQuantity = (index: number) => {
		dispatch(incrementItemsCount());

		const cartString = localStorage.getItem('cart');

		const cart = JSON.parse(cartString!) as Array<{
			name: string;
			price: number;
			restaurantId: string;
			quantity: number;
		}>;

		cart[index].quantity++;

		setCart(cart);
		localStorage.setItem('cart', JSON.stringify(cart));
	};

	const checkout = async () => {
		setErrorMessage('');

		if (isDelivery) {
			if (contactNumber.length === 0 || address.length === 0) {
				setErrorMessage(
					'Please enter your contact number and delivery address or choose pickup if you want to pick it from the restaurant directly'
				);
				setTimeout(() => {
					document.getElementById('my-modal-6')?.click();
				}, 1000);
				return;
			}
		}

		try {
			const createPickupOrder = httpsCallable(
				functions,
				'createPickupOrder'
			);
			const res = await createPickupOrder({
				cart: cart,
				specialInstructions: specialInstructions,
				isDelivery: isDelivery,
				customerName: userState.fullName,
				customerRollNumber: userState.rollNumber,
				contactNumber: contactNumber,
				deliveryAddress: address,
			});

			// Remove cart and its items
			localStorage.clear();
			setCart([]);
			setErrorMessage('');

			console.log('Response data');
			console.log(res.data);

			waitingForOrderConfirmation(
				(res.data as { orderId: string }).orderId
			);
		} catch (error) {
			setHideModal(true);
			setErrorMessage((error as FirebaseError).message);
			console.log(error);
		}
	};

	const waitingForOrderConfirmation = (orderId: string) => {
		return onSnapshot(doc(db, 'pre-orders', orderId), (d) => {
			if (!d.exists) {
				return;
			}
			const status = d.data()!.status as string;

			if (status === 'confirmed') {
				setSuccessMessage('Order confirmed!');
				setHideModal(true);
			} else if (status === 'denied') {
				setErrorMessage('Order denied');
				setHideModal(true);
			} else if (status === 'expired') {
				setErrorMessage('Order expired');
				setHideModal(true);
			}
		});
	};

	const getBalance = (): number => {
		let balance = 0;

		cart?.forEach((c) => {
			balance += c.quantity * c.price;
		});

		return balance;
	};

	const toggleDelivery = (e: React.FormEvent<HTMLInputElement>) => {
		setIsDelivery(e.currentTarget.checked);
	};

	return isLoading ? (
		<BoxLoading />
	) : (
		<DashboardLayout
			displayBottomNav={false}
			displayCard={false}
			displayCart={true}
		>
			<div className='flex flex-col'>
				<BackButton />

				<h1 className='text-2xl text-white font-semibold'>Your Cart</h1>

				<div className='h-12'></div>

				<h2 className='mb-2 text-2xl font-medium'>
					{restaurant_map.get(cart?.at(0)?.restaurantId!)
						? restaurant_map.get(cart?.at(0)?.restaurantId!)
						: null}
				</h2>

				{cart?.map((cartItem, index) => (
					<div
						className='mb-2 card bg-base-100 border-2 border-gray-200 shadow-md'
						key={index}
					>
						<div className='card-body py-2'>
							<div className='card-title'>
								<p>{cartItem.name}</p>
							</div>
							<div className='flex flex-row'>
								<p>Price: {cartItem.price}</p>
								<p>Quantity: {cartItem.quantity}</p>
							</div>
						</div>

						<div className='flex flex-row card-actions justify-center mb-2 mt-1'>
							<button
								className='btn btn-success text-3xl text-white w-14 bg-blue-600 focus:bg-blue-600 mr-2'
								onClick={() => increaseQuantity(index)}
							>
								+
							</button>
							<button
								className='btn btn-error text-3xl text-white w-14 bg-red-400 focus:bg-red-400 ml-2'
								onClick={() => decreaseQuantity(index)}
							>
								-
							</button>
						</div>
					</div>
				))}

				<p className='text-2xl my-2'>Total amount: {getBalance()}</p>

				<div className='form-control mb-6'>
					<label className='cursor-pointer label'>
						<span className='label-text text-lg'>Pick-up</span>
						<input
							type='checkbox'
							className='toggle'
							onChange={toggleDelivery}
						/>
						<span className='label-text text-lg'>Delivery</span>
					</label>
				</div>

				{isDelivery ? (
					<div>
						<TextField
							type='text'
							valueSetter={setContactNumber}
							placeholder='Contact Number'
							maxLength={11}
						/>
						<textarea
							className='w-full textarea textarea-bordered'
							placeholder='Delivery Address:'
							onChange={(e) => setAddress(e.target.value)}
						></textarea>
					</div>
				) : null}

				<textarea
					className='textarea textarea-bordered mb-6'
					placeholder='Special instructions if any'
					onChange={(e) => setSpecialInstructions(e.target.value)}
				></textarea>

				{/* Checkout button */}
				{cart !== undefined ? (
					cart.length !== 0 ? (
						<label
							htmlFor='my-modal-6'
							className='w-full btn btn-primary bg-gradient-to-l from-primary to-primarydark border-none text-white text-2xl'
							onClick={checkout}
						>
							Checkout
						</label>
					) : null
				) : null}

				<input
					type='checkbox'
					id='my-modal-6'
					className='modal-toggle'
				/>
				{hideModal ? null : (
					<div className='modal modal-bottom sm:modal-middle'>
						<div className='modal-box'>
							<h3 className='font-bold text-lg'>
								Waiting for restaurant to accept your order!
							</h3>
							<p className='py-4'>
								Please wait for order confirmation
							</p>
						</div>
					</div>
				)}
			</div>

			<SuccessAlert message={successMessage} />
			<ErrorAlert message={errorMessage} />
		</DashboardLayout>
	);
};

export default DigitalCard;
