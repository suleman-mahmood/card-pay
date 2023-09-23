import { FirebaseError } from 'firebase/app';
import { httpsCallable } from 'firebase/functions';
import type { NextPage } from 'next';
import { useRouter } from 'next/router';
import { useState } from 'react';
import BackButton from '../../components/buttons/BackButton';
import ButtonPrimary from '../../components/buttons/ButtonPrimary';
import ErrorAlert from '../../components/cards/ErrorAlert';
import TextField from '../../components/inputs/TextField';
import AuthLayout from '../../components/layouts/AuthLayout';
import BoxLoading from '../../components/loaders/BoxLoading';
import { functions } from '../../services/initialize-firebase';

const Login: NextPage = () => {
	const router = useRouter();

	const [rollNumber, setRollNumber] = useState('');

	const [errorMessage, setErrorMessage] = useState('');
	const [isLoading, setIsLoading] = useState(false);

	const handleSubmit = async (e: React.FormEvent) => {
		e.preventDefault();
		setIsLoading(true);
		setErrorMessage('');

		try {
			const sendForgotPasswordEmail = httpsCallable(
				functions,
				'sendForgotPasswordEmail'
			);
			await sendForgotPasswordEmail({
				rollNumber: rollNumber,
			});

			setIsLoading(false);
			setErrorMessage('');
			router.push({
				pathname: '/auth/change-password',
				query: {
					rollNumber: rollNumber,
				},
			});
		} catch (error) {
			setIsLoading(false);
			setErrorMessage((error as FirebaseError).message);
			console.log(error);
		}
	};

	return isLoading ? (
		<BoxLoading />
	) : (
		<AuthLayout>
			<h1 className='text-2xl'>Password Reset</h1>
			<h1 className='text-xl my-4'>
				A password reset email will be send to your outlook
			</h1>

			<form onSubmit={handleSubmit} className='w-full form-control'>
				<TextField
					type='text'
					valueSetter={setRollNumber}
					placeholder='Roll Number'
					maxLength={8}
				/>

				<div className='h-2'></div>

				<ButtonPrimary
					type={'submit'}
					onClick={handleSubmit}
					text='Send'
				/>
			</form>

			<BackButton textColor='text-black' />
			<ErrorAlert message={errorMessage} />
		</AuthLayout>
	);
};

export default Login;
