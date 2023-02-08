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
import { functions } from '../../services/initialize-firebase';
import Swal from 'sweetalert2';
import ErrorAlert from '../../components/cards/ErrorAlert';
import TextField from '../../components/inputs/TextField';

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

	const [currStudent, setCurrStudent] = useState<UserDoc>();

	const [rollNumber, setRollNumber] = useState('');

	const handleSubmit = async (e: React.FormEvent) => {
		e.preventDefault();

		setIsLoading(true);

		try {
			const getStudent = httpsCallable(functions, 'getStudent');
			const res = await getStudent({ rollNumber: rollNumber });

			setCurrStudent(res.data as UserDoc);
			setIsLoading(false);
			setErrorMessage('');
		} catch (error) {
			setIsLoading(false);
			setErrorMessage((error as FirebaseError).message);
		}
	};

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
			<h1 className='text-2xl'>Students</h1>

			<form
				onSubmit={handleSubmit}
				className='form-control w-full max-w-xs'
			>
				<TextField
					type='text'
					// labelText='Email:'
					placeholder='Enter Roll Number'
					valueSetter={setRollNumber}
					maxLength={8}
				/>
				<button
					type='submit'
					className='mt-6 btn btn-outline btn-primary'
				>
					Search
				</button>

				<ErrorAlert message={errorMessage} />
			</form>
			{currStudent ? (
				<div className='my-4 card bg-base-200 shadow-xl'>
					<div className='card-body'>
						<h2 className='card-title'>{currStudent.fullName}</h2>
						<p>Balance: {currStudent.balance}</p>
						<p>Email: {currStudent.email}</p>
						<div className='card-actions justify-center'>
							<label htmlFor='my-modal' className='btn'>
								View transactions
							</label>
						</div>
					</div>
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
								{currStudent ? currStudent.fullName : ''}
							</h3>
							<p className='py-4'>
								{currStudent ? currStudent.email : ''}
							</p>
							{currStudent
								? currStudent.transactions.map((t, j) => (
										<TransactionCard
											amount={t.amount}
											fromOrTo='From'
											name={t.senderName}
											plusOrMinus='+'
											timestamp={beautifyTime(
												t.timestamp
											)}
											key={j}
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
			) : null}
		</DashboardLayout>
	);
};

export default Dashboard;
