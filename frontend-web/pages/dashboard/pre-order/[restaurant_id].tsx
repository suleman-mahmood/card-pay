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
		variantsExist: boolean;
		variants: Array<{
			name: string;
			price: number;
			category: string;
		}>;
	}>;
}

interface MenuItem {
	name: string;
	price: number;
}

interface MenuCategory {
	[key: string]: MenuItem[];
}

interface SelectedOptions {
	[key: string]: {
		isSelected: string | boolean;
		price: number;
		optional: boolean;
	};
}

interface Props {
	newMenu: MenuCategory;
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
	const [shouldDisplaySecondaryMenu, setShouldDisplaySecondaryMenu] =
		useState(false);

	const [menu, setMenu] = useState<RestaurantDetails>();
	const [selectedItemVariant, setSelectedItemVariant] = useState<{
		name: string;
		price: number;
		description: string;
		variantsExist: boolean;
		variants: Array<{
			name: string;
			price: number;
			category: string;
		}>;
	}>();
	const [selectedOptions, setSelectedOptions] = useState<SelectedOptions>({});

	useEffect(() => {
		const fetchRestaurantMenu = async () => {
			if (restaurant_id === undefined) {
				return;
			}
			const docRef = doc(db, 'restaurants', restaurant_id as string);
			const docSnap = await getDoc(docRef);
			const docData = docSnap.data() as RestaurantDetails;

			setMenu(docData);
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

	const handleAddClick = (item: {
		name: string;
		price: number;
		description: string;
		variantsExist: boolean;
		variants: Array<{
			name: string;
			price: number;
			category: string;
		}>;
	}) => {
		if (item.variantsExist === undefined) {
			addToCart(item);
			return;
		}

		if (!item.variantsExist) {
			addToCart(item);
			return;
		}

		setSelectedItemVariant(item);
		setShouldDisplaySecondaryMenu(true);
	};

	const displayMenu = () => {
		const newMenu: {
			[category: string]: Array<{
				name: string;
				price: number;
				description: string;
				variantsExist: boolean;
				variants: Array<{
					name: string;
					price: number;
					category: string;
				}>;
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
									onClick={() => handleAddClick(item)}
								>
									+
								</button>
							</div>
							<div className='justify-start'>
								<p className='max-w-max -mt-2 text-lg'>
									Price: {item.price}
								</p>
								{item.description !== undefined ? (
									<p className='max-w-max font-medium text-xs text-primarydark text-left'>
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

	const handleRadioChange = (
		event: React.ChangeEvent<HTMLInputElement>,
		item: MenuItem
	): void => {
		const name: string = event.target.name;
		const value: string = event.target.value;
		setSelectedOptions((prevState) => ({
			...prevState,
			[name]: { isSelected: value, price: item.price, optional: false },
		}));
	};

	const handleCheckboxChange = (
		event: React.ChangeEvent<HTMLInputElement>,
		item: MenuItem
	): void => {
		const name: string = event.target.value;
		const checked: boolean = event.target.checked;
		setSelectedOptions((prevState) => ({
			...prevState,
			[name]: { isSelected: checked, price: item.price, optional: true },
		}));
	};

	const displaySecondaryMenu = () => {
		const newMenu: {
			[category: string]: Array<{
				name: string;
				price: number;
				category: string;
			}>;
		} = {};

		selectedItemVariant?.variants.forEach((item) => {
			if (item.category in newMenu) {
				newMenu[item.category].push(item);
			} else {
				newMenu[item.category] = [item];
			}
		});

		return Object.keys(newMenu).map((key) => (
			<div key={key}>
				<p className='text-2xl mt-4 font-bold text-left'>{key}</p>
				<div className='flex flex-col gap-2'>
					<div className='flex flex-col gap-2'></div>
					{key !== 'optional' ? (
						<div>
							{newMenu[key].map((item: MenuItem) => (
								<label
									key={item.name}
									className='flex items-center'
								>
									<input
										type='radio'
										value={item.name}
										className='mr-2'
										name={key}
										checked={
											selectedOptions[key] &&
											selectedOptions[key].isSelected ===
												item.name
										}
										onChange={(e) =>
											handleRadioChange(e, item)
										}
									/>
									{item.name}: +Rs.{item.price}
								</label>
							))}
						</div>
					) : (
						<div>
							{newMenu[key].map((item: MenuItem) => (
								<label
									key={item.name}
									className='flex items-center'
								>
									<input
										type='checkbox'
										value={item.name}
										className='mr-2'
										checked={
											selectedOptions[item.name] &&
											(selectedOptions[item.name]
												.isSelected as boolean)
										}
										onChange={(e) =>
											handleCheckboxChange(e, item)
										}
									/>
									{item.name}: +Rs.{item.price}
								</label>
							))}
						</div>
					)}
				</div>
			</div>
		));
	};

	const handleAddToCart = () => {
		setErrorMessage('');

		let categories: string[] = [];
		selectedItemVariant?.variants.forEach((item) => {
			if (
				item.category !== 'optional' &&
				categories.indexOf(item.category) === -1
			) {
				categories.push(item.category);
			}
		});
		const uniqueItems = categories.length;

		let selectedUniqueItems = 0;
		Object.keys(selectedOptions).map((key) => {
			const option = selectedOptions[key];

			if (
				option.optional ||
				(typeof option.isSelected === 'boolean' &&
					option.isSelected === false)
			) {
				return;
			}

			selectedUniqueItems += 1;
		});

		if (uniqueItems !== selectedUniqueItems) {
			setErrorMessage('Please select all required items!');
			return;
		}

		let newName = `${selectedItemVariant!.name}`;
		let total = selectedItemVariant!.price;

		Object.keys(selectedOptions).map((key) => {
			const option = selectedOptions[key];

			if (typeof option.isSelected !== 'boolean') {
				total += option.price;
				newName += `, ${key}: ${option.isSelected}`;
			}
		});

		Object.keys(selectedOptions).map((key) => {
			const option = selectedOptions[key];

			if (
				typeof option.isSelected === 'boolean' &&
				option.isSelected === true
			) {
				total += option.price;
				newName += `, ${key}`;
			}
		});

		addToCart({ name: newName, price: total });
		setShouldDisplaySecondaryMenu(false);
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

			{shouldDisplaySecondaryMenu ? (
				<div className='fixed z-10 inset-0 overflow-y-auto'>
					<div className='flex items-center justify-center min-h-screen px-4 pt-4 pb-20 text-center'>
						<div
							className='fixed inset-0 transition-opacity'
							aria-hidden='true'
						>
							<div className='absolute inset-0 bg-gray-500 opacity-75'></div>
						</div>

						<div className='w-full inline-block align-bottom bg-gradient-to-l from-primary to-primarydark text-gray-200	 rounded-lg px-4 pt-5 pb-4 text-left overflow-hidden shadow-2xl border-2 border-gray-500 transform transition-all sm:my-8 sm:align-middle sm:max-w-lg sm:w-full sm:p-6'>
							<div className='sm:flex sm:items-start'>
								<div className='mt-3 text-center sm:mt-0 sm:ml-4 sm:text-left'>
									<h3 className='text-lg text-center leading-6 font-medium text-white'>
										{selectedItemVariant?.name}: Rs.
										{selectedItemVariant?.price}
									</h3>
									<div className='mt-2'>
										<p className='text-sm leading-5 text-gray-200'>
											{selectedItemVariant?.description}
										</p>
										{displaySecondaryMenu()}
										<ErrorAlert message={errorMessage} />
									</div>
								</div>
							</div>

							<div className='mt-5 sm:mt-4 sm:flex sm:flex-row-reverse'>
								<span className='flex w-full rounded-md shadow-sm sm:ml-3 sm:w-auto'>
									<button
										type='button'
										className='inline-flex btn-primary justify-center w-full rounded-md border border-transparent px-4 py-2 text-base leading-6 font-medium text-white shadow-sm  focus:outline-none  focus:shadow-outline-green transition ease-in-out duration-150 sm:text-sm sm:leading-5'
										onClick={handleAddToCart}
									>
										Add to cart
									</button>
								</span>

								<span className='mt-3 flex w-full rounded-md shadow-sm sm:mt-0 sm:w-auto'>
									<button
										type='button'
										className='inline-flex justify-center w-full rounded-md border border-gray-300 px-4 py-2 bg-white text-base leading-6 font-medium text-gray-700 shadow-sm hover:text-gray-500 focus:outline-none focus:border-blue-300 focus:shadow-outline-blue transition ease-in-out duration-150 sm:text-sm sm:leading-5'
										onClick={() => {
											setShouldDisplaySecondaryMenu(
												false
											);
											setErrorMessage('');
										}}
									>
										Cancel
									</button>
								</span>
							</div>
						</div>
					</div>
				</div>
			) : null}

			{/* Cart button below */}
			{!shouldDisplaySecondaryMenu && cartState.itemsCount !== 0 ? (
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
