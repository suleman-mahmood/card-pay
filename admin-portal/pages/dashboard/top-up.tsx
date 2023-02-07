import { FirebaseError } from 'firebase/app';
import { httpsCallable } from 'firebase/functions';
import type { NextPage } from 'next';
import { useState } from 'react';
import BackButton from '../../components/buttons/BackButton';
import ButtonPrimary from '../../components/buttons/ButtonPrimary';
import ErrorAlert from '../../components/cards/ErrorAlert';
import SuccessAlert from '../../components/cards/SuccessAlert';
import TextField from '../../components/inputs/TextField';
import DashboardLayout from '../../components/layouts/DashboardLayout';
import BoxLoading from '../../components/loaders/BoxLoading';
import { functions } from '../../services/initialize-firebase';

const Deposit: NextPage = () => {
	const [errorMessage, setErrorMessage] = useState('');
	const [successMessage, setSuccessMessage] = useState('');
	const [isLoading, setIsLoading] = useState(false);

	const [amount, setAmount] = useState(0);
	const [rollNumber, setRollNumber] = useState('');

	const handleSubmit = async () => {
		if (rollNumber.length === 0) {
			setErrorMessage('Enter name please');
			return;
		} else if (amount <= 0) {
			setErrorMessage('Enter amount above 0');
			return;
		}

		setIsLoading(true);
		setErrorMessage('');
		setSuccessMessage('');

		const topUpUserVirtualCash = httpsCallable(
			functions,
			'topUpUserVirtualCash'
		);
		try {
			await topUpUserVirtualCash({
				rollNumber: rollNumber,
				amount: amount,
			});

			setIsLoading(false);
			setErrorMessage('');
			setSuccessMessage('Top up successful!');
		} catch (error) {
			setIsLoading(false);
			setErrorMessage((error as FirebaseError).message);
			setSuccessMessage('');
		}
	};

	return isLoading ? (
		<BoxLoading />
	) : (
		<DashboardLayout>
			<h1 className='mb-4 text-2xl'>Top Up any account</h1>

			<TextField
				type='text'
				valueSetter={setRollNumber}
				placeholder='Roll Number'
				maxLength={8}
			/>

			<TextField
				type='number'
				valueSetter={setAmount}
				placeholder='Amount'
			/>

			<ButtonPrimary onClick={handleSubmit} text='Top Up!' />

			<ErrorAlert message={errorMessage} />
			<SuccessAlert message={successMessage} />

			<BackButton to='/dashboard' />
		</DashboardLayout>
	);
};

export default Deposit;
