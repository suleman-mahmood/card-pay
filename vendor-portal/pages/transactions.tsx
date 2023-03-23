import { onAuthStateChanged } from 'firebase/auth';
import type { NextPage } from 'next';
import { useRouter } from 'next/router';
import React, { useEffect, useState } from 'react';
import TextField from '../components/text-field';
import { auth, db, functions } from '../services/initialize-firebase';
import { User as FirebaseUser } from 'firebase/auth';
import Navbar from '../components/navbar';
import { httpsCallable } from 'firebase/functions';
import Swal from 'sweetalert2';
import Loader from '../components/loader';
import { doc, getDoc } from 'firebase/firestore';

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

const Transactions: NextPage = () => {
	const router = useRouter();

	const [loading, setLoading] = useState(true);
	const [user, setUser] = useState<FirebaseUser | null>(null);
	const [userData, setUserData] = useState<userDataDoc | null>(null);

	useEffect(() => {
		return onAuthStateChanged(auth, (user) => {
			if (user) {
				setUser(user);
				fetchUserData(user.uid);
			} else {
				router.push('/');
			}
		});
	}, []);

	const fetchUserData = async (uid: string) => {
		const docRef = doc(db, 'users', uid);
		const docSnap = await getDoc(docRef);

		if (docSnap.exists()) {
			setUserData(docSnap.data() as userDataDoc);
		} else {
			console.log('Could not find user document');
		}

		setLoading(false);
	};

	const formatTimestamp = (timestamp: string | number): string => {
		const date = new Date(timestamp);
		const options: Intl.DateTimeFormatOptions = {
			weekday: 'long',
			year: 'numeric',
			month: 'long',
			day: 'numeric',
			hour: 'numeric',
			minute: 'numeric',
		};

		return date.toLocaleDateString('en-US', options);
	};

	const showTransactions = () => {
		const transactions = userData?.transactions.map((v) => {
			const d = new Date(v.timestamp);
			return { ...v, timestamp: d.getTime() };
		});

		if (transactions === undefined) {
			return;
		}

		transactions.sort((obj1, obj2) => obj2.timestamp - obj1.timestamp);

		const lastReconcile = [];
		for (let i = 0; i < transactions.length; i++) {
			const t = transactions[i];

			if (t.senderName === userData?.fullName) {
				break;
			}

			lastReconcile.push(t);
		}

		return lastReconcile.map((v, i) => (
			<tr key={i}>
				<th>{v.senderName}</th>
				<th>{v.amount}</th>
				<th>{formatTimestamp(v.timestamp)}</th>
			</tr>
		));
	};

	return loading ? (
		<Loader />
	) : (
		<div className='min-h-screen flex flex-col'>
			<Navbar />
			<div className='hero flex-grow'>
				<div className='w-full hero-content text-center'>
					<div className='w-full'>
						<h1 className='mb-4 text-5xl font-bold'>
							Transactions
						</h1>
						<p>{userData?.fullName}</p>
						<p className='mb-8'>Balance: {userData?.balance}</p>

						<div className='w-full overflow-x-auto'>
							<table className='table w-full'>
								<thead>
									<tr>
										<th>Sender Name</th>
										<th>Amount</th>
										<th>Timestamp</th>
									</tr>
								</thead>
								<tbody>{showTransactions()}</tbody>
							</table>
						</div>
					</div>
				</div>
			</div>
		</div>
	);
};

export default Transactions;
