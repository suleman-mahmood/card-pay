import type { NextPage } from 'next';
import { useRouter } from 'next/router';
import ButtonPrimary from '../../components/buttons/ButtonPrimary';
import DashboardLayout from '../../components/layouts/DashboardLayout';

const Dashboard: NextPage = () => {
	const router = useRouter();

	const redirectToDeposit = () => {
		router.push('/dashboard/deposit');
	};

	const redirectToChangePin = () => {
		router.push('/dashboard/change-pin');
	};

	return (
		<DashboardLayout>
			<div className="flex flex-col">
				<div className="flex flex-row justify-center">
					<ButtonPrimary text="Deposit" onClick={redirectToDeposit} />
					<div className='w-4'></div>
					<ButtonPrimary text="Change Pin" onClick={redirectToChangePin} />
				</div>
			</div>
		</DashboardLayout>
	);
};

export default Dashboard;
