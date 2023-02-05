import { FirebaseError } from 'firebase/app';
import { httpsCallable } from 'firebase/functions';
import type { NextPage } from 'next';
import { useRouter } from 'next/router';
import { useState } from 'react';
import ButtonPrimary from '../../components/buttons/ButtonPrimary';
import ErrorAlert from '../../components/cards/ErrorAlert';
import TextField from '../../components/inputs/TextField';
import AuthLayout from '../../components/layouts/AuthLayout';
import BoxLoading from '../../components/loaders/BoxLoading';
import { functions } from '../../services/initialize-firebase';

const Login: NextPage = () => {
	const router = useRouter();

	const [errorMessage, setErrorMessage] = useState('');
	const [isLoading, setIsLoading] = useState(false);

	const [password, setPassword] = useState('');
	const [confirmPassword, setConfirmPassword] = useState('');
	const [otp, setOtp] = useState('');

	const changePassword = async (e: React.FormEvent) => {
		e.preventDefault();

		if (password !== confirmPassword) {
			setErrorMessage("Passwords don't match");
			return;
		}

		try {
			setIsLoading(true);

			const verifyForgotPasswordOtp = httpsCallable(
				functions,
				'verifyForgotPasswordOtp'
			);
			await verifyForgotPasswordOtp({
				rollNumber: router.query.rollNumber,
				password: password,
				otp: otp.trim(),
			});

			// on success
			setIsLoading(false);
			setErrorMessage('');
			router.push('/auth/login');
		} catch (error) {
			setIsLoading(false);
			setErrorMessage((error as FirebaseError).message);
		}
	};

	return isLoading ? (
		<BoxLoading />
	) : (
		<AuthLayout>
			<h1 className='text-2xl'>4-digit OTP sent on email</h1>
			<h2 className='text-xl'>Enter it below</h2>

			<form onSubmit={changePassword} className='form-control w-full'>
				<TextField
					type={'text'}
					valueSetter={setOtp}
					maxLength={4}
					placeholder='4-digit OTP'
				/>

				<TextField
					type='password'
					valueSetter={setPassword}
					placeholder='Password'
				/>
				<TextField
					type='password'
					valueSetter={setConfirmPassword}
					placeholder='Confirm Password'
				/>

				<ButtonPrimary
					type='submit'
					onClick={changePassword}
					text='Change password!'
				/>
			</form>

			<ErrorAlert message={errorMessage} />
		</AuthLayout>
	);
};

export default Login;
