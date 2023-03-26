import { FirebaseError } from 'firebase/app';
import { signInWithEmailAndPassword } from 'firebase/auth';
import type { NextPage } from 'next';
import Link from 'next/link';
import { useRouter } from 'next/router';
import { useState } from 'react';
import ButtonPrimary from '../../components/buttons/ButtonPrimary';
import ErrorAlert from '../../components/cards/ErrorAlert';
import TextField from '../../components/inputs/TextField';
import AuthLayout from '../../components/layouts/AuthLayout';
import BoxLoading from '../../components/loaders/BoxLoading';
import { auth } from '../../services/initialize-firebase';
import { faQuestionCircle } from '@fortawesome/free-solid-svg-icons';
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';
import ButtonSecondary from '../../components/buttons/ButtonSecondary';
import { faWhatsapp } from '@fortawesome/free-brands-svg-icons';
import { IconProp } from '@fortawesome/fontawesome-svg-core';

const whatsappUrl = 'https://wa.me/923322208287';

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
			<h1 className='text-2xl mb-2'>Sign in to your account</h1>
			<h2 className='mb-4 text-xs'>
				Don&apos;t have an account?
				<ButtonSecondary
					onClick={redirectToSignup}
					text={'Sign Up Now'}
					invertColors={false}
				/>
			</h2>

			<form onSubmit={loginUser} className='w-full form-control'>
				<TextField
					type='text'
					valueSetter={setRollNumber}
					placeholder='Roll Number'
					maxLength={8}
				/>
				<TextField
					type='password'
					valueSetter={setPassword}
					placeholder='Password'
				/>
				<div className='label-text-alt link link-hover text-right text-blue-500 mr-2'>
					<Link href='/auth/forgot-password'>Forgot password?</Link>
				</div>

				<div className='h-6'></div>

				<ButtonPrimary
					type={'submit'}
					onClick={loginUser}
					text='Sign In'
				/>
			</form>

			<a
				href={whatsappUrl}
				target='_blank'
				rel='noreferrer'
				className='absolute bottom-4 left-8 py-2 px-4 bg-green-500 text-white rounded'
			>
				<FontAwesomeIcon
					icon={faWhatsapp as IconProp}
					className='mx-2'
				/>
			</a>

			<button
				className='absolute bottom-4 right-8 btn btn-primary bg-gradient-to-l from-primary to-primarydark text-white shadow-lg rounded-xl'
				onClick={() => {
					router.push('/auth/faq');
				}}
			>
				<FontAwesomeIcon
					icon={faQuestionCircle}
					className='mr-2 text-white scale-125'
				/>
				FAQ
			</button>

			<ErrorAlert message={errorMessage} />
		</AuthLayout>
	);
};

export default Login;
