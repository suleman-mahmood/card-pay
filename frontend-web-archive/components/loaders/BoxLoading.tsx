import { FC } from 'react';
import { useLottie } from 'lottie-react';
import * as animationData from '../../assets/box-loader.json';

interface IBoxLoading {}

const BoxLoading: FC<IBoxLoading> = props => {
	const { View } = useLottie({
		animationData: animationData,
		loop: true,
		autoplay: true,
	});
	return (
		<div className="min-h-screen flex flex-col justify-center">{View}</div>
	);
};

export default BoxLoading;
