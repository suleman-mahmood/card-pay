import { FirebaseError } from 'firebase/app';
import { signInWithEmailAndPassword } from 'firebase/auth';
import type { NextPage } from 'next';
import { useRouter } from 'next/router';
import { useState } from 'react';
import ButtonPrimary from '../../components/buttons/ButtonPrimary';
import ErrorAlert from '../../components/cards/ErrorAlert';
import TextField from '../../components/inputs/TextField';
import AuthLayout from '../../components/layouts/AuthLayout';
import BoxLoading from '../../components/loaders/BoxLoading';
import { auth } from '../../services/initialize-firebase';

const Login: NextPage = () => {
	const router = useRouter();

	const [rollNumber, setRollNumber] = useState('');
	const [password, setPassword] = useState('');

	const [errorMessage, setErrorMessage] = useState('');
	const [isLoading, setIsLoading] = useState(false);

	const redirectToSignup = () => {
		router.push('/auth/signup');
	};

	const loginUser = async (e: React.FormEvent) => {
		e.preventDefault();
		setIsLoading(true);
		setErrorMessage('');

		const email = `${rollNumber}@lums.edu.pk`;

		try {
			await signInWithEmailAndPassword(auth, email, password);
			setIsLoading(false);
			setErrorMessage('');
			router.push('/dashboard/');
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
			<h1 className="text-2xl">Sign in to your account</h1>
			<h2 className="mb-4 text-xl">
				Don&apos;t have an account yet?
				<a
					className="ml-2 text-blue-500 text-xl"
					onClick={redirectToSignup}
				>
					Sign Up Now
				</a>
			</h2>

			<form onSubmit={loginUser} className="form-control w-full">
				<TextField
					type="text"
					valueSetter={setRollNumber}
					placeholder="Roll Number"
					maxLength={8}
				/>
				<TextField
					type="password"
					valueSetter={setPassword}
					placeholder="Password"
				/>

				<ButtonPrimary
					type={'submit'}
					onClick={loginUser}
					text="Log In"
				/>
			</form>

			<ErrorAlert message={errorMessage} />
		</AuthLayout>
	);
};

export default Login;
