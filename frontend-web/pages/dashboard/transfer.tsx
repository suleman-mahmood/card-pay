import type { NextPage } from 'next';
import { useRouter } from 'next/router';
import ButtonPrimary from '../../components/buttons/ButtonPrimary';
import TextField from '../../components/inputs/TextField';
import DashboardLayout from '../../components/layouts/DashboardLayout';

const Transfer: NextPage = () => {
	const router = useRouter();

	const redirectToDashboard = () => {
		router.push('/dashboard');
	};

	return (
		<DashboardLayout>
			<h1 className="text-2xl">Transfer</h1>
			<h2 className="mb-4 text-xl">Peer to Peer funds transfer</h2>

			<TextField placeholder="Roll Number" />
			<TextField placeholder="Amount" />

			<ButtonPrimary onClick={redirectToDashboard} text="Transfer Now!" />
		</DashboardLayout>
	);
};

export default Transfer;
