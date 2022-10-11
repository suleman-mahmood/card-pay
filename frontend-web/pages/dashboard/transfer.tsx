import type { NextPage } from 'next';
import { useRouter } from 'next/router';
import { useEffect, useState } from 'react';
import ButtonPrimary from '../../components/buttons/ButtonPrimary';
import TextField from '../../components/inputs/TextField';
import DashboardLayout from '../../components/layouts/DashboardLayout';
import { auth } from '../../services/initialize-firebase';

const Transfer: NextPage = () => {
	const router = useRouter();

	const [rollNumber, setRollNumber] = useState('');
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
		<DashboardLayout>
			<h1 className="text-2xl">Transfer</h1>
			<h2 className="mb-4 text-xl">Peer to Peer funds transfer</h2>

			<TextField
				type="text"
				valueSetter={setRollNumber}
				maxLength={8}
				placeholder="Roll Number"
			/>
			<TextField
				type="number"
				valueSetter={setAmount}
				placeholder="Amount"
			/>

			<ButtonPrimary onClick={redirectToDashboard} text="Transfer Now!" />
		</DashboardLayout>
	);
};

export default Transfer;
