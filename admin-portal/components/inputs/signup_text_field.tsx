import { FC } from 'react';

interface ITextField {
	placeholder: string;
	type: string;
	valueSetter: React.Dispatch<React.SetStateAction<any>>;
	value?: number;
	maxLength?: number;
}

const TextField: FC<ITextField> = props => {
	return (
		<input
			type={props.type}
			placeholder={props.placeholder}
			className='input bg-white rounded-3xl text-primarydark placeholder-primary w-full max-w-xs mb-4 shadow-lg focus:bg-gray-100'
			onChange={(e: React.ChangeEvent<HTMLInputElement>) => {
				props.valueSetter(e.target.value);
			}}
			maxLength={props.maxLength}
			value={props.value}
		/>
	);
};

export default TextField;
