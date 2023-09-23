import { FC } from 'react';

interface IErrorAlert {
	message: string;
}

const ErrorAlert: FC<IErrorAlert> = props => {
	return props.message.length === 0 ? (
		<div></div>
	) : (
		<div className="alert alert-error shadow-lg my-2">
			<div>
				<svg
					xmlns="http://www.w3.org/2000/svg"
					className="stroke-current flex-shrink-0 h-6 w-6"
					fill="none"
					viewBox="0 0 24 24"
				>
					<path
						strokeLinecap="round"
						strokeLinejoin="round"
						strokeWidth="2"
						d="M10 14l2-2m0 0l2-2m-2 2l-2-2m2 2l2 2m7-2a9 9 0 11-18 0 9 9 0 0118 0z"
					/>
				</svg>
				<span>Error! {props.message}</span>
			</div>
		</div>
	);
};

export default ErrorAlert;
