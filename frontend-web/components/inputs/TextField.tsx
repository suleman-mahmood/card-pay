import { FC } from 'react';

interface ITextField {
	placeholder: string;
}

const TextField: FC<ITextField> = props => {
	return (
		<input
			type="text"
			placeholder={props.placeholder}
			className="input input-bordered w-full max-w-xs mb-4"
		/>
	);
};

export default TextField;
