import React from 'react'

interface TextFieldProps {
    labelText: string,
    placeholder: string,
    inputType: string,
    valueSetter: React.Dispatch<React.SetStateAction<any>>,
}

export default function TextField(props: TextFieldProps) {
    return (
        <div>
            <label className="label label-text">
                {props.labelText}
            </label>
            <input onChange={(e: React.ChangeEvent<HTMLInputElement>) => { props.valueSetter(e.target.value) }} required type={props.inputType} placeholder={props.placeholder} className="input input-bordered w-full max-w-xs" />
        </div>
    )
}
