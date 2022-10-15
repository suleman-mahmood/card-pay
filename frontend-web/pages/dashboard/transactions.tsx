import type { NextPage } from 'next';
import { useEffect, useState } from 'react';
import { useSelector } from 'react-redux';
import TransactionCard from '../../components/cards/TransactionCard';
import DashboardLayout from '../../components/layouts/DashboardLayout';
import BoxLoading from '../../components/loaders/BoxLoading';
import { selectUser } from '../../store/store';
interface ITransaction {
	amount: number;
	id: string;
	recipientName: string;
	senderName: string;
	status: string;
	timestamp: string;
}

const Transactions: NextPage = () => {
	const [isLoading, setIsLoading] = useState(false);

	const [reversedTransactions, setReversedTransactions] = useState<
		Array<ITransaction>
	>([]);

	const { userState } = useSelector(selectUser);

	useEffect(() => {
		let rt = structuredClone(userState.transactions);
		rt.reverse();
		setReversedTransactions(rt);
	}, [userState]);

	return isLoading ? (
		<BoxLoading />
	) : (
		<DashboardLayout>
			<h1 className="text-2xl mb-4">Transactions</h1>

			{reversedTransactions.map((t, i) =>
				t.senderName === userState.fullName ? (
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
