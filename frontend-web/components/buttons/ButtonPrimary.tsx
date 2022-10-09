import { FC } from 'react';

interface IButtonPrimary {
	onClick: React.MouseEventHandler<HTMLButtonElement>;
	text: string;
}

const ButtonPrimary: FC<IButtonPrimary> = props => {
	return (
		<button className="btn btn-primary text-lg" onClick={props.onClick}>
			{props.text}
		</button>
	);
};

export default ButtonPrimary;
