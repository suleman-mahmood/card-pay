import { FC } from 'react';

interface ITextField {
	placeholder: string;
	type: string;
	valueSetter: React.Dispatch<React.SetStateAction<any>>;
	value?: string;
	maxLength?: number;
}

const TextField: FC<ITextField> = (props) => {
	return (
		<input
			type={props.type}
			placeholder={props.placeholder}
			className='input bg-gradient-to-l from-primary to-primarydark rounded-3xl text-white placeholder-white w-full max-w-xs mb-4'
			onChange={(e: React.ChangeEvent<HTMLInputElement>) => {
				props.valueSetter(e.target.value);
			}}
			maxLength={props.maxLength}
			value={props.value}
		/>
	);
};

export default TextField;
