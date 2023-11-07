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
  created_at: string;
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

interface UnpaidRegistration {
  form_data: {
    "question": string;
    "answer": string;
  }[];
  attendance_status: string;
  event_name: string;
  created_at: string;
  amount: number;
}

const BASE_URL_PROD = 'https://cardpay-1.el.r.appspot.com';
const BASE_URL_DEV = 'https://dev-dot-cardpay-1.el.r.appspot.com';
const BASE_URL_LOCAL = 'http://127.0.0.1:5000';
const BASE_URL = BASE_URL_PROD;

export default function page() {
  const router = useRouter();
  const [user, setUser] = useState<FirebaseUser | null>(null);
  const [externalRegistrations, setExternalRegistrations] = useState<Registration[]>([]);
  const [internalRegistrations, setInternalRegistrations] = useState<InternalRegistration[]>([]);
  const [unpaidRegistrations, setUnpaidRegistrations] = useState<UnpaidRegistration[]>([]);
  const [isFetching, setIsFetching] = useState<boolean>(true);
  const [tabSelected, setTabSelected] = useState<number>(0);
  const [balance, setBalance] = useState<number>(0);
  const [vendor_name, setVendorName] = useState<string>("");
  const [maxIndex, setMaxIndex] = useState(0);

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
        const retrieved_registrations = data.data.external_registrations as Array<Registration>;
        const internal_registrations = data.data.internal_registrations as Array<InternalRegistration>;
        const unpaid_registrations = data.data.unpaid_registrations as Array<UnpaidRegistration>;

        let maxLength = 0;
        let maxIndex = 0;

        retrieved_registrations.map((item, index) => {
          if (item.form_data.length >= maxLength) {
            maxIndex = index
          }
        })
        setMaxIndex(maxIndex)

        setExternalRegistrations(retrieved_registrations);
        setInternalRegistrations(internal_registrations);
        setUnpaidRegistrations(unpaid_registrations);
        setIsFetching(false);
      })
      .catch((error) => {
        console.error("Error fetching data:", error);
      });
  };

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
              {internalRegistrations.map((registration, index) => (
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
                <th>Status</th>
                <th>Attendance status</th>
                <th>Amount</th>
                <th>Created at</th>
                {externalRegistrations.length !== 0 ? externalRegistrations[maxIndex].form_data.map((form_data, index) => (
                  <th key={index}>
                    {form_data.question}
                  </th>
                )) : null}
              </tr>
            </thead>
            <tbody>
              {externalRegistrations.map((reg, index) => (
                <tr
                  key={index}
                >
                  <td>{reg.event_name}</td>
                  <td>{reg.status}</td> 
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
                {unpaidRegistrations.length !== 0 ? unpaidRegistrations[0].form_data.map((form_data, index) => (
                  <th key={index}>
                    {form_data.question}
                  </th>
                )) : null}
              </tr>
            </thead>
            <tbody>
              {unpaidRegistrations.map((reg, index) => (
                <tr
                  key={index}
                >
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
