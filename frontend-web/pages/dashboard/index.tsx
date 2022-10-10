import type { NextPage } from 'next';
import Router from 'next/router';
import ButtonPrimary from '../../components/buttons/ButtonPrimary';
import DashboardLayout from '../../components/layouts/DashboardLayout';
import { auth } from '../../services/initialize-firebase';

const Dashboard: NextPage = () => {
	const router = Router;
	
	const redirectToDeposit = () => {
		router.push('/dashboard/deposit');
	};

	const redirectToLogin = async () => {
		await auth.signOut();
		router.push('/auth/login');
	};

	return (
		<DashboardLayout>
			<div className='flex flex-col'>
				<div className='flex flex-row justify-center'>
					<ButtonPrimary text='Deposit' onClick={redirectToDeposit}/>
					<div className='w-4'></div>
					<ButtonPrimary text='Logout' onClick={redirectToLogin}/>
				</div>
			</div>
		</DashboardLayout>
	);
};

export default Dashboard;
