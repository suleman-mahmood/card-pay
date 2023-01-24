import { FirebaseError } from 'firebase/app';
import { httpsCallable } from 'firebase/functions';
import type { NextPage } from 'next';
import { useRouter } from 'next/router';
import { useEffect, useState } from 'react';
import ButtonPrimary from '../../components/buttons/ButtonPrimary';
import TextField from '../../components/inputs/TextField';
import AuthLayout from '../../components/layouts/AuthLayout';
import { auth, functions } from '../../services/initialize-firebase';

const Login: NextPage = () => {
	const router = useRouter();

	const [otp, setOtp] = useState('');

	const verifyEmail = async () => {
		try {
			const verifyEmailOtp = httpsCallable(functions, 'verifyEmailOtp');
			await verifyEmailOtp({
				otp: otp.trim(),
			});

			// on success
			// setIsLoading(false);
			// setErrorMessage('');
			await auth.signOut();
			router.push('/auth/login');
		} catch (error) {
			// setIsLoading(false);
			// setErrorMessage((error as FirebaseError).message);
			console.log((error as FirebaseError).message);
			console.log(error);
		}
	};

	const resendEmail = async () => {
		const resendOtpEmail = httpsCallable(functions, 'resendOtpEmail');
		await resendOtpEmail();
	};

	return (
		<AuthLayout>
			<h1 className='text-2xl'>4-digit OTP sent on email</h1>
			<h2 className='text-xl'>Enter it below</h2>
			<button className='mb-4 text-blue-500' onClick={resendEmail}>
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
		</AuthLayout>
	);
};

export default Login;
