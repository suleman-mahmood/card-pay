import { FirebaseError } from 'firebase/app';
import { doc, getDoc } from 'firebase/firestore';
import { httpsCallable } from 'firebase/functions';
import type { NextPage } from 'next';
import { useRouter } from 'next/router';
import { useEffect, useState } from 'react';
import ButtonPrimary from '../../components/buttons/ButtonPrimary';
import ErrorAlert from '../../components/cards/ErrorAlert';
import TextField from '../../components/inputs/TextField';
import DashboardLayout from '../../components/layouts/DashboardLayout';
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

const Transfer: NextPage = () => {
	const router = useRouter();

	const [rollNumber, setRollNumber] = useState('');
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

	const handleTransfer = async () => {
		if (amount <= 0) {
			setErrorMessage('Please enter an amount greater than 0');
			return;
		} else if (rollNumber.length !== 8) {
			setErrorMessage('Please enter an 8-digit Roll Number');
			return;
		} else if (userData === null) {
			setErrorMessage('Please refresh the page');
			return;
		}

		setIsLoading(true);
		setErrorMessage('');

		const transfer = httpsCallable(functions, 'transfer');
		try {
			await transfer({
				amount: amount,
				recipientRollNumber: rollNumber,
			});

			setIsLoading(false);
			setErrorMessage('');

			router.push('/dashboard');
		} catch (error) {
			setIsLoading(false);
			setErrorMessage((error as FirebaseError).code);
			console.log(error);
		}
	};

	return isLoading ? (
		<BoxLoading />
	) : (
		<DashboardLayout>
			<h1 className="text-2xl">Transfer</h1>
			<h2 className="mb-4 text-xl">Peer to Peer funds transfer</h2>

			<TextField
				type="text"
				valueSetter={setRollNumber}
				maxLength={8}
				placeholder="Roll Number"
			/>
			<TextField
				type="number"
				valueSetter={setAmount}
				placeholder="Amount"
			/>

			<ButtonPrimary onClick={handleTransfer} text="Transfer Now!" />

			<ErrorAlert message={errorMessage} />
		</DashboardLayout>
	);
};

export default Transfer;
