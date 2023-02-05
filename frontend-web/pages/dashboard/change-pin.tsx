import { FirebaseError } from 'firebase/app';
import { httpsCallable } from 'firebase/functions';
import type { NextPage } from 'next';
import Link from 'next/link';
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
	const [oldPin, setOldPin] = useState('');
	const [pin, setPin] = useState('');
	const [confirmPin, setConfirmPin] = useState('');

	const [errorMessage, setErrorMessage] = useState('');
	const [successMessage, setSuccessMessage] = useState('');
	const [isLoading, setIsLoading] = useState(false);

	const handleChangePin = async () => {
		const regex = /^[0-9]{4}$/g; // Matches 4 digits only 0-9

		if (pin !== confirmPin) {
			setErrorMessage("Pins don't match");
			return;
		} else if (pin.match(regex) === null) {
			setErrorMessage('Pin must contain only numbers 0-9');
			return;
		} else if (pin.length !== 4) {
			setErrorMessage('Pin must be 4-digits long');
			return;
		}

		setIsLoading(true);
		setErrorMessage('');
		setSuccessMessage('');

		const changeUserPin = httpsCallable(functions, 'changeUserPin');
		try {
			await changeUserPin({
				pin: pin,
				oldPin: oldPin,
			});

			setIsLoading(false);
			setErrorMessage('');
			setSuccessMessage('Changed pin!');
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
			<h1 className='text-2xl'>Change Pin</h1>
			<h2 className='text-xl'>Change your transaction pin</h2>

			<div className='my-2 mr-4 label-text-alt link link-hover text-right text-blue-500'>
				<Link href='/dashboard/forgot-pin'>Forgot pin?</Link>
			</div>

			<TextField
				type='text'
				valueSetter={setOldPin}
				placeholder='Old pin'
				maxLength={4}
			/>

			<TextField
				type='text'
				valueSetter={setPin}
				placeholder='New pin'
				maxLength={4}
			/>

			<TextField
				type='text'
				valueSetter={setConfirmPin}
				placeholder='Confirm new pin'
				maxLength={4}
			/>

			<ButtonPrimary onClick={handleChangePin} text='Change pin' />

			<ErrorAlert message={errorMessage} />
			<SuccessAlert message={successMessage} />

			<BackButton />
		</DashboardLayout>
	);
};

export default Deposit;
