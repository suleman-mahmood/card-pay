import { FC } from 'react';

interface ITextField {
	placeholder: string;
	type: string;
	valueSetter: React.Dispatch<React.SetStateAction<any>>;
	maxLength?: number;
}

const TextField: FC<ITextField> = props => {
	return (
		<input
			type={props.type}
			placeholder={props.placeholder}
			className="input input-bordered w-full max-w-xs mb-4"
			onChange={(e: React.ChangeEvent<HTMLInputElement>) => {
				props.valueSetter(e.target.value);
			}}
			maxLength={props.maxLength}
		/>
	);
};

export default TextField;
