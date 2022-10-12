import { doc, getDoc } from 'firebase/firestore';
import type { NextPage } from 'next';
import { useRouter } from 'next/router';
import { useEffect, useState } from 'react';
import ButtonPrimary from '../../components/buttons/ButtonPrimary';
import TransactionCard from '../../components/cards/TransactionCard';
import DashboardLayout from '../../components/layouts/DashboardLayout';
import BoxLoading from '../../components/loaders/BoxLoading';
import { auth, db } from '../../services/initialize-firebase';

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

interface ITransaction {
	amount: number;
	id: string;
	recipientName: string;
	senderName: string;
	status: string;
	timestamp: string;
}

const Transactions: NextPage = () => {
	const router = useRouter();

	const [isLoading, setIsLoading] = useState(false);

	const [userData, setUserData] = useState<userDataDoc | null>(null);
	const [reversedTransactions, setReversedTransactions] = useState<
		Array<ITransaction>
	>([]);

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
			const data = docSnap.data() as userDataDoc;
			setUserData(data);

			const rt = data.transactions.reverse();
			setReversedTransactions(rt);
		} else {
			console.log('Could not find user document');
		}

		setIsLoading(false);
	};

	return isLoading ? (
		<BoxLoading />
	) : (
		<DashboardLayout>
			<h1 className="text-2xl mb-4">Transactions</h1>

			{reversedTransactions.map((t, i) =>
				t.senderName === userData!.fullName ? (
					<TransactionCard
						amount={t.amount}
						fromOrTo="To"
						name={t.recipientName}
						plusOrMinus="-"
						timestamp={t.timestamp}
						key={i}
						color="bg-red-100"
					/>
				) : (
					<TransactionCard
						amount={t.amount}
						fromOrTo="From"
						name={t.senderName}
						plusOrMinus="+"
						timestamp={t.timestamp}
						key={i}
						color="bg-green-100"
					/>
				)
			)}
		</DashboardLayout>
	);
};

export default Transactions;
