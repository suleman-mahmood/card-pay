"use client";
/* eslint-disable */
import React from "react";
import { useEffect, useState } from "react";
import { useRouter } from "next/navigation";
import { User as FirebaseUser } from "firebase/auth";
import LoadingOverlay from "../spinner";
import { useSearchParams } from 'next/navigation'

import '../../globals.css'
import { BASE_URL } from "@/services/remote-config";
import { ref, uploadBytes, getDownloadURL } from "firebase/storage";
import { storage } from "@/services/initialize-firebase";

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
    FILE_UPLOAD
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
    const [isLumsEmail, setIsLumsEmail] = useState(false);
    const [dynamicInputStrs, setDynamicInputStrs] = useState<{ [name: string]: string }>({});

    useEffect(() => {
        fetchEvents();
    }, []);

    const SearchBar = () => {
        const search = searchParams.get('event_id')
        return search;
    }

    const uploadToFirebase = async (file: any) => {
        setIsLoadingSpinner(true);
        const storageRef = ref(storage, 'images/' + crypto.randomUUID());
        const snapshot = await uploadBytes(storageRef, file);
        const download_url = await getDownloadURL(snapshot.ref)
        setIsLoadingSpinner(false);
        return download_url;
    }

    const handleSelectChange = (event: any) => {
        console.log(event)
        events.map((item) => {
            if (event === item.id) {
                setSelectedEvent(item);
                if (event === '1ba4c981-5d98-431c-84bf-67ad8d8cc0a9') {
                    setIsLumsEmail(true)
                }
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
                    item.event_start_timestamp = new Date(item.event_start_timestamp);
                    item.event_start_timestamp = `${getDayName(item.event_start_timestamp)}, ${getTwoDigitDay(item.event_start_timestamp)} ${getMonthName(item.event_start_timestamp)} ${item.event_start_timestamp.getFullYear()} ${get12HourTime(item.event_start_timestamp)}`

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
                        else if (item.type === 'FILE_UPLOAD') {
                            item.type = QuestionType.FILE_UPLOAD
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

    function getDayName(date: any) {
        const days = ["Sun", "Mon", "Tue", "Wed", "Thu", "Fri", "Sat"];
        return days[date.getUTCDay()];
    }

    function getTwoDigitDay(date: any) {
        return ("0" + date.getUTCDate()).slice(-2);
    }

    function getMonthName(date: any) {
        const months = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"];
        return months[date.getUTCMonth()];
    }

    function get12HourTime(date: any) {
        const hours = date.getUTCHours() % 12 || 12;
        const minutes = ("0" + date.getUTCMinutes()).slice(-2);
        const period = date.getUTCHours() < 12 ? "AM" : "PM";
        return `${hours}:${minutes} ${period}`;
    }

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

        sendFormData(user, formattedResponses, selectedEvent?.id)
    };

    const buildInput = (schemaItem: EventFormSchemaItem, index: any) => {

        const handleInputChange: any = async (e: any, question: string | null = null, option = null) => {
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
                const lumsEmailPattern = /^[a-zA-Z0-9._%+-]+@lums\.edu\.pk$/i;
                if (selectedEvent?.id === '1ba4c981-5d98-431c-84bf-67ad8d8cc0a9') {
                    setIsValidEmail(lumsEmailPattern.test(value));
                }
                else {
                    setIsValidEmail(emailPattern.test(value));
                }
                const updatedResponses: any = { ...formResponses, [schemaItem.question]: value };
                setFormResponses(updatedResponses);
            }
            else if (schemaItem.type === QuestionType.DYNAMIC_INPUT_STR && question === null) {
                value = e.target.value;

                if (schemaItem.question === "Number of team members (excluding team lead) | Between 1-5") {
                    const newValue = parseInt(e.target.value);
                    if (newValue >= 1 && newValue <= 5) {
                        value = newValue.toString();
                    }
                    else {
                        value = newValue < 1 ? '1' : '5';
                    }
                }

                const updatedResponses: any = { ...formResponses, [schemaItem.question]: value };
                const dis = { ...dynamicInputStrs, [index]: Number(value) }
                setDynamicInputStrs(dis)
                setFormResponses(updatedResponses);
            }
            else if (schemaItem.type === QuestionType.DYNAMIC_INPUT_STR) {
                if (question?.indexOf("Photograph") !== -1) {
                    const file_to_upload = e.target.files[0];
                    value = await uploadToFirebase(file_to_upload);
                }
                else {
                    value = e.target.value
                };

                const updatedResponses: any = { ...formResponses, [question!]: value };
                setFormResponses(updatedResponses);
            }
            else if (schemaItem.type === QuestionType.FILE_UPLOAD) {
                const file_to_upload = e.target.files[0];
                const download_url = await uploadToFirebase(file_to_upload);
                const updatedResponses: any = { ...formResponses, [schemaItem.question]: download_url };
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
                        {isLumsEmail ? (
                            <div>
                                {!isValidEmail && (
                                    <div className="error-message">Please enter a valid LUMS email address.</div>
                                )}
                            </div>
                        ) : <div>
                            {!isValidEmail && (
                                <div className="error-message">Please enter a valid email.</div>
                            )}
                        </div>
                        }
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
        if (schemaItem.type === QuestionType.FILE_UPLOAD) {
            return (
                <input type="file" className="file-input file-input-bordered w-full max-w-xs" id="file-dynamic" onChange={(e) => handleInputChange(e)} />
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

                    {Array.from({ length: Number(dynamicInputStrs[index]) }, (_, i) => i + 1).map((option, j) => (
                        schemaItem.options.map((elem, k) => (
                            <div key={k}>
                                <label className="label">
                                    <span className="label-text">{elem + ' ' + (j + 1).toString()}</span>
                                </label>
                                {
                                    elem.toString() === "Photograph" ? (
                                        <input type="file" className="file-input file-input-bordered w-full max-w-xs" onChange={(e) => handleInputChange(e, elem + ' ' + (j + 1))} />
                                    ) : <input
                                        type="text"
                                        className="input input-bordered w-full max-w-xs"
                                        onChange={(e) => handleInputChange(e, elem + ' ' + (j + 1))}
                                    />
                                }
                            </div>
                        ))
                    ))}
                </div>
            )
        }

    }


    return <div className="flex min-h-screen flex-col items-center artboard xs:phone-3 events-all-page overflow-scroll">

        {
            !selectedEvent && (
                <h4 className="mt-2 text-2xl">Select Event</h4>
            )
        }

        {
            !selectedEvent && (
                <div className="carousel-vertical carousel-center max-w-md p-2 space-y-4 rounded-box w-full">
                    {events.map((event, i) => (
                        <div key={i} className="carousel-item w-full py-2 flex shadow rounded-xl" id={String("item" + i)}
                            onClick={() => handleSelectChange(event.id)}>
                            <img src={event.image_url} className="w-1/4 h-14 w-14 rounded-xl ml-2" />
                            <div className="flex flex-col w-3/4 justify-center rounded ml-2">
                                <div className="event-start text-xs">
                                    {event.event_start_timestamp}
                                </div>
                                <div className="text-sm">
                                    {event.name}
                                </div>
                                <div className="event-venue text-xs">
                                    {event.venue}
                                </div>
                            </div>
                        </div>
                    ))}
                </div>
            )
        }


        {selectedEvent && (
            <div className="items-center justify-center md:w-1/4 lg:h-25">
                <div className="btn back-button" onClick={() => window.location.reload()}>
                    ❮
                </div>
                <img src={selectedEvent.image_url} className="w-full rounded-xl" />
                <div className="text-center bg-white rounded-xl shadow w-full flex flex-col">
                    <b>{selectedEvent.name}</b>
                    <span className="text-sm">{selectedEvent.event_start_timestamp}</span>
                    <span className="text-xs event-venue">{selectedEvent.venue}</span>
                    <span className="text-sm event-start">Rs.{selectedEvent.registration_fee}</span>
                </div>

                <div className="flex flex-col p-3">
                    <div>
                        About
                    </div>
                    <span className="text-xs event-venue">
                        {selectedEvent.description}
                    </span>
                </div>
            </div>
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

        {
            selectedEvent && (
                <button className="m-4 btn bg-white" onClick={submitForm} disabled={!isValidPhoneNumber || !isValidEmail}>Submit</button>
            )
        }

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