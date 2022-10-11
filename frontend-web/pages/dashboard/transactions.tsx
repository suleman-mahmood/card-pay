import type { NextPage } from 'next';
import { useRouter } from 'next/router';
import { useEffect } from 'react';
import ButtonPrimary from '../../components/buttons/ButtonPrimary';
import TransactionCard from '../../components/cards/TransactionCard';
import DashboardLayout from '../../components/layouts/DashboardLayout';
import { auth } from '../../services/initialize-firebase';

const Transactions: NextPage = () => {
	const router = useRouter();

	useEffect(() => {
		return auth.onAuthStateChanged(user => {
			if (user) {
				if (!user.emailVerified) {
					router.push('/auth/student-verification');
				}
			} else {
				router.push('/');
			}
		});
	}, []);

	return (
		<DashboardLayout>
			<h1 className="text-2xl mb-4">Transactions</h1>

			<TransactionCard />
		</DashboardLayout>
	);
};

export default Transactions;
