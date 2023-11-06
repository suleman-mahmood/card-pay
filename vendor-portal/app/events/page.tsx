"use client";
/* eslint-disable */
import React from "react";
import { useEffect, useState } from "react";
import { useRouter } from "next/navigation";
import { User as FirebaseUser } from "firebase/auth";
import LoadingOverlay from "./spinner";
import { useSearchParams } from 'next/navigation'

const BASE_URL_PROD = 'https://cardpay-1.el.r.appspot.com';
const BASE_URL_DEV = 'https://dev-dot-cardpay-1.el.r.appspot.com';
const BASE_URL = BASE_URL_PROD;

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
    DYNAMIC_INPUT_STR,
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
    const router = useRouter();
    const searchParams = useSearchParams()
    const [events, setEvents] = useState<Event[]>([]);
    const [user, setUser] = useState<FirebaseUser | null>(null);
    const [selectedEvent, setSelectedEvent] = useState<Event>();
    const [formResponses, setFormResponses] = useState({});
    const [checkedOptions, setCheckedOptions]: any = useState([]);
    const [isOpen, setIsOpen] = useState(false);
    const [isLoadingSpinner, setIsLoadingSpinner] = useState(true);
    const [showPopup, setShowPopup] = useState(false);
    const [showSuccessPopup, setShowSuccessPopup] = useState(false);
    const [popupMessage, setPopupMessage] = useState('');
    const [phoneNumber, setPhoneNumber] = useState('');
    const [isValidPhoneNumber, setIsValidPhoneNumber] = useState(false);
    const [email, setEmail] = useState('');
    const [isValidEmail, setIsValidEmail] = useState(false);
    const [dynamicInputStrs, setDynamicInputStrs] = useState<{ [name: string]: string }>({});

    useEffect(() => {
        fetchEvents();
    }, []);

    const SearchBar = () => {
        const search = searchParams.get('event_id')
        return search;
    }

    const handleSelectChange = (event: any) => {
        events.map((item) => {
            if (event.target.value === item.id) {
                console.log(item);

                setSelectedEvent(item);
            }
        })
    };

    const fetchEvents = async () => {
        fetch(
            `${BASE_URL}/api/v1/vendor-app/get-live-events?closed_loop_id=${'2456ce60-7b0a-4369-a392-2400653dbdaf'}`,
            {
                method: "GET",
                mode: "cors",
                headers: {
                    "Content-Type": "application/json"
                }
            }
        )
            .then(async (response) => {
                if (!response.ok) {
                    const res = await response.json()
                    setPopupMessage(res.message);
                    throw new Error(`HTTP Error! Status: ${response.status}`);
                }
                return response.json();
            })
            .then((data) => {
                const localEvents = data.data.map((item: any) => {
                    item.event_form_schema["fields"].map((item: any) => {
                        if (item.type === 'INPUT_STR') {
                            item.type = QuestionType.INPUT_STR
                        }
                        else if (item.type === 'INPUT_INT') {
                            item.type = QuestionType.INPUT_INT
                        }
                        else if (item.type === 'INPUT_FLOAT') {
                            item.type = QuestionType.INPUT_FLOAT
                        }
                        else if (item.type === 'MULTIPLE_CHOICE') {
                            item.type = QuestionType.MULTIPLE_CHOICE
                        }
                        else if (item.type === 'DROPDOWN') {
                            item.type = QuestionType.DROPDOWN
                        }
                        else if (item.type === 'DYNAMIC_INPUT_STR') {
                            item.type = QuestionType.DYNAMIC_INPUT_STR
                        }
                    })
                    if (item.id === SearchBar()) {
                        setSelectedEvent(item)

                    }
                    return item;
                })
                setEvents(localEvents);
                setIsLoadingSpinner(false);
            })
            .catch((error) => {
                setIsLoadingSpinner(false);
                (document.getElementById('my_modal_1') as any).showModal()
            });
    };

    const sendFormData = async (user: any, formData: any, eventId: any) => {
        try {
            const response = await fetch(`${BASE_URL}/api/v1/vendor-app/register-event`, {
                method: "POST",
                mode: "cors",
                headers: {
                    "Content-Type": "application/json"
                },
                body: JSON.stringify({
                    event_id: eventId,
                    event_form_data: formData,
                    full_name: formData.fields[0].answer,
                    phone_number: formData.fields[1].answer,
                    email: formData.fields[2].answer,
                }),
            });

            if (!response.ok) {
                const res = await response.json();
                setPopupMessage(res.message);
                setIsLoadingSpinner(false);
                throw new Error(`HTTP Error! Status: ${response.status}`);
            }

            const data = await response.json();
            setPopupMessage(data.message + '.' + '\n' + 'Redirecting to payment invoice.');
            setIsLoadingSpinner(false);
            (document.getElementById('my_modal_2') as any).showModal()
            window.location.href = data.data.checkout_url;
        } catch (error) {
            (document.getElementById('my_modal_1') as any).showModal()
            setIsLoadingSpinner(false);
        }
    };

    const submitForm = () => {
        setIsLoadingSpinner(true);

        const outputList = Object.entries(formResponses).map(([question, answer]) => ({ question, answer }));

        let formattedResponses: any = outputList.filter((response) => response !== undefined);
        formattedResponses = { fields: formattedResponses }

        console.log(formattedResponses);
        return;

        sendFormData(user, formattedResponses, selectedEvent?.id)
    };

    const buildInput = (schemaItem: EventFormSchemaItem, index: any) => {

        const handleInputChange: any = (e: any, question = null, option = null) => {
            let value;
            if (schemaItem.type === QuestionType.MULTIPLE_CHOICE) {
                const clickedOption: any = checkedOptions.indexOf(option);
                let all: any = [...checkedOptions];
                if (clickedOption === -1) {
                    all.push(option);
                } else {
                    all.splice(clickedOption, 1);
                }
                setCheckedOptions(all);
                all = all.join(",")
                const updatedResponses: any = { ...formResponses, [schemaItem.question]: all };
                setFormResponses(updatedResponses);
            }
            else if (schemaItem.type === QuestionType.INPUT_STR && index === 1) {
                value = e.target.value;
                setPhoneNumber(value);
                const phoneNumberPattern = /^\+92\d{10}$/;
                setIsValidPhoneNumber(phoneNumberPattern.test(value));
                const updatedResponses: any = { ...formResponses, [schemaItem.question]: value };
                setFormResponses(updatedResponses);
            }
            else if (schemaItem.type === QuestionType.INPUT_STR && index === 2) {
                value = e.target.value;
                setEmail(value);
                const emailPattern = /^[A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,4}$/i;
                setIsValidEmail(emailPattern.test(value));
                const updatedResponses: any = { ...formResponses, [schemaItem.question]: value };
                setFormResponses(updatedResponses);
            }
            else if (schemaItem.type === QuestionType.DYNAMIC_INPUT_STR && question === null) {
                value = e.target.value;
                const updatedResponses: any = { ...formResponses, [schemaItem.question]: value };
                const dis = { ...dynamicInputStrs, [index]: Number(value) }
                setDynamicInputStrs(dis)
                setFormResponses(updatedResponses);
            }
            else if (schemaItem.type === QuestionType.DYNAMIC_INPUT_STR) {
                value = e.target.value;
                const updatedResponses: any = { ...formResponses, [question!]: value };
                setFormResponses(updatedResponses);
            }
            else {
                value = e.target.value;
                const updatedResponses: any = { ...formResponses, [schemaItem.question]: value };
                setFormResponses(updatedResponses);
            }

        };

        if (schemaItem.type === QuestionType.INPUT_STR) {
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
            if (index === 1) {
                return (
                    <form>
                        <input
                            type="text"
                            className={`input input-bordered w-full max-w-xs`}
                            onChange={handleInputChange}
                            placeholder={"+92XXXXXXXXXX"}
                        />
                        {!isValidPhoneNumber && (
                            <div className="error-message">Please enter a valid phone number</div>
                        )}
                    </form>
                )
            }
            if (index === 2) {
                return (
                    <form>
                        <input
                            type="text"
                            className={`input input-bordered w-full max-w-xs`}
                            onChange={handleInputChange}
                            placeholder={"coolemail@gmail.com"}
                        />
                        {!isValidEmail && (
                            <div className="error-message">Please enter a valid email.</div>
                        )}
                    </form>
                )
            }
            return (
                <form>
                    <input
                        type="text"
                        className="input input-bordered w-full max-w-xs"
                        onChange={handleInputChange}
                    />
                </form>
            )
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
        if (schemaItem.type === QuestionType.DYNAMIC_INPUT_STR) {
            return (
                <div className="form-control">
                    <input type="number" className="input input-bordered w-full max-w-xs" onChange={handleInputChange} />

                    {Array.from({ length: dynamicInputStrs[index] }, (_, i) => i + 1).map((option, j) => (
                        schemaItem.options.map((elem, k) => (
                            <div key={k}>
                                <label className="label">
                                    <span className="label-text">{elem + ' ' + (j + 1).toString()}</span>
                                </label>
                                <input
                                    type="text"
                                    className="input input-bordered w-full max-w-xs"
                                    onChange={(e) => handleInputChange(e, elem + ' ' + (j + 1))}
                                />
                            </div>
                        ))
                    ))}
                </div>
            )
        }

    }

    return <div className="flex min-h-screen flex-col items-center p-2">
        <h3 className="" >REGISTER EVENT</h3>

        <select className="select select-bordered mt-4 mb-4"
            value={selectedEvent?.name}
            onChange={handleSelectChange}
        >
            <option value="">Select an event</option>
            {events.map((event, i) => (
                <option key={i} value={event.id}>
                    {event.name}
                </option>
            ))}
        </select>

        {selectedEvent && (
            <p><b>EVENT:</b> {selectedEvent.name}</p>
        )}

        {
            selectedEvent?.event_form_schema && (
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
            )
        }

        <button className="m-4 btn bg-white" onClick={submitForm} disabled={!isValidPhoneNumber || !isValidEmail}>Submit</button>

        {isLoadingSpinner && <LoadingOverlay />}

        <dialog id="my_modal_1" className="modal">
            <div className="modal-box">
                <h3 className="font-bold text-lg">
                    <span className="error">
                        Error
                    </span>
                </h3>
                <p className="py-4 error">{popupMessage}</p>
                <div className="modal-action">
                    <form method="dialog">
                        <button className="btn">Close</button>
                    </form>
                </div>
            </div>
        </dialog>

        <dialog id="my_modal_2" className="modal">
            <div className="modal-box">
                <h3 className="font-bold text-lg">
                    <span className="success">
                        Success
                    </span>
                </h3>
                <p className="py-4 success">{popupMessage}</p>
                <div className="modal-action">
                    <form method="dialog">
                        <button className="btn">Close</button>
                    </form>
                </div>
            </div>
        </dialog>

    </div>
}