import type { NextPage } from 'next';
import { useRouter } from 'next/router';
import { useEffect, useState } from 'react';
import ButtonPrimary from '../../components/buttons/ButtonPrimary';
import TextField from '../../components/inputs/TextField';
import AuthLayout from '../../components/layouts/AuthLayout';
import { auth } from '../../services/initialize-firebase';

const Deposit: NextPage = () => {
	const router = useRouter();

	const [amount, setAmount] = useState(0);

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

	const redirectToDashboard = () => {
		router.push('/dashboard');
	};

	return (
		<AuthLayout>
			<h1 className="text-2xl">Deposit</h1>
			<h2 className="mb-4 text-xl">Deposit funds in your student card</h2>

			<TextField
				type="number"
				valueSetter={setAmount}
				placeholder="Amount"
			/>

			<ButtonPrimary onClick={redirectToDashboard} text="Deposit Now!" />
		</AuthLayout>
	);
};

export default Deposit;
