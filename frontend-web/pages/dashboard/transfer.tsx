import type { NextPage } from 'next';
import Router from 'next/router';
import ButtonPrimary from '../../components/buttons/ButtonPrimary';
import DashboardLayout from '../../components/layouts/DashboardLayout';
import { auth } from '../../services/initialize-firebase';

const Transfer: NextPage = () => {
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
			<h1>Transfer</h1>
		</DashboardLayout>
	);
};

export default Transfer;
