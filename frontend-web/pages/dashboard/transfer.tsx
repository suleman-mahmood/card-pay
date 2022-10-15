import { FirebaseError } from 'firebase/app';
import { httpsCallable } from 'firebase/functions';
import type { NextPage } from 'next';
import { useRouter } from 'next/router';
import { useState } from 'react';
import { useSelector } from 'react-redux';
import ButtonPrimary from '../../components/buttons/ButtonPrimary';
import ErrorAlert from '../../components/cards/ErrorAlert';
import TextField from '../../components/inputs/TextField';
import DashboardLayout from '../../components/layouts/DashboardLayout';
import BoxLoading from '../../components/loaders/BoxLoading';
import { functions } from '../../services/initialize-firebase';
import { selectUser } from '../../store/store';

const Transfer: NextPage = () => {
	const router = useRouter();

	const [rollNumber, setRollNumber] = useState('');
	const [amount, setAmount] = useState(0);
	const { userState } = useSelector(selectUser);

	const [errorMessage, setErrorMessage] = useState('');
	const [isLoading, setIsLoading] = useState(false);

	const handleTransfer = async () => {
		if (amount <= 0) {
			setErrorMessage('Please enter an amount greater than 0');
			return;
		} else if (rollNumber.length !== 8) {
			setErrorMessage('Please enter an 8-digit Roll Number');
			return;
		} else if (userState.id === '') {
			setErrorMessage('Please refresh the page');
			return;
		}

		setIsLoading(true);
		setErrorMessage('');

		const transfer = httpsCallable(functions, 'transfer');
		try {
			await transfer({
				amount: amount,
				recipientRollNumber: rollNumber,
			});

			setIsLoading(false);
			setErrorMessage('');

			router.push('/dashboard');
		} catch (error) {
			setIsLoading(false);
			setErrorMessage((error as FirebaseError).message);
			console.log(error);
		}
	};

	return isLoading ? (
		<BoxLoading />
	) : (
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

			<ButtonPrimary onClick={handleTransfer} text="Transfer Now!" />

			<ErrorAlert message={errorMessage} />
		</DashboardLayout>
	);
};

export default Transfer;
