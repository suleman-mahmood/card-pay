import { FC } from 'react';

interface ITransactionCard {
	fromOrTo: 'From' | 'To';
	plusOrMinus: '+' | '-';
	color: 'bg-red-100' | 'bg-green-100';
	name: string;
	amount: number;
	timestamp: string;
}

const TransactionCard: FC<ITransactionCard> = props => {
	return (
		<div
			className={
				'card w-full mb-2 shadow-md text-left bg-red-100 ' + props.color
			}
		>
			<div className="card-body">
				<div className="card-title flex flex-row">
					<h2>
						{props.fromOrTo}: {props.name}
					</h2>
					<div className="flex-grow"></div>
					<h2>
						{props.plusOrMinus}
						{props.amount}
					</h2>
				</div>
				<p>{props.timestamp}</p>
			</div>
		</div>
	);
};

export default TransactionCard;
