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
import { useSelector } from 'react-redux';
import { selectUser } from '../../../store/store';
import TextField from '../../../components/inputs/TextField';

const DigitalCard: NextPage = () => {
	const { userState } = useSelector(selectUser);

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
			restaurant_id: string;
			quantity: number;
		}>
	>();

	useEffect(() => {
		const cartString = localStorage.getItem('cart');

		if (cartString) {
			const cart = JSON.parse(cartString) as Array<{
				name: string;
				price: number;
				restaurant_id: string;
				quantity: number;
			}>;

			setCart(cart);
		}
	}, []);

	const decreaseQuantity = (index: number) => {
		const cartString = localStorage.getItem('cart');

		const cart = JSON.parse(cartString!) as Array<{
			name: string;
			price: number;
			restaurant_id: string;
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
		const cartString = localStorage.getItem('cart');

		const cart = JSON.parse(cartString!) as Array<{
			name: string;
			price: number;
			restaurant_id: string;
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
				(res.data as { order_id: string }).order_id
			);
		} catch (error) {
			setHideModal(true);
			setErrorMessage((error as FirebaseError).message);
			console.log(error);
		}
	};

	const waitingForOrderConfirmation = (order_id: string) => {
		console.log(order_id);
		return onSnapshot(doc(db, 'pre-orders', order_id), (d) => {
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

				<h2 className='mb-2 text-xl'>{cart?.at(0)?.restaurant_id}</h2>

				{cart?.map((cartItem, index) => (
					<div
						className='mb-4 card bg-base-100 shadow-xl'
						key={index}
					>
						<div className='card-body'>
							<div className='card-title'>
								<p>{cartItem.name}</p>
							</div>
							<div className='flex flex-row'>
								<p>Price: {cartItem.price}</p>
								<p>Quantity: {cartItem.quantity}</p>
							</div>
						</div>

						<div className='card-actions justify-center'>
							<button
								className='btn btn-success'
								onClick={() => increaseQuantity(index)}
							>
								Increase quantity
							</button>
							<button
								className='btn btn-error'
								onClick={() => decreaseQuantity(index)}
							>
								Decrease quantity
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
							className='w-full btn btn-primary'
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
