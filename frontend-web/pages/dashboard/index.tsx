import type { NextPage } from 'next';
import { useRouter } from 'next/router';
import { useEffect } from 'react';
import ButtonPrimary from '../../components/buttons/ButtonPrimary';
import DashboardLayout from '../../components/layouts/DashboardLayout';
import { auth } from '../../services/initialize-firebase';

const Dashboard: NextPage = () => {
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

	const redirectToDeposit = () => {
		router.push('/dashboard/deposit');
	};

	return (
		<DashboardLayout>
			<div className="flex flex-col">
				<div className="flex flex-row justify-center">
					<ButtonPrimary text="Deposit" onClick={redirectToDeposit} />
				</div>
			</div>
		</DashboardLayout>
	);
};

export default Dashboard;
