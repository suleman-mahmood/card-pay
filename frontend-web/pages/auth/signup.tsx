import { FirebaseError } from 'firebase/app';
import {
	createUserWithEmailAndPassword,
	sendEmailVerification,
} from 'firebase/auth';
import { httpsCallable } from 'firebase/functions';
import type { NextPage } from 'next';
import { useRouter } from 'next/router';
import { useState } from 'react';
import ButtonPrimary from '../../components/buttons/ButtonPrimary';
import ErrorAlert from '../../components/cards/ErrorAlert';
import PhoneField from '../../components/inputs/PhoneField';
import TextField from '../../components/inputs/TextField';
import AuthLayout from '../../components/layouts/AuthLayout';
import { auth, functions } from '../../services/initialize-firebase';

const Signup: NextPage = () => {
	const router = useRouter();

	const [errorMessage, setErrorMessage] = useState('');
	const [isLoading, setIsLoading] = useState(false);

	const [fullName, setFullName] = useState('');
	const [rollNumber, setRollNumber] = useState('');
	const [password, setPassword] = useState('');
	const [confirmPassword, setConfirmPassword] = useState('');
	const [pin, setPin] = useState('');
	const [confirmPin, setConfirmPin] = useState('');
	const [phoneNumber, setPhoneNumber] = useState('');

	const redirectToLogin = () => {
		router.push('/auth/login');
	};

	const signupUser = async (e: React.FormEvent) => {
		e.preventDefault();

		if (password !== confirmPassword) {
			console.log("Passwords don't match");
			setErrorMessage("Passwords don't match");
			return;
		} else if (pin != confirmPin) {
			console.log("Pins don't match");
			setErrorMessage("Pins don't match");
			return;
		} else if (rollNumber.length !== 8) {
			console.log('Roll number must be 8 digits');
			setErrorMessage('Roll number must be 8 digits');
			return;
		} else if (phoneNumber.length !== 10) {
			console.log('Phone number must be 10 digits');
			setErrorMessage('Phone number must be 10 digits');
			return;
		}

		setIsLoading(true);
		setErrorMessage('');

		const email = `${rollNumber}@lums.edu.pk`;

		try {
			const { user } = await createUserWithEmailAndPassword(
				auth,
				email,
				password
			);

			const createUser = httpsCallable(functions, 'createUser');
			await createUser({
				fullName: fullName.trim(),
				rollNumber: rollNumber,
				pin: pin,
				role: 'student',
				phoneNumber: phoneNumber,
			});

			setIsLoading(false);
			setErrorMessage('');
			router.push('/auth/student-verification');
		} catch (error) {
			setIsLoading(false);
			setErrorMessage((error as FirebaseError).message);
			console.log(error);
		}
	};

	return (
		<AuthLayout>
			<h1 className='text-2xl'>Create your account</h1>
			<h2 className='mb-4 text-sm'>
				Do you already have an account?
				<a
					className='ml-2 text-blue-500 text-xl'
					onClick={redirectToLogin}
				>
					Sign In Now
				</a>
			</h2>

			<form onSubmit={signupUser} className='form-control w-full'>
				<TextField
					type='text'
					valueSetter={setFullName}
					placeholder='Full Name'
				/>
				<TextField
					type='text'
					valueSetter={setRollNumber}
					maxLength={8}
					placeholder='Roll Number'
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
				<TextField
					type={'text'}
					valueSetter={setPin}
					maxLength={4}
					placeholder='4-digit pin'
				/>
				<TextField
					type={'text'}
					valueSetter={setConfirmPin}
					maxLength={4}
					placeholder='Confirm 4-digit pin'
				/>
				<PhoneField valueSetter={setPhoneNumber} />

				<div className='h-6'></div>

				<ButtonPrimary
					type='submit'
					onClick={signupUser}
					text='Sign Up'
				/>
			</form>

			<ErrorAlert message={errorMessage} />
		</AuthLayout>
	);
};

export default Signup;
