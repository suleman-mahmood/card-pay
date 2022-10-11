import type { NextPage } from 'next';
import { useRouter } from 'next/router';
import ButtonPrimary from '../../components/buttons/ButtonPrimary';
import TransactionCard from '../../components/cards/TransactionCard';
import DashboardLayout from '../../components/layouts/DashboardLayout';
import { auth } from '../../services/initialize-firebase';

const Transactions: NextPage = () => {
	const router = useRouter();

	const redirectToDeposit = () => {
		router.push('/dashboard/deposit');
	};

	const redirectToLogin = async () => {
		await auth.signOut();
		router.push('/auth/login');
	};

	return (
		<DashboardLayout>
			<h1 className="text-2xl mb-4">Transactions</h1>

			<TransactionCard />
		</DashboardLayout>
	);
};

export default Transactions;
