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
	const [errorMessage, setErrorMessage] = useState('');
	const [successMessage, setSuccessMessage] = useState('');
	const [isLoading, setIsLoading] = useState(false);

	const [name, setName] = useState<string>('');
	const [email, setEmail] = useState<string>('');
	const [password, setPassword] = useState<string>('');

	const handleSubmit = async () => {
		if (name.length === 0) {
			setErrorMessage('Enter name please');
			return;
		} else if (email.length === 0) {
			setErrorMessage('Enter email please');
			return;
		} else if (password.length === 0) {
			setErrorMessage('Enter password please');
			return;
		}

		setIsLoading(true);
		setErrorMessage('');
		setSuccessMessage('');

		const makeVendorAccount = httpsCallable(functions, 'makeVendorAccount');
		try {
			await makeVendorAccount({
				email: email,
				password: password,
				name: name,
			});

			setIsLoading(false);
			setErrorMessage('');
			setSuccessMessage('Changed pin!');
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
			<h1 className='mb-4 text-2xl'>Make Vendor Account</h1>

			<TextField
				type='text'
				valueSetter={setName}
				placeholder='Full Name'
				maxLength={4}
			/>

			<TextField
				type='text'
				valueSetter={setEmail}
				placeholder='Email'
				maxLength={4}
			/>

			<TextField
				type='text'
				valueSetter={setPassword}
				placeholder='Password'
				maxLength={4}
			/>

			<ButtonPrimary onClick={handleSubmit} text='Make!' />

			<ErrorAlert message={errorMessage} />
			<SuccessAlert message={successMessage} />

			<BackButton to='/dashboard' />
		</DashboardLayout>
	);
};

export default Deposit;
