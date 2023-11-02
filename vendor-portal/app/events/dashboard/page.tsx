"use client";
/* eslint-disable */

import React from "react";
import { useEffect, useState } from "react";
import { useRouter } from "next/navigation";
import { User as FirebaseUser } from "firebase/auth";
import { onAuthStateChanged } from "firebase/auth";
import { auth } from "../../../services/initialize-firebase";
import { TypeAnimation } from "react-type-animation";
import Link from "next/link";


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

const BASE_URL_PROD = 'https://cardpay-1.el.r.appspot.com';
const BASE_URL_DEV = 'https://dev-dot-cardpay-1.el.r.appspot.com';
const BASE_URL_LOCAL = 'http://127.0.0.1:5000';
const BASE_URL = BASE_URL_PROD;

export default function page() {
  const router = useRouter();
  const [user, setUser] = useState<FirebaseUser | null>(null);
  const [registrations, setRegistrations] = useState<Registration[]>([]);
  const [isFetching, setIsFetching] = useState<boolean>(true);
  const [balance, setBalance] = useState<number>(0);
  const [vendor_name, setVendorName] = useState<string>("");

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
        const retrieved_registrations = data.data as Array<Registration>;
        setRegistrations(retrieved_registrations);
        setIsFetching(false);
        console.log(retrieved_registrations);
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
    <div className="min-h-screen flex flex-col justify-between p-4">
      <Link href={"/events/mark-attendance"} className="btn">Mark attendance</Link>
      <h1 className="mb-2 text-4xl font-bold text-center text-violet-600">
        {vendor_name}
      </h1>
      <h1 className="mb-2 text-2xl font-bold text-center text-black">
        Transactions
      </h1>
      <h3 className="mb-2 text-md text-center text-violet-600">
        Balance: {balance}
      </h3>
      <div className="overflow-x-auto">
        <table className="table">
          <thead>
            <tr className="bg-white">
              {registrations.length !== 0 ? registrations[0].form_data.map((form_data, index) => (
                <th key={index}>
                  {form_data.question}
                </th>
              )) : null}
              {/* <th>Event name</th>
              <th>Status</th>
              <th>Attendance status</th>
              <th>Amount</th>
              <th>Created at</th> */}
            </tr>
          </thead>
          <tbody>
            {registrations.map((reg, index) => (
              <tr
                key={index}
              >
                {reg.form_data.map((form_data, index) => (
                  <td key={index}>
                    {form_data.answer}
                  </td>
                ))}
                {/* <td>{reg.event_name}</td>
                <td>{reg.status}</td> // Between we are only fetching successful invoices
                <td>{reg.attendance_status}</td>
                <td>{reg.amount}</td>
                <td>{reg.created_at}</td> */}
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
}
