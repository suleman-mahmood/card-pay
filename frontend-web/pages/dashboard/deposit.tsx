import { FirebaseError } from 'firebase/app';
import { doc, getDoc } from 'firebase/firestore';
import { httpsCallable } from 'firebase/functions';
import type { NextPage } from 'next';
import { useRouter } from 'next/router';
import { useEffect, useState } from 'react';
import ButtonPrimary from '../../components/buttons/ButtonPrimary';
import ErrorAlert from '../../components/cards/ErrorAlert';
import TextField from '../../components/inputs/TextField';
import AuthLayout from '../../components/layouts/AuthLayout';
import BoxLoading from '../../components/loaders/BoxLoading';
import { auth, db, functions } from '../../services/initialize-firebase';

interface userDataDoc {
	balance: number;
	email: string;
	fullName: string;
	id: string;
	role: string;
	rollNumber: string;
	verified: boolean;
	transactions: Array<{
		amount: number;
		id: string;
		recipientName: string;
		senderName: string;
		status: string;
		timestamp: string;
	}>;
}

const Deposit: NextPage = () => {
	const router = useRouter();

	const [amount, setAmount] = useState(0);
	const [userData, setUserData] = useState<userDataDoc | null>(null);

	const [errorMessage, setErrorMessage] = useState('');
	const [isLoading, setIsLoading] = useState(false);

	useEffect(() => {
		return auth.onAuthStateChanged(user => {
			if (user) {
				if (!user.emailVerified) {
					router.push('/auth/student-verification');
				} else {
					// User is logged in
					fetchUserData(user.uid);
				}
			} else {
				router.push('/');
			}
		});
	}, []);

	const fetchUserData = async (uid: string) => {
		setIsLoading(true);

		const docRef = doc(db, 'users', uid);
		const docSnap = await getDoc(docRef);

		if (docSnap.exists()) {
			setUserData(docSnap.data() as userDataDoc);
		} else {
			console.log('Could not find user document');
		}

		setIsLoading(false);
	};

	const redirectToDashboard = () => {
		router.push('/dashboard');
	};

	const handleDeposit = async () => {
		if (amount <= 0) {
			setErrorMessage('Please enter an amount greater than 0');
			return;
		} else if (userData === null) {
			setErrorMessage('Please refresh the page');
			return;
		}

		setIsLoading(true);
		setErrorMessage('');

		const addDepositRequest = httpsCallable(functions, 'addDepositRequest');
		try {
			const { data } = await addDepositRequest({
				amount: amount,
				fullName: userData?.fullName,
				email: userData?.email,
			});

			setIsLoading(false);
			setErrorMessage('');

			const url = (data as any).paymentUrl;
			window.location.href = url;

			// Don't use, browsers disables pop-ups
			// window.open(url, '_blank');
		} catch (error) {
			setIsLoading(false);
			setErrorMessage((error as FirebaseError).code);
			console.log(error);
		}
	};

	return isLoading ? (
		<BoxLoading />
	) : (
		<AuthLayout>
			<h1 className="text-2xl">Deposit</h1>
			<h2 className="mb-4 text-xl">Deposit funds in your student card</h2>

			<TextField
				type="number"
				valueSetter={setAmount}
				placeholder="Amount"
			/>

			<ButtonPrimary onClick={handleDeposit} text="Deposit Now!" />

			<ErrorAlert message={errorMessage} />

			<div className="btn-group grid grid-cols-2 absolute top-6 left-6">
				<button
					className="btn btn-outline"
					onClick={redirectToDashboard}
				>
					Back
				</button>
			</div>
		</AuthLayout>
	);
};

export default Deposit;
