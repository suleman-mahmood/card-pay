"use client";
/* eslint-disable */

import React from "react";
import { useEffect, useState } from "react";
import { useRouter } from "next/navigation";
import { User as FirebaseUser } from "firebase/auth";
import { onAuthStateChanged } from "firebase/auth";
import { auth } from "../../../services/initialize-firebase";
import { TypeAnimation } from "react-type-animation";

interface Registration {
  form_data: {
    "question": string;
    "answer": string;
  }[];
  attendance_status: string;
  event_name: string;
  created_at: any;
  amount: number;
  status: string;
}

interface InternalRegistration {
  id: string,
  full_name: string,
  personal_email: string,
  phone_number: string,
  event_name: string
}

interface internalGroupedData {
  [name: string]: InternalRegistration[]
}

interface externalGroupedData {
  [name: string]: Registration[]
}

interface unpaidGroupedData {
  [name: string]: UnpaidRegistration[]
}

interface UnpaidRegistration {
  form_data: {
    "question": string;
    "answer": string;
  }[];
  attendance_status: string;
  event_name: string;
  created_at: any;
  amount: number;
}

const BASE_URL_PROD = 'https://cardpay-1.el.r.appspot.com';
const BASE_URL_DEV = 'https://dev-dot-cardpay-1.el.r.appspot.com';
const BASE_URL_LOCAL = 'http://127.0.0.1:5000';
const BASE_URL = BASE_URL_PROD;

export default function page() {
  const router = useRouter();
  const [user, setUser] = useState<FirebaseUser | null>(null);
  const [externalRegistrations, setExternalRegistrations] = useState<externalGroupedData>({});
  const [internalRegistrations, setInternalRegistrations] = useState<internalGroupedData>({});
  const [unpaidRegistrations, setUnpaidRegistrations] = useState<unpaidGroupedData>({});
  const [isFetching, setIsFetching] = useState<boolean>(true);
  const [tabSelected, setTabSelected] = useState<number>(0);
  const [balance, setBalance] = useState<number>(0);
  const [vendor_name, setVendorName] = useState<string>("");
  const [maxIndexUnpaid, setMaxIndexUnpaid] = useState(0);
  const [maxIndexExternal, setMaxIndexExternal] = useState(0);
  const [allEvents, setAllEvents] = useState<string[]>([]);
  const [selectedOption, setSelectedOption] = useState('');

  useEffect(() => {
    return onAuthStateChanged(auth, (user: any) => {
      if (user) {
        setUser(user);
        fetchRegistrations(user);
        fetchVendorBalance(user);
        fetchVendor(user);
      } else {
        router.push("/");
      }
    });
  }, []);

  const handleSelectChange = (event: any) => {
    const selectedValue = event.target.value;
    setSelectedOption(selectedValue);
  };

  const fetchRegistrations = async (user: FirebaseUser) => {
    const token = await user?.getIdToken();
    fetch(
      `${BASE_URL}/api/v1/vendor-app/get-society-registrations`,
      {
        method: "GET",
        mode: "cors",
        headers: {
          "Content-Type": "application/json",
          Authorization: `Bearer ${token}`,
        },
      }
    )
      .then((response) => {
        if (!response.ok) {
          throw new Error(`HTTP Error! Status: ${response.status}`);
        }
        return response.json();
      })
      .then((data) => {
        const external_registrations = data.data.external_registrations as Array<Registration>;
        const internal_registrations = data.data.internal_registrations as Array<InternalRegistration>;
        const unpaid_registrations = data.data.unpaid_registrations as Array<UnpaidRegistration>;

        unpaid_registrations.map((item, index) => {
          item.created_at = new Date(item.created_at);
          item.created_at = `${getDayName(item.created_at)}, ${getTwoDigitDay(item.created_at)} ${getMonthName(item.created_at)} ${item.created_at.getFullYear()} ${get12HourTime(item.created_at)}`
        })

        external_registrations.map((item, index) => {
          item.created_at = new Date(item.created_at);
          item.created_at = `${getDayName(item.created_at)}, ${getTwoDigitDay(item.created_at)} ${getMonthName(item.created_at)} ${item.created_at.getFullYear()} ${get12HourTime(item.created_at)}`
        })

        const unpaidGroupedData : unpaidGroupedData = {};
        const internalGroupedData : internalGroupedData = {};
        const externalGroupedData : externalGroupedData = {};

        unpaid_registrations.forEach((obj: UnpaidRegistration) => {
          const eventName : string = obj.event_name;

          if (!unpaidGroupedData[eventName]) {
            unpaidGroupedData[eventName] = [];
          }

          unpaidGroupedData[eventName].push(obj);
        });

        internal_registrations.forEach((obj: InternalRegistration) => {
          const eventName = obj.event_name;

          if (!internalGroupedData[eventName]) {
            internalGroupedData[eventName] = [];
          }

          internalGroupedData[eventName].push(obj);
        });

        external_registrations.forEach((obj: Registration) => {
          const eventName = obj.event_name;

          if (!externalGroupedData[eventName]) {
            externalGroupedData[eventName] = [];
          }

          externalGroupedData[eventName].push(obj);
        });

        const keysUnion = Array.from(
          new Set([...Object.keys(unpaidGroupedData), ...Object.keys(internalGroupedData), ...Object.keys(externalGroupedData)])
        );

        setSelectedOption(keysUnion[0])
        setAllEvents(keysUnion)
        setExternalRegistrations(externalGroupedData);
        setInternalRegistrations(internalGroupedData);
        setUnpaidRegistrations(unpaidGroupedData);
        setIsFetching(false);
      })
      .catch((error) => {
        console.error("Error fetching data:", error);
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

  const fetchVendorBalance = async (user: FirebaseUser) => {
    const token = await user?.getIdToken();
    fetch(
      `${BASE_URL}/api/v1/vendor-app/get-vendor-balance`,
      {
        method: "GET",
        mode: "cors",
        headers: {
          "Content-Type": "application/json",
          Authorization: `Bearer ${token}`,
        },
      }
    )
      .then((response) => {
        if (!response.ok) {
          throw new Error(`HTTP Error! Status: ${response.status}`);
        }
        return response.json();
      })
      .then((data) => {
        const retrieved_balance = data.data.balance;
        setBalance(retrieved_balance);
      })
      .catch((error) => {
        console.error("Error fetching data:", error);
      });
  };

  const fetchVendor = async (user: FirebaseUser) => {
    const token = await user?.getIdToken();
    fetch(`${BASE_URL}/api/v1/vendor-app/get-vendor`, {
      method: "GET",
      mode: "cors",
      headers: {
        "Content-Type": "application/json",
        Authorization: `Bearer ${token}`,
      },
    })
      .then((response) => {
        if (!response.ok) {
          throw new Error(`HTTP Error! Status: ${response.status}`);
        }
        return response.json();
      })
      .then((data) => {
        const vendor_name = data.data.full_name;
        setVendorName(vendor_name);
      })
      .catch((error) => {
        console.error("Error fetching data:", error);
      });
  };

  return isFetching ? (
    <div className="flex min-h-screen flex-col items-center justify-between p-24">
      <TypeAnimation
        sequence={[
          // Same substring at the start will only be typed out once, initially
          "CardPay",
          1000,
          "Payment Sirf CardPay",
          1000,
          "Thora Intezar Farmaein",
          1000,
        ]}
        wrapper="span"
        speed={60}
        style={{ fontSize: "2em", display: "inline-block" }}
        repeat={Infinity}
      />
    </div>
  ) : (
    <div className="min-h-screen flex flex-col p-4">
      <h1 className="mb-2 text-2xl font-bold text-center text-violet-600">
        {vendor_name}
      </h1>

      <div className="w-full items-center justify-center">
        <select className="select select-bordered w-full max-w-xs" placeholder="Select Event"
          value={selectedOption} onChange={handleSelectChange}>
          {
            allEvents.map((item, index) => (
              <option key={index} value={item}>
                {item}
              </option>
            )
            )
          }
        </select>
      </div>


      <h3 className="mb-2 text-xl text-center text-violet-600">
        Balance: {balance}
      </h3>

      <div className="tabs tabs-boxed flex flex-row  justify-center">
        <a className={"tab " + (tabSelected === 0 ? 'tab-active' : '')} onClick={() => setTabSelected(0)}>Internal Registrations</a>
        <a className={"tab " + (tabSelected === 1 ? 'tab-active' : '')} onClick={() => setTabSelected(1)}>External Registrations</a>
        <a className={"tab " + (tabSelected === 2 ? 'tab-active' : '')} onClick={() => setTabSelected(2)}>Unpaid Registrations</a>
      </div>

      {tabSelected === 0 ? (
        <div className="overflow-x-auto">
          <table className="table">
            <thead>
              <tr>
                <th>Full Name</th>
                <th>Email</th>
                <th>Phone Number</th>
                <th>Event Name</th>
              </tr>
            </thead>
            <tbody>
              {internalRegistrations[selectedOption].map((registration, index) => (
                <tr key={index}>
                  <td>{registration.full_name}</td>
                  <td>{registration.personal_email}</td>
                  <td>{registration.phone_number}</td>
                  <td>{registration.event_name}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      ) : null}

      {tabSelected === 1 ? (
        <div className="overflow-x-auto">
          <table className="table">
            <thead>
              <tr className="bg-white">
                <th>Event name</th>
                <th>Attendance status</th>
                <th>Amount</th>
                <th>Created at</th>
                {externalRegistrations[selectedOption].length !== 0 ? externalRegistrations[selectedOption][maxIndexExternal].form_data.map((form_data, index) => (
                  <th key={index}>
                    {form_data.question}
                  </th>
                )) : null}
              </tr>
            </thead>
            <tbody>
              {externalRegistrations[selectedOption].map((reg, index) => (
                <tr
                  key={index}
                >
                  <td>{reg.event_name}</td>
                  <td>{reg.attendance_status}</td>
                  <td>{reg.amount}</td>
                  <td>{reg.created_at}</td>
                  {reg.form_data.map((form_data, index) => (
                    <td key={index}>
                      {form_data.answer}
                    </td>
                  ))}
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      ) : null}


      {tabSelected === 2 ? (
        <div className="overflow-x-auto">
          <table className="table">
            <thead>
              <tr className="bg-white">
                <th>Event name</th>
                <th>Attendance status</th>
                <th>Amount</th>
                <th>Created at</th>
                {unpaidRegistrations[selectedOption].length !== 0 ? unpaidRegistrations[selectedOption][maxIndexUnpaid].form_data.map((form_data, index) => (
                  <th key={index}>
                    {form_data.question}
                  </th>
                )) : null}
              </tr>
            </thead>
            <tbody>
              {unpaidRegistrations[selectedOption].map((reg, index) => (
                <tr
                  key={index}
                >
                  <td>{reg.event_name}</td>
                  <td>{reg.attendance_status}</td>
                  <td>{reg.amount}</td>
                  <td>{reg.created_at}</td>
                  {reg.form_data.map((form_data, index) => (
                    <td key={index}>
                      {form_data.answer}
                    </td>
                  ))}
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      ) : null}
    </div>
  );
}
