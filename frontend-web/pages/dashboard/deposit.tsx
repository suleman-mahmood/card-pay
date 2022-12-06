import { FirebaseError } from 'firebase/app';
import { httpsCallable } from 'firebase/functions';
import type { NextPage } from 'next';
import { useState } from 'react';
import { useSelector } from 'react-redux';
import BackButton from '../../components/buttons/BackButton';
import ButtonPrimary from '../../components/buttons/ButtonPrimary';
import ErrorAlert from '../../components/cards/ErrorAlert';
import TextField from '../../components/inputs/TextField';
import DashboardLayout from '../../components/layouts/DashboardLayout';
import BoxLoading from '../../components/loaders/BoxLoading';
import { functions } from '../../services/initialize-firebase';
import { selectUser } from '../../store/store';

const DEPOSIT_AMOUNTS = [
	[10, 50, 100],
	[500, 1000, 5000],
];

const Deposit: NextPage = () => {
	const [amount, setAmount] = useState(0);
	const { userState } = useSelector(selectUser);

	const [errorMessage, setErrorMessage] = useState('');
	const [isLoading, setIsLoading] = useState(false);

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
			<h1 className='text-2xl'>Deposit</h1>
			<h2 className='mb-4 text-xl'>Deposit funds in your student card</h2>

			{DEPOSIT_AMOUNTS.map((row, i) => {
				return (
					<div key={i} className='flex flex-row justify-around mb-4'>
						{row.map((n, j) => {
							return (
								<button
									key={j + (i + 1) * 1000}
									className='btn btn-outline btn-primary'
									onClick={() => setAmount(n)}
								>
									{n}
								</button>
							);
						})}
					</div>
				);
			})}

			<h2 className='text-lg'>Or enter a custom amount:</h2>

			<TextField
				type='number'
				valueSetter={setAmount}
				placeholder='Amount'
				value={amount}
			/>

			<ButtonPrimary onClick={handleDeposit} text='Deposit Now!' />

			<ErrorAlert message={errorMessage} />

			<BackButton />
		</DashboardLayout>
	);
};

export default Deposit;
