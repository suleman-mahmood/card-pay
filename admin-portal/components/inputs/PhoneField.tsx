import { FC } from 'react';

interface IPhoneField {
	valueSetter: React.Dispatch<React.SetStateAction<any>>;
}

const PhoneField: FC<IPhoneField> = props => {
	return (
		<div className='form-control'>
			<label className='label'>
				<span className='label-text text-white font-semibold text-base '>
					Phone number
				</span>
			</label>
			<label className='input-group'>
				<span className='bg-white text-primarydark'>+92</span>
				<input
					type='text'
					placeholder='3334312540'
					className='input input-bordered bg-white text-primarydark placeholder-primary w-full max-w-xs shadow-lg'
					maxLength={10}
					onChange={(e: React.ChangeEvent<HTMLInputElement>) => {
						props.valueSetter(e.target.value);
					}}
				/>
			</label>
		</div>
	);
};

export default PhoneField;
