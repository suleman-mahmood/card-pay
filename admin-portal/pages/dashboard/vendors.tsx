import { FirebaseError } from 'firebase-admin';
import { onAuthStateChanged } from 'firebase/auth';
import { collection, getDocs, query, where } from 'firebase/firestore';
import { httpsCallable } from 'firebase/functions';
import type { NextPage } from 'next';
import { useRouter } from 'next/router';
import { useEffect, useState } from 'react';
import TransactionCard from '../../components/cards/TransactionCard';
import DashboardLayout from '../../components/layouts/DashboardLayout';
import BoxLoading from '../../components/loaders/BoxLoading';
import { auth, db, functions } from '../../services/initialize-firebase';

const ADMIN_UID = 'JoNhydNzAWXGilGS4fRsOK1ePTm2';

type UserRole = 'student' | 'vendor' | 'admin';

interface Transaction {
	amount: number;
	id: string;
	timestamp: string;
	senderName: string;
	recipientName: string;
	status: string;
}

interface UserDoc {
	id: string;
	fullName: string;
	personalEmail: string;
	email: string;
	pendingDeposits: boolean;
	pin: string;
	phoneNumber: string;
	rollNumber: string;
	verified: boolean;
	role: UserRole;
	balance: number;
	transactions: Array<Transaction>;
}

const Dashboard: NextPage = () => {
	const router = useRouter();

	const [isLoading, setIsLoading] = useState(false);
	const [errorMessage, setErrorMessage] = useState('');

	const [vendors, setVendors] = useState<UserDoc[]>([]);
	const [currentVendor, setCurrentVendor] = useState<UserDoc>();

	useEffect(() => {
		const getVendors = async () => {
			try {
				const getAllVendors = httpsCallable(functions, 'getAllVendors');
				const res = await getAllVendors({});

				setVendors(res.data as UserDoc[]);
				setErrorMessage('');
			} catch (error) {
				setErrorMessage((error as FirebaseError).message);
			}
		};

		getVendors();
	}, []);

	const beautifyTime = (t: string): string => {
		const options = {
			minute: 'numeric',
			hour: 'numeric',
			month: 'short',
			day: 'numeric',
			year: 'numeric',
		} as const;
		const today = new Date(t);

		return today.toLocaleDateString('en-US', options);
	};

	return isLoading ? (
		<BoxLoading />
	) : (
		<DashboardLayout>
			<h1 className='text-2xl'>Vendors</h1>

			{vendors.map((v, i) => (
				<div key={i} className='card bg-base-100 shadow-xl'>
					<div className='card-body'>
						<h2 className='card-title'>{v.fullName}</h2>
						<p>Balance: {v.balance}</p>
						<p>Email: {v.email}</p>
						<div className='card-actions justify-center'>
							<label
								onClick={() => setCurrentVendor(v)}
								htmlFor='my-modal'
								className='btn'
							>
								View transactions
							</label>
						</div>
					</div>

					{/* Modal stuff */}
					<input
						type='checkbox'
						id='my-modal'
						className='modal-toggle'
					/>
					<div className='modal'>
						<div className='modal-box'>
							<div className='modal-action'>
								<label htmlFor='my-modal' className='btn'>
									Close!
								</label>
							</div>
							<h3 className='font-bold text-lg'>
								{currentVendor ? currentVendor.fullName : ''}
							</h3>
							<p className='py-4'>
								{currentVendor ? currentVendor.email : ''}
							</p>
							{currentVendor
								? currentVendor.transactions.map((t, j) => (
										<TransactionCard
											amount={t.amount}
											fromOrTo='From'
											name={t.senderName}
											plusOrMinus='+'
											timestamp={beautifyTime(
												t.timestamp
											)}
											key={i * 10000 + j}
											color='bg-gradient-to-l from-primary to-primarydark'
											textColor='text-white'
											amountTextColor='text-green-400'
										/>
								  ))
								: ''}
							<div className='modal-action'>
								<label htmlFor='my-modal' className='btn'>
									Close!
								</label>
							</div>
						</div>
					</div>
				</div>
			))}
		</DashboardLayout>
	);
};

export default Dashboard;
