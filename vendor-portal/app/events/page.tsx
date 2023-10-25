"use client";
import React from "react";
import { useEffect, useState } from "react";
import { useRouter } from "next/navigation";
import { createWatchCompilerHost, isConstructorDeclaration } from "@/node_modules/typescript/lib/typescript";
import { isMapIterator } from "util/types";

enum EventStatus {
    DRAFT,
    APPROVED,
    CANCELLED,
}

enum QuestionType {
    INPUT_STR,
    INPUT_INT,
    INPUT_FLOAT,
    MULTIPLE_CHOICE,
    DROPDOWN,
}

enum ValidationEnum {
    REQUIRED,
    MIN_LENGTH,
    MAX_LENGTH,
}

interface ValidationRule {
    type: ValidationEnum,
    value: number | boolean,
}

interface EventFormSchemaItem {
    question: string
    type: QuestionType
    validation: ValidationRule[]
    options: string[]
}

interface EventFormSchema {
    fields: EventFormSchemaItem[]
}

interface Event {
    id: string;
    status: EventStatus;
    cancellation_reason: string;
    name: string;
    organizer_name: string;
    venue: string;
    capacity: number;
    description: string;
    image_url: string;
    closed_loop_id: string;
    event_start_timestamp: string;
    event_end_timestamp: string;
    registration_start_timestamp: string;
    registration_end_timestamp: string;
    registration_fee: number;
    qr_id?: string;
    event_form_schema: EventFormSchema;
}

export default function page() {
    const [events, setEvents] = useState<Event[]>([
        {
            id: "",
            status: EventStatus.APPROVED,
            cancellation_reason: "",
            name: "some event",
            organizer_name: "",
            venue: "",
            capacity: 50,
            description: "",
            image_url: "",
            closed_loop_id: "",
            event_start_timestamp: "",
            event_end_timestamp: "",
            registration_start_timestamp: "",
            registration_end_timestamp: "",
            registration_fee: 50,
            qr_id: "",
            event_form_schema: {
                "fields": [
                    {
                        question: "Enter your name?",
                        options: [],
                        type: QuestionType.INPUT_STR,
                        validation: [
                            {
                                type: ValidationEnum.MIN_LENGTH,
                                value: 5
                            },
                            {
                                type: ValidationEnum.REQUIRED,
                                value: true
                            },
                            {
                                type: ValidationEnum.MAX_LENGTH,
                                value: 25
                            }
                        ],
                    },
                    {
                        question: "Choose batch",
                        options: ["23", "24", "25"],
                        type: QuestionType.DROPDOWN,
                        validation: [],
                    },
                    {
                        question: "Age?",
                        options: [],
                        type: QuestionType.INPUT_INT,
                        validation: [],
                    },
                    {
                        question: "Average car milage??",
                        options: [],
                        type: QuestionType.INPUT_FLOAT,
                        validation: [],
                    },
                    {
                        question: "Hobbies?",
                        options: ["Cricket", "Football", "E-gaming"],
                        type: QuestionType.MULTIPLE_CHOICE,
                        validation: [],
                    }
                ]
            }
        }
    ]);
    const [selectedEvent, setSelectedEvent] = useState<Event>();
    const [formResponses, setFormResponses] = useState([]);
    const [checkedOptions, setCheckedOptions] = useState([]);

    const submitForm = () => {
        // let formattedResponses = formResponses.filter((response) => response !== undefined);
        // formattedResponses = { fields: [formattedResponses] }
        // console.log(formattedResponses);
        window.location.href = "https://marketplace.paypro.com.pk/pyb?bid=MTIzNTIzMjA3MDAwMDE%3d";
    };

    const buildInput = (schemaItem: EventFormSchemaItem, index: any) => {
        const handleInputChange = (e, option = null) => {
            let value;

            if (schemaItem.type === QuestionType.MULTIPLE_CHOICE) {
                const clickedOption = checkedOptions.indexOf(option);
                let all = [...checkedOptions];
                if (clickedOption === -1) {
                    all.push(option);
                } else {
                    all.splice(clickedOption, 1);
                }
                setCheckedOptions(all);
                all = all.join(",")
                const updatedResponses = [...formResponses];
                updatedResponses[index] = { question: schemaItem.question, answer: all };
                setFormResponses(updatedResponses);
            } else {
                value = e.target.value;
                const updatedResponses = [...formResponses];
                updatedResponses[index] = { question: schemaItem.question, answer: value };
                setFormResponses(updatedResponses);
            }

        };

        if (schemaItem.type === QuestionType.INPUT_STR) {
            if (schemaItem.validation.length !== 0) {
                let minLength = undefined;
                let maxLength = undefined;
                let required = undefined;
                schemaItem.validation.map((item) => {
                    if (item.type === ValidationEnum.REQUIRED && typeof (item.value) === "boolean") {
                        required = item.value
                    }
                    if (item.type === ValidationEnum.MIN_LENGTH) {
                        minLength = item.value
                    }
                    if (item.type === ValidationEnum.MAX_LENGTH) {
                        maxLength = item.value
                    }
                })
                return (
                    <form>
                        <input
                            type="text"
                            className="input input-bordered w-full max-w-xs"
                            onChange={handleInputChange}
                            required={required}
                            minLength={minLength}
                            maxLength={maxLength}
                        />
                    </form>
                )
            }
            else {
                return (
                    <input
                        type="text"
                        className="input input-bordered w-full max-w-xs"
                        onChange={handleInputChange}
                    />
                )
            }
        }
        if (schemaItem.type === QuestionType.INPUT_INT || schemaItem.type === QuestionType.INPUT_FLOAT) {
            return (
                <input type="number" className="input input-bordered w-full max-w-xs" onChange={handleInputChange} />
            )
        }
        if (schemaItem.type === QuestionType.DROPDOWN) {
            return (
                <select className="select select-bordered w-full max-w-xs" onChange={handleInputChange}>
                    <option disabled>{schemaItem.question}</option>
                    {schemaItem.options.map((option, j) => <option key={j}>{option}</option>)}
                </select>
            )
        }
        if (schemaItem.type === QuestionType.MULTIPLE_CHOICE) {
            return (
                <div className="form-control">
                    {schemaItem.options.map((option, j) => (
                        <label key={j} className="label cursor-pointer">
                            <input type="checkbox" className="checkbox"
                                value={option}
                                onChange={(e) => handleInputChange(e, option)}
                            />
                            <span className="label-text ml-2">{option}</span>
                        </label>
                    ))}
                </div>
            )
        }

    }

    return <div className="flex min-h-screen flex-col items-center p-2">
        <h1 className="" >Register event</h1>
        <details className="dropdown mb-4">
            <summary className="m-1 btn">Select event</summary>
            <ul className="p-2 shadow menu dropdown-content z-[1] bg-base-100 rounded-box w-52">
                {
                    events.map((event, i) => (
                        <li key={i} onClick={() => setSelectedEvent(event)}><a>Item {event.name}</a></li>
                    ))
                }
            </ul>
        </details>
        <h1>Selected event: {selectedEvent?.name}</h1>

        {
            selectedEvent?.event_form_schema.fields.map((field, i) => (
                <div key={i}>
                    <div className="form-control w-full max-w-xs">
                        <label className="label">
                            <span className="label-text">{field.question}</span>
                        </label>
                        {buildInput(field, i)}
                    </div>
                </div>
            ))
        }

        <button className="btn btn-primary" onClick={submitForm}>Submit</button>


    </div>
}