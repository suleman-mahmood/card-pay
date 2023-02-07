import { onAuthStateChanged } from 'firebase/auth';
import { collection, getDocs, query, where } from 'firebase/firestore';
import type { NextPage } from 'next';
import { useRouter } from 'next/router';
import { useEffect, useState } from 'react';
import DashboardLayout from '../../components/layouts/DashboardLayout';
import BoxLoading from '../../components/loaders/BoxLoading';
import { auth, db } from '../../services/initialize-firebase';

const ADMIN_UID = 'JoNhydNzAWXGilGS4fRsOK1ePTm2';

const Dashboard: NextPage = () => {
	const router = useRouter();

	const [isLoading, setIsLoading] = useState(false);

	useEffect(() => {}, []);

	const redirectToMakeVendorAccount = () => {
		router.push('/dashboard/make-vendor-account');
	};

	const redirectToTopUp = () => {
		router.push('/dashboard/top-up');
	};

	return isLoading ? (
		<BoxLoading />
	) : (
		<DashboardLayout>
			<h1 className='text-2xl'>Dashboard</h1>
			<div className='flex flex-col'>
				<div className='flex flex-row justify-around'>
					<div className='flex flex-col'>
						<button onClick={redirectToMakeVendorAccount}>
							<div className='w-24 shadow-md p-3 rounded-2xl'>
								{/* <Image src={DepositIcon} alt='' /> */}
								<img src='https://i.ibb.co/5RYhN9P/Digi.png' />
							</div>
						</button>
						<h3 className='text-lg mt-1'>Make Vendor</h3>
					</div>

					<div className='flex flex-col'>
						<button onClick={redirectToTopUp}>
							<div className='w-24 shadow-md p-4 rounded-2xl'>
								{/* <Image src={ChangePinIcon} alt='' /> */}
								<img src='https://i.ibb.co/5RYhN9P/Digi.png' />
							</div>
						</button>
						<h3 className='text-lg'>Top Up</h3>
					</div>
				</div>
			</div>
		</DashboardLayout>
	);
};

export default Dashboard;
