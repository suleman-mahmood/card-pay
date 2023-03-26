import { FC } from 'react';

interface IButtonSecondary {
	onClick: React.MouseEventHandler<HTMLAnchorElement>;
	text: string;
	invertColors: boolean;
}

const ButtonSecondary: FC<IButtonSecondary> = (props) => {
	const colors = props.invertColors
		? 'text-white border-white'
		: 'text-blue-500 border-blue-400';

	return (
		<a
			className={
				'p-2 ml-2 outline-none text-lg shadow-lg border-2 rounded-md ' +
				colors
			}
			onClick={props.onClick}
		>
			{props.text}
		</a>
	);
};

export default ButtonSecondary;
