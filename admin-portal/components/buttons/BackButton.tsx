import { FC } from 'react';
import { useRouter } from 'next/router';

interface IBackButton {
	to?: string;
	textColor?: string;
}

const BackButton: FC<IBackButton> = ({ to, textColor }) => {
	const router = useRouter();

	const redirectToDashboard = () => {
		if (to === undefined) {
			router.push('/dashboard');
		} else {
			router.push(to);
		}
	};

	return (
		<div className='btn-group grid grid-cols-2 absolute top-4 left-8'>
			<button
				className={`btn btn-outline ${
					textColor === undefined ? 'text-white' : textColor
				}`}
				onClick={redirectToDashboard}
			>
				Back
			</button>
		</div>
	);
};

export default BackButton;
