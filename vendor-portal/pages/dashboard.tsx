import { onAuthStateChanged } from 'firebase/auth';
import type { NextPage } from 'next';
import { useRouter } from 'next/router';
import React, { useEffect, useState } from 'react';
import TextField from '../components/text-field';
import { auth, functions } from '../services/initialize-firebase';
import { User as FirebaseUser } from 'firebase/auth';
import Navbar from '../components/navbar';
import { httpsCallable } from 'firebase/functions';
import Swal from 'sweetalert2';
import Loader from '../components/loader';

const KEY_PAD_CONFIG = [
	[1, 2, 3],
	[4, 5, 6],
	[7, 8, 9],
	[0, 0, 0],
];

const FOCUS_DELAY = 500;

const Transactions: NextPage = () => {
	const router = useRouter();

	const [loading, setLoading] = useState(true);
	const [user, setUser] = useState<FirebaseUser | null>(null);
	const [amount, setAmount] = useState(0);
	const [rollNumber, setRollNumber] = useState(0);
	const [errorMessage, setErrorMessage] = useState('');
	const [shouldFocus, setShouldFocus] = useState(true);

	const getRandomInteger = (): number => {
		return Math.floor(Math.random() * 10000);
	};

	useEffect(() => {
		return onAuthStateChanged(auth, user => {
			if (user) {
				setUser(user);
				setLoading(false);
			} else {
				router.push('/');
			}
		});
	}, []);

	useEffect(() => {
		if (!shouldFocus) {
			return;
		}

		const intervalId = setInterval(() => {
			const elem = document.getElementById(
				'roll-number-input'
			) as HTMLInputElement;
			if (elem) {
				elem.readOnly = true;
				elem.focus();
				elem.readOnly = false;
			}
		}, FOCUS_DELAY);

		return () => clearInterval(intervalId);
	}, [shouldFocus]);

	const handleSubmit = async (e: React.FormEvent) => {
		e.preventDefault();
		setErrorMessage('');
		setShouldFocus(false);
		setLoading(true);
		setAmount(0);

		const cleanedRollNumber = rollNumber.toString().substring(4);

		const { value: userPin } = await Swal.fire({
			title: `Transaction for Rs.${amount}`,
			input: 'password',
			inputLabel: 'Input your 4-digit pin',
			inputPlaceholder: 'Enter your pin',
		});

		if (!userPin) {
			setErrorMessage('Please enter pin');
			setShouldFocus(true);
			setLoading(false);
			return;
		}

		const makeTransaction = httpsCallable(functions, 'makeTransaction');

		makeTransaction({
			amount: amount,
			senderRollNumber: cleanedRollNumber,
			pin: userPin,
		})
			.then(result => {
				setShouldFocus(true);
				setLoading(false);

				Swal.fire({
					icon: 'success',
					title: 'Transaction was successful',
					showConfirmButton: false,
					timer: 2000,
				});
			})
			.catch(error => {
				setErrorMessage(error.message);
				setShouldFocus(true);
				setLoading(false);
			});
	};

	const handleAmountClick = (value: number) => {
		setAmount(oldAmount => {
			const newAmount = oldAmount.toString() + value.toString();
			return parseInt(newAmount);
		});
	};

	const handleBackspace = () => {
		setAmount(oldAmount => {
			const oldAmountStr = oldAmount.toString();
			if (oldAmountStr.length <= 1) {
				return 0;
			}
			const newAmount = oldAmountStr.slice(0, -1);
			return parseInt(newAmount);
		});
	};

	return loading ? (
		<Loader />
	) : (
		<div className="min-h-screen flex flex-col">
			<Navbar />
			<div className="hero flex-grow">
				<div className="hero-content text-center">
					<div className="max-w-md">
						<h1 className="mb-4 text-5xl font-bold">Dashboard</h1>
						<p>1. Enter the amount using the on-screen keypad</p>
						<p className="mb-8">2. Scan the student's card</p>

						<div className="w-full flex flex-col items-center">
							{KEY_PAD_CONFIG.map((k, i) => {
								return (
									<div
										key={getRandomInteger()}
										className="flex flex-row mb-4"
									>
										{k.map(value => {
											return (
												<button
													key={getRandomInteger()}
													className="btn mr-4"
													onClick={() =>
														handleAmountClick(value)
													}
												>
													{value}
												</button>
											);
										})}
									</div>
								);
							})}
						</div>

						<button
							className="btn btn-primary mr-4"
							onClick={handleBackspace}
						>
							Delete
						</button>

						<button
							className="btn btn-secondary"
							onClick={() => setAmount(0)}
						>
							Clear amount
						</button>

						<div className="flex flex-col items-center">
							<form
								onSubmit={handleSubmit}
								className="form-control w-full max-w-xs"
							>
								<TextField
									inputType="number"
									labelText="Amount:"
									placeholder="xxxx"
									currentVal={amount}
									valueSetter={setAmount}
									readOnly={true}
								/>

								<TextField
									id="roll-number-input"
									inputType="password"
									labelText="Roll Number:"
									placeholder="00000000"
									valueSetter={setRollNumber}
								/>

								<button
									type="submit"
									className="mt-6 btn btn-outline btn-primary hidden"
								>
									Transact!
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

export default Transactions;
