import type { NextPage } from 'next';
import { useEffect, useState } from 'react';
import BackButton from '../../../components/buttons/BackButton';
import ErrorAlert from '../../../components/cards/ErrorAlert';
import DashboardLayout from '../../../components/layouts/DashboardLayout';
import BoxLoading from '../../../components/loaders/BoxLoading';
import { doc, getDoc } from 'firebase/firestore';
import { db } from '../../../services/initialize-firebase';
import { useRouter } from 'next/router';

interface RestaurantDetails {
	description: string;
	rating: number;
	menu: Array<{
		name: string;
		price: number;
		category: string;
	}>;
}

const DigitalCard: NextPage = () => {
	const router = useRouter();
	const { restaurant_id } = router.query;

	const [errorMessage, setErrorMessage] = useState('');
	const [isLoading, setIsLoading] = useState(false);

	const [menu, setMenu] = useState<RestaurantDetails>();

	useEffect(() => {
		const fetchRestaurantMenu = async () => {
			if (restaurant_id === undefined) {
				return;
			}
			const docRef = doc(db, 'restaurants', restaurant_id as string);
			const docSnap = await getDoc(docRef);
			const docData = docSnap.data() as RestaurantDetails;
			setMenu(docData);
			console.log(docData);
		};

		fetchRestaurantMenu();
	}, [restaurant_id]);


	const redirectToCart = async () => {
		router.push('/dashboard/pre-order/cart');
	};

	const addToCart = (item: { name: string; price: number }) => {
		const cartString = localStorage.getItem('cart');
		const newCartItem = {
			...item,
			restaurantId: restaurant_id as string,
			quantity: 1,
		};

		if (cartString) {
			const cart = JSON.parse(cartString) as Array<{
				name: string;
				price: number;
				restaurantId: string;
				quantity: number;
			}>;

			let found = false;
			let loc = -1;
			cart.forEach((c, index) => {
				if (c.name === item.name) {
					found = true;
					loc = index;
				}
			});

			if (found) {
				cart[loc].quantity++;
			} else {
				cart.push(newCartItem);
			}

			localStorage.setItem('cart', JSON.stringify(cart));
		} else {
			localStorage.setItem('cart', JSON.stringify([newCartItem]));
		}

	};

	const displayMenu = () => {
		const newMenu: {
			[category: string]: Array<{ name: string; price: number }>;
		} = {};

		menu?.menu.forEach((item) => {
			if (item.category in newMenu) {
				newMenu[item.category].push(item);
			} else {
				newMenu[item.category] = [item];
			}
		});

		return Object.keys(newMenu).map((key) => (
			<div key={key}>
				<p className='text-2xl mt-4 font-bold text-left'>{key}</p>
				<hr className='h-px bg-gray-200 border-2 dark:bg-gray-700'></hr>
				{newMenu[key].map((item, i) => (
					<div key={i} className='mt-2 card bg-base-100 border-2 outline-gray-400'>
						<div className='card-body py-2'>
							<div className='flex flex-row card-title'>
								<p className='max-w-max font-medium text-left'>{item.name}</p>
								<div className='grow'></div>
								<button
										className='btn btn-primary bg-gradient-to-l from-primary to-primarydark border-none text-2xl mt-2 text-white rounded-full'
										onClick={() => addToCart(item)}
									>
										+
									</button>
							</div>
							<div className='justify-start'>
								<p className='max-w-max -mt-2 text-lg'>Price: {item.price}</p>
							</div>
						</div>
						<hr className='h-px bg-gray-200 border-2 dark:bg-gray-700'></hr>
					</div>
				))}
			</div>
		));
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
				<ErrorAlert message={errorMessage} />
				<BackButton />

				<h1 className='text-2xl text-white font-semibold'>
					Available Restaurants
				</h1>

				<div className='h-12'></div>

				{displayMenu()}
			</div>
			<div className='fixed bottom-0 left-0 z-50 w-full h-16 bg-white border-t border-gray-200 dark:bg-gray-700 dark:border-gray-600 px-2'>
				<button className='btn btn-primary w-full mt-2 bg-gradient-to-l from-primary to-primarydark border-hidden shadow-sm text-white' onClick={redirectToCart}>
					View your Cart
				</button>
			</div>
		</DashboardLayout>
	);
};

export default DigitalCard;
