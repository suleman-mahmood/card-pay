import { FC } from 'react';
import { useRouter } from 'next/router';

interface IBackButton {}

const BackButton: FC<IBackButton> = props => {
	const router = useRouter();

	const redirectToDashboard = () => {
		router.push('/dashboard');
	};

	return (
		<div className='btn-group grid grid-cols-2 absolute top-4 left-8'>
			<button
				className='btn btn-outline text-white'
				onClick={redirectToDashboard}
			>
				Back
			</button>
		</div>
	);
};

export default BackButton;
