import { FirebaseError } from 'firebase/app';
import { httpsCallable } from 'firebase/functions';
import type { NextPage } from 'next';
import { useRouter } from 'next/router';
import { useState } from 'react';
import ErrorAlert from '../../components/cards/ErrorAlert';
import PhoneField from '../../components/inputs/PhoneField';
import TextField from '../../components/inputs/signup_text_field';
import WelcomeLayout from '../../components/layouts/WelcomeLayout';
import BoxLoading from '../../components/loaders/BoxLoading';
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
	const [referralRollNumber, setReferralRollNumber] = useState('');

	const redirectToLogin = () => {
		router.push('/auth/login');
	};

	const signupUser = async (e: React.FormEvent) => {
		e.preventDefault();
		const words = fullName.split(' ');

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
		} else if (words.length < 2) {
			console.log('Enter first and last name');
			setErrorMessage('Enter first and last name');
			return;
		}

		setIsLoading(true);
		setErrorMessage('');

		try {
			const createUser = httpsCallable(functions, 'createUser');
			const res = await createUser({
				fullName: fullName.trim(),
				rollNumber: rollNumber,
				password: password,
				pin: pin,
				phoneNumber: phoneNumber,
				referralRollNumber: referralRollNumber,
			});
			const uid: string = res.data as string;

			setIsLoading(false);
			setErrorMessage('');

			router.push({
				pathname: '/auth/student-verification',
				query: {
					uid: uid,
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
		<WelcomeLayout>
			<h1 className='text-2xl'>Create your account</h1>
			<h2 className='mb-4 text-sm'>
				Do you already have an account?
				<a
					className='ml-2 text-blue-50 text-xl'
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
					value={fullName}
				/>
				<TextField
					type='text'
					valueSetter={setRollNumber}
					maxLength={8}
					placeholder='Roll Number: 23xxxxxx'
					value={rollNumber}
				/>
				<TextField
					type='password'
					valueSetter={setPassword}
					placeholder='Password'
					value={password}
				/>
				<TextField
					type='password'
					valueSetter={setConfirmPassword}
					placeholder='Confirm Password'
					value={confirmPassword}
				/>
				<TextField
					type={'text'}
					valueSetter={setPin}
					maxLength={4}
					placeholder='4-digit pin'
					value={pin}
				/>
				<TextField
					type={'text'}
					valueSetter={setConfirmPin}
					maxLength={4}
					placeholder='Confirm 4-digit pin'
					value={confirmPin}
				/>
				<PhoneField valueSetter={setPhoneNumber} value={phoneNumber} />

				<h1 className='mt-4 pl-1 text-left text-gray-300'>Optional:</h1>
				<TextField
					type='text'
					valueSetter={setReferralRollNumber}
					maxLength={8}
					placeholder='Referral Roll Number: 2xxxxxxx'
					value={referralRollNumber}
				/>

				<div className='h-6'></div>

				<button
					disabled={isLoading}
					className='bg-white shadow-xl rounded-full text-primarydark py-2 text-xl font-semibold active:bg-primarydark active:text-white'
					onClick={signupUser}
				>
					Sign Up{' '}
				</button>
			</form>

			<ErrorAlert message={errorMessage} />
		</WelcomeLayout>
	);
};

export default Signup;
