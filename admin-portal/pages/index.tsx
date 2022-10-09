import type { NextPage } from 'next';
import Head from 'next/head';
import { auth, db } from '../services/initialize-firebase';
import React, { useEffect, useState } from 'react';
import { onAuthStateChanged, signInWithEmailAndPassword } from 'firebase/auth';
import { useRouter } from 'next/router';
import TextField from '../components/text-field';
import Loader from '../components/loader';

const ADMIN_UID = 'JoNhydNzAWXGilGS4fRsOK1ePTm2';

const Index: NextPage = () => {
	const router = useRouter();

	const [email, setEmail] = useState('');
	const [password, setPassword] = useState('');
	const [errorMessage, setErrorMessage] = useState('');
	const [loading, setLoading] = useState(false);

	const handleSubmit = (e: React.FormEvent) => {
		e.preventDefault();
		setErrorMessage('');
		setLoading(true);
	};

	return loading ? (
		<Loader />
	) : (
		<div>
			<Head>
				<title>Admin Portal - CardPay</title>
				<meta
					name="description"
					content="Admin portal for CardPay app"
				/>
				<link rel="icon" href="/favicon.ico" />
			</Head>

			<div className="hero min-h-screen">
				<div className="hero-content text-center">
					<div className="max-w-5xl">
						<h1 className="text-5xl font-bold">
							Welcome to <b>Admin Portal</b> for CardPay!
						</h1>
						<p className="py-6">
							Get started by logging in to your CardPay Admin
							account
						</p>

						<div className="flex flex-col items-center">
							<form
								onSubmit={handleSubmit}
								className="form-control w-full max-w-xs"
							>
								<TextField
									inputType="email"
									labelText="Email:"
									placeholder="cool.vendor@profit.com"
									valueSetter={setEmail}
								/>

								<TextField
									inputType="password"
									labelText="Password:"
									placeholder="********"
									valueSetter={setPassword}
								/>

								<button
									type="submit"
									className="mt-6 btn btn-outline btn-primary"
								>
									Login
								</button>

								{errorMessage === '' ? null : (
									<div className="mt-6 alert alert-error shadow-lg">
										<div>
											<svg
												xmlns="http://www.w3.org/2000/svg"
												className="stroke-current flex-shrink-0 h-6 w-6"
												fill="none"
												viewBox="0 0 24 24"
											>
												<path
													strokeLinecap="round"
													strokeLinejoin="round"
													strokeWidth="2"
													d="M10 14l2-2m0 0l2-2m-2 2l-2-2m2 2l2 2m7-2a9 9 0 11-18 0 9 9 0 0118 0z"
												/>
											</svg>
											<span>Error! {errorMessage}</span>
										</div>
									</div>
								)}
							</form>
						</div>
					</div>
				</div>
			</div>
		</div>
	);
};

export default Index;
