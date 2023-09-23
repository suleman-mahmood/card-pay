import { FC } from 'react';

interface IButtonPrimary {
	onClick: React.MouseEventHandler<HTMLButtonElement>;
	text: string;
	type?: 'button' | 'submit' | 'reset';
}

const ButtonPrimary: FC<IButtonPrimary> = (props) => {
	return (
		<button
			className='btn btn-primary border-hidden shadow-lg bg-gradient-to-l from-primary to-primarydark rounded-3xl text-lg text-white'
			type={props.type}
			onClick={props.onClick}
		>
			{props.text}
		</button>
	);
};

export default ButtonPrimary;
