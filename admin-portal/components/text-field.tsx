import React from "react";

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
    <div>
      <label className="label label-text">{props.labelText}</label>
      <input
        id={props.id}
        onChange={(e: React.ChangeEvent<HTMLInputElement>) => {
          props.valueSetter(e.target.value);
        }}
        required
        type={props.inputType}
        placeholder={props.placeholder}
        className="input input-bordered w-full max-w-xs"
        value={props.currentVal}
        readOnly={props.readOnly}
      />
    </div>
  );
}
