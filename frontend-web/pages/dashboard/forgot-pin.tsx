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

	return isLoading ? (
		<BoxLoading />
	) : (
		<DashboardLayout>
			<h1 className='text-2xl mb-2'>Forgot Pin?</h1>

			<p className='text-xl'>
				Send a selfie with your student card to the following email
				address: <b>cardpayteam@gmail.com</b>
			</p>

			<ErrorAlert message={errorMessage} />
			<SuccessAlert message={successMessage} />

			<BackButton />
		</DashboardLayout>
	);
};

export default Deposit;
