import { FC, useState, useEffect } from 'react';
import { useRouter } from 'next/router';

interface IBackButtonProps {
	textColor?: string;
}

const BackButton: FC<IBackButtonProps> = ({ textColor }) => {
	const router = useRouter();

	const handleBack = () => {
		router.back();
	};

	return (
		<div className='btn-group grid grid-cols-2 absolute top-4 left-8'>
			<button
				className={'btn btn-outline textColor text-white ' + textColor}
				onClick={handleBack}
			>
				Back
			</button>
		</div>
	);
};

export default BackButton;
