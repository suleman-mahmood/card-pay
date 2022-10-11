import type { NextPage } from 'next';
import { useRouter } from 'next/router';
import ButtonPrimary from '../../components/buttons/ButtonPrimary';
import TextField from '../../components/inputs/TextField';
import AuthLayout from '../../components/layouts/AuthLayout';

const Deposit: NextPage = () => {
	const router = useRouter();

	const redirectToDashboard = () => {
		router.push('/dashboard');
	};

	return (
		<AuthLayout>
			<h1 className="text-2xl">Deposit</h1>
			<h2 className="mb-4 text-xl">Deposit funds in your student card</h2>

			<TextField placeholder="Password" />

			<ButtonPrimary onClick={redirectToDashboard} text="Deposit Now!" />
		</AuthLayout>
	);
};

export default Deposit;
