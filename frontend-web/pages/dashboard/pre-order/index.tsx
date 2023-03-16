import type { NextPage } from 'next';
import { useEffect, useState } from 'react';
import BackButton from '../../../components/buttons/BackButton';
import ErrorAlert from '../../../components/cards/ErrorAlert';
import DashboardLayout from '../../../components/layouts/DashboardLayout';
import BoxLoading from '../../../components/loaders/BoxLoading';
import JJKitchenImage from '../../../assets/jj-kitchen.jpg';
import RestaurantCard from '../../../components/cards/RestaurantCard';
import { doc, getDoc } from 'firebase/firestore';
import { db } from '../../../services/initialize-firebase';

interface RestaurantList {
	restaurant_list: Array<{ id: string; name: string; description: string }>;
}

const DigitalCard: NextPage = () => {
	const [errorMessage, setErrorMessage] = useState('');
	const [isLoading, setIsLoading] = useState(false);

	const [restaurantList, setRestaurantList] = useState<RestaurantList>();

	useEffect(() => {
		const fetchRestaurants = async () => {
			const docRef = doc(db, 'restaurant_list', 'restaurant_list');
			const docSnap = await getDoc(docRef);
			const docData = docSnap.data() as RestaurantList;
			setRestaurantList(docData);
		};

		fetchRestaurants();
	}, []);

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

				{restaurantList?.restaurant_list.map(
					({ name, id, description }) => (
						<div className='mb-4' key={id}>
							<RestaurantCard
								key={id}
								id={id}
								bgImage={JJKitchenImage}
								title={name}
								description={description}
							/>
						</div>
					)
				)}
			</div>
		</DashboardLayout>
	);
};

export default DigitalCard;
