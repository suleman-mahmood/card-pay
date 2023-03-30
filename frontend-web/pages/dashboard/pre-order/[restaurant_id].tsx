import type { NextPage } from 'next';
import { useEffect, useState } from 'react';
import BackButton from '../../../components/buttons/BackButton';
import ErrorAlert from '../../../components/cards/ErrorAlert';
import DashboardLayout from '../../../components/layouts/DashboardLayout';
import BoxLoading from '../../../components/loaders/BoxLoading';
import { doc, getDoc } from 'firebase/firestore';
import { db } from '../../../services/initialize-firebase';
import { useRouter } from 'next/router';
import { useDispatch, useSelector } from 'react-redux';
import { incrementItemsCount } from '../../../store/cartSlice';
import { selectCart } from '../../../store/store';

interface RestaurantDetails {
	description: string;
	rating: number;
	menu: Array<{
		name: string;
		price: number;
		category: string;
		description: string;
	}>;
}

const restaurant_map = new Map<string, string>([
	['kJsH8JZUXWM8inVd4K3rl2BMzZ32', 'The Bunkers'],
	['x9YRwWaAjEhGaqqFrK8UN5ulfWJ3', 'Delish'],
	['g6lwpLs9e5PkLGksluN8GMk3GLg2', 'Chop Chop'],
	['7h2Oo2aLVBgcYF9u4PIsGZZkLYB2', 'Juice Zone'],
	['2V2NmkCJyMd9AtQYg6q4ES51q1o1', 'Frooti'],
	['2BTm3kcTW6ar1WfVAWoUysHuAkn2', 'Baradari'],
	['ZSNSJzaE6hg0K9XueSvuy2qltc82', 'JJ Kitchen Food'],
	['j4lFpFk51rgQcipHvss8GucqzPV2', 'JJ Kitchen Desserts'],
]);

const DigitalCard: NextPage = () => {
	const router = useRouter();

	const { cartState } = useSelector(selectCart);
	const dispatch = useDispatch();

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
		dispatch(incrementItemsCount());

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
			[category: string]: Array<{
				name: string;
				price: number;
				description: string;
			}>;
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
				<hr className='h-px bg-gray-200 border-2'></hr>
				{newMenu[key].map((item, i) => (
					<div
						key={i}
						className='mt-2 card bg-base-100 border-2 outline-gray-400'
					>
						<div className='card-body py-2'>
							<div className='flex flex-row card-title'>
								<p className='max-w-max font-medium text-left'>
									{item.name}
								</p>
								<div className='grow'></div>
								<button
									className='btn btn-primary bg-gradient-to-l from-primary to-primarydark border-none text-2xl mt-2 text-white rounded-full'
									onClick={() => addToCart(item)}
								>
									+
								</button>
							</div>
							<div className='justify-start'>
								<p className='max-w-max -mt-2 text-lg'>
									Price: {item.price}
								</p>
								{item.description !== undefined ? (
									<p className='max-w-max font-medium text-left'>
										{item.description}
									</p>
								) : null}
							</div>
						</div>
						<hr className='h-px bg-gray-200 border-2'></hr>
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

				<h1 className='text-3xl text-white font-semibold -mt-1'>
					{restaurant_map.get((restaurant_id as string)!)
						? restaurant_map.get((restaurant_id as string)!)
						: 'Noname'}
				</h1>
				<div className='h-10'></div>
				<img
					src='https://i.ibb.co/p4Lk71y/ramadan.png'
					className='scale-110 rounded-3xl shadow-lg'
				></img>
				{displayMenu()}
			</div>

			{/* Cart button below */}
			{cartState.itemsCount !== 0 ? (
				<div className='fixed bottom-4 left-0 w-full '>
					<button
						className='w-3/4 btn btn-primary bg-gradient-to-l from-primary to-primarydark border-hidden shadow-sm text-white'
						onClick={redirectToCart}
					>
						<p className='py-2 px-4 mr-2 bg-red-500 rounded-lg'>
							{cartState.itemsCount}
						</p>
						<p>items in cart</p>
					</button>
				</div>
			) : null}
		</DashboardLayout>
	);
};

export default DigitalCard;
