import { FC } from 'react';

interface ITransactionCard {}

const TransactionCard: FC<ITransactionCard> = props => {
	return (
		<div className="card w-full shadow-md text-left">
			<div className="card-body">
				<div className="card-title flex flex-row">
					<h2>From: Awesome guy</h2>
					<div className="flex-grow"></div>
					<h2>+500</h2>
				</div>
				<p>07:25 12th October 2022</p>
			</div>
		</div>
	);
};

export default TransactionCard;
