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
			<h1 className='text-2xl mb-4'>Transactions</h1>

			{reversedTransactions.map((t, i) =>
				t.senderName === userState.fullName ? (
					<TransactionCard
						amount={t.amount}
						fromOrTo='To'
						name={t.recipientName}
						plusOrMinus='-'
						timestamp={beautifyTime(t.timestamp)}
						key={i}
						color='bg-white'
						textColor='text-primarydark'
						amountTextColor='text-red-500'
					/>
				) : (
					<TransactionCard
						amount={t.amount}
						fromOrTo='From'
						name={t.senderName}
						plusOrMinus='+'
						timestamp={beautifyTime(t.timestamp)}
						key={i}
						color='bg-gradient-to-l from-primary to-primarydark'
						textColor='text-white'
						amountTextColor='text-green-400'
					/>
				)
			)}
		</DashboardLayout>
	);
};

export default Transactions;
