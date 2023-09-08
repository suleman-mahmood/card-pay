import React from 'react';

interface TextFieldProps {
	id?: string;
	labelText: string;
	placeholder: string;
	inputType: string;
	valueSetter: React.Dispatch<React.SetStateAction<any>>;
	currentVal?: number;
	readOnly?: boolean;
}

export default function TextField(props: TextFieldProps) {
	return (
		<div className="mb-4">
			<label className="text-2xl label label-text">
				{props.labelText}
			</label>
			<input
				id={props.id}
				onChange={(e: React.ChangeEvent<HTMLInputElement>) => {
					props.valueSetter(e.target.value);
				}}
				required
				type={props.inputType}
				placeholder={props.placeholder}
				className="input input-bordered text-2xl"
				value={props.currentVal}
				readOnly={props.readOnly}
			/>
		</div>
	);
}