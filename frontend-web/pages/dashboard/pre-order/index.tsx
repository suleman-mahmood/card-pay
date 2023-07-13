import type { NextPage } from 'next';
import { useEffect, useState } from 'react';
import BackButton from '../../../components/buttons/BackButton';
import ErrorAlert from '../../../components/cards/ErrorAlert';
import DashboardLayout from '../../../components/layouts/DashboardLayout';
import BoxLoading from '../../../components/loaders/BoxLoading';
import JJKitchenImage from '../../../assets/jj-kitchen.jpg';
import BunkersImage from '../../../assets/Bunkers.jpeg';
import FrootiImage from '../../../assets/frooti.jpg';
import DelishImage from '../../../assets/Delish.jpeg';
import BaradariImage from '../../../assets/Baradari1.jpeg';
import ChopChopImage from '../../../assets/ChopChop.jpeg';
import JuiceZoneImage from '../../../assets/JuiceZone.jpeg';
import RestaurantCard from '../../../components/cards/RestaurantCard';
import { doc, getDoc } from 'firebase/firestore';
import { db } from '../../../services/initialize-firebase';
import { StaticImageData } from 'next/image';

interface RestaurantList {
	restaurant_list: Array<{ id: string; name: string; description: string }>;
}

const imagesMap = new Map<string, StaticImageData>([
	['kJsH8JZUXWM8inVd4K3rl2BMzZ32', BunkersImage],
	['x9YRwWaAjEhGaqqFrK8UN5ulfWJ3', DelishImage],
	['g6lwpLs9e5PkLGksluN8GMk3GLg2', ChopChopImage],
	['7h2Oo2aLVBgcYF9u4PIsGZZkLYB2', JuiceZoneImage],
	['2V2NmkCJyMd9AtQYg6q4ES51q1o1', FrootiImage],
	['2BTm3kcTW6ar1WfVAWoUysHuAkn2', BaradariImage]
]);

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
						name!='Baradari' ? (
							<div className='mb-4' key={id}>
								<RestaurantCard
									key={id}
									id={id}
									bgImage={
										imagesMap.get(id) !== undefined
											? imagesMap.get(id)!
											: JJKitchenImage
									}
									title={name}
									description={description}
								/>
							</div>
						) : null
					)
				)}
			</div>
		</DashboardLayout>
	);
};

export default DigitalCard;
