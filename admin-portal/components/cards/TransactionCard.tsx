import { FC } from 'react';

interface ITransactionCard {
	fromOrTo: 'From' | 'To';
	plusOrMinus: '+' | '-';
	color: 'bg-white' | 'bg-gradient-to-l from-primary to-primarydark';
	textColor: 'text-white' | 'text-primarydark';
	amountTextColor: 'text-red-500' | 'text-green-400';
	name: string;
	amount: number;
	timestamp: string;
}

const TransactionCard: FC<ITransactionCard> = props => {
	return (
		<div
			className={
				'card w-full h-24 mb-2 shadow-md text-left ' + props.color + ' ' + props.textColor
			}
		>
			<div className="card-body pt-4">
				<div className="card-title flex flex-row truncate">
					<h2 className='text-ellipsis overflow-hidden'>
						{props.name}
					</h2>
					<div className="flex-grow"></div>
					<h2 className={props.amountTextColor}>
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
