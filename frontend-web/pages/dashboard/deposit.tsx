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

const Deposit: NextPage = () => {
	const router = useRouter();

	const [amount, setAmount] = useState(0);
	const { userState } = useSelector(selectUser);

	const [errorMessage, setErrorMessage] = useState('');
	const [isLoading, setIsLoading] = useState(false);

	const redirectToDashboard = () => {
		router.push('/dashboard');
	};

	const handleDeposit = async () => {
		if (amount <= 0) {
			setErrorMessage('Please enter an amount greater than 0');
			return;
		} else if (userState.id === '') {
			setErrorMessage('Please refresh the page');
			return;
		}

		setIsLoading(true);
		setErrorMessage('');

		const addDepositRequest = httpsCallable(functions, 'addDepositRequest');
		try {
			const { data } = await addDepositRequest({
				amount: amount,
				fullName: userState.fullName,
				email: userState.email,
			});

			setIsLoading(false);
			setErrorMessage('');

			const url = (data as any).paymentUrl;
			window.location.href = url;

			// Don't use, browsers disables pop-ups
			// window.open(url, '_blank');
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
			<h1 className="text-2xl">Deposit</h1>
			<h2 className="mb-4 text-xl">Deposit funds in your student card</h2>

			<TextField
				type="number"
				valueSetter={setAmount}
				placeholder="Amount"
			/>

			<ButtonPrimary onClick={handleDeposit} text="Deposit Now!" />

			<ErrorAlert message={errorMessage} />

			<div className="btn-group grid grid-cols-2 absolute top-6 left-6">
				<button
					className="btn btn-outline"
					onClick={redirectToDashboard}
				>
					Back
				</button>
			</div>
		</DashboardLayout>
	);
};

export default Deposit;
