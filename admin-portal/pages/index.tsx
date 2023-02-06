import type { NextPage } from 'next';
import Head from 'next/head';
import { auth } from '../services/initialize-firebase';
import React, { useState } from 'react';
import { signInWithEmailAndPassword } from 'firebase/auth';
import { useRouter } from 'next/router';
import { FirebaseError } from 'firebase-admin';
import BoxLoading from '../components/loaders/BoxLoading';
import ErrorAlert from '../components/cards/ErrorAlert';
import TextField from '../components/inputs/TextField';

const ADMIN_UID = 'JoNhydNzAWXGilGS4fRsOK1ePTm2';

const Index: NextPage = () => {
	const router = useRouter();

	const [email, setEmail] = useState('');
	const [password, setPassword] = useState('');
	const [errorMessage, setErrorMessage] = useState('');
	const [isLoading, setIsLoading] = useState(false);

	const handleSubmit = async (e: React.FormEvent) => {
		e.preventDefault();
		setErrorMessage('');
		setIsLoading(true);

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
		<div>
			<Head>
				<title>Admin Portal - CardPay</title>
				<meta
					name='description'
					content='Admin portal for CardPay app'
				/>
				<link rel='icon' href='/favicon.ico' />
			</Head>

			<div className='hero min-h-screen'>
				<div className='hero-content text-center'>
					<div className='max-w-5xl'>
						<h1 className='text-5xl font-bold'>
							Welcome to <b>Admin Portal</b> for CardPay!
						</h1>
						<p className='py-6'>
							Get started by logging in to your CardPay Admin
							account
						</p>

						<div className='flex flex-col items-center'>
							<form
								onSubmit={handleSubmit}
								className='form-control w-full max-w-xs'
							>
								<TextField
									type='email'
									// labelText='Email:'
									placeholder='cool.vendor@profit.com'
									valueSetter={setEmail}
								/>

								<TextField
									type='password'
									// labelText='Password:'
									placeholder='********'
									valueSetter={setPassword}
								/>

								<button
									type='submit'
									className='mt-6 btn btn-outline btn-primary'
								>
									Login
								</button>

								<ErrorAlert message={errorMessage} />
							</form>
						</div>
					</div>
				</div>
			</div>
		</div>
	);
};

export default Index;
