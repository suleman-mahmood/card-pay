import { FirebaseError } from 'firebase/app';
import { httpsCallable } from 'firebase/functions';
import type { NextPage } from 'next';
import { useRouter } from 'next/router';
import { useEffect, useState } from 'react';
import ButtonPrimary from '../../components/buttons/ButtonPrimary';
import ErrorAlert from '../../components/cards/ErrorAlert';
import TextField from '../../components/inputs/TextField';
import AuthLayout from '../../components/layouts/AuthLayout';
import BoxLoading from '../../components/loaders/BoxLoading';
import { auth, functions } from '../../services/initialize-firebase';

const Login: NextPage = () => {
	const router = useRouter();

	const [otp, setOtp] = useState('');

	const [isLoading, setIsLoading] = useState(false);
	const [errorMessage, setErrorMessage] = useState('');

	const verifyEmail = async (e: React.FormEvent) => {
		e.preventDefault();
		setIsLoading(true);

		try {
			const verifyEmailOtp = httpsCallable(functions, 'verifyEmailOtp');
			await verifyEmailOtp({
				otp: otp.trim(),
				uid: router.query.uid,
			});

			// on success
			setIsLoading(false);
			setErrorMessage('');
			await auth.signOut();
			router.push('/auth/login');
		} catch (error) {
			setIsLoading(false);
			setErrorMessage((error as FirebaseError).message);
			console.log((error as FirebaseError).message);
		}
	};

	const resendEmail = async () => {
		const resendOtpEmail = httpsCallable(functions, 'resendOtpEmail');
		await resendOtpEmail({
			uid: router.query.uid,
		});
	};

	return isLoading ? (
		<BoxLoading />
	) : (
		<AuthLayout>
			<h1 className='text-2xl'>4-digit OTP sent on email</h1>
			<h2 className='text-xl'>Enter it below</h2>
			<button
				className='btn btn-outline btn-success mb-3 mt-1 rounded-full'
				onClick={resendEmail}
			>
				Resend email
			</button>

			<form onSubmit={verifyEmail} className='form-control w-full'>
				<TextField
					type={'text'}
					valueSetter={setOtp}
					maxLength={4}
					placeholder='4-digit OTP'
				/>

				<ButtonPrimary
					type='submit'
					onClick={verifyEmail}
					text='Verify your email!'
				/>
			</form>

			<ErrorAlert message={errorMessage} />
		</AuthLayout>
	);
};

export default Login;
