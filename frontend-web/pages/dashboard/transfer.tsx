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

const DEPOSIT_AMOUNTS = [
	[10, 50, 100],
	[500, 1000, 5000],
];

const Transfer: NextPage = () => {
	const router = useRouter();
	const { userState } = useSelector(selectUser);

	const [rollNumber, setRollNumber] = useState('');
	const [amount, setAmount] = useState(0);
	const [pin, setPin] = useState('');

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
		} else if (pin.length !== 4) {
			setErrorMessage('Please enter 4-digit pin');
			return;
		}

		setIsLoading(true);
		setErrorMessage('');

		const transfer = httpsCallable(functions, 'transfer');
		try {
			await transfer({
				amount: amount,
				recipientRollNumber: rollNumber,
				pin: pin,
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
			<h1 className='text-2xl'>Transfer</h1>
			<h2 className='mb-4 text-xl'>Peer to Peer funds transfer</h2>

			<TextField
				type='password'
				valueSetter={setPin}
				placeholder='Enter your pin'
				maxLength={4}
			/>

			<TextField
				type='text'
				valueSetter={setRollNumber}
				maxLength={8}
				placeholder='Roll Number'
			/>

			{DEPOSIT_AMOUNTS.map((row, i) => {
				return (
					<div key={i} className='flex flex-row justify-around mb-4 '>
						{row.map((n, j) => {
							return (
								<button
									key={j + (i + 1) * 1000}
									className='btn btn-primary shadow-xl text-white text-lg bg-primarydark focus:text-white focus:bg-primary focus:shadow-inner flex-1 mx-3 rounded-full border-none '
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
				value={amount.toString()}
			/>

			<ButtonPrimary onClick={handleTransfer} text='Transfer Now!' />

			<ErrorAlert message={errorMessage} />
		</DashboardLayout>
	);
};

export default Transfer;
