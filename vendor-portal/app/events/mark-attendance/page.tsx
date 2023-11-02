"use client";
/* eslint-disable */

import React from "react";
import { useEffect, useState } from "react";
import { useRouter } from "next/navigation";
import { User as FirebaseUser } from "firebase/auth";
import { onAuthStateChanged } from "firebase/auth";
import { auth } from "../../../services/initialize-firebase";
import { TypeAnimation } from "react-type-animation";
import QrScanner from 'qr-scanner';
import LoadingOverlay from "../spinner";

const BASE_URL_PROD = 'https://cardpay-1.el.r.appspot.com';
const BASE_URL_DEV = 'https://dev-dot-cardpay-1.el.r.appspot.com';
const BASE_URL_LOCAL = 'http://127.0.0.1:5000';
const BASE_URL = BASE_URL_PROD;

interface MarkAttendanceResponse {
  attendance_data: {
    form_data: {
      "question": string;
      "answer": string;
    }[];
    attendance_status: string;
    event_name: string;
    registration_fee: number;
  }
  already_marked: boolean,
}

export default function page() {
  const router = useRouter();
  const [user, setUser] = useState<FirebaseUser | null>(null);
  const [isFetching, setIsFetching] = useState<boolean>(true);
  const [isModalOpen, setIsModalOpen] = useState(false);
  const [isErrorModalOpen, setIsErrorModalOpen] = useState(false);
  const [res, setRes] = useState<MarkAttendanceResponse>();
  const [error, setError] = useState();
  const [isLoadingSpinner, setIsLoadingSpinner] = useState(true);

  useEffect(() => {
    return onAuthStateChanged(auth, (user: any) => {
      if (user) {
        setUser(user);
        setIsFetching(false);
      } else {
        router.push("/");
      }
    });
  }, []);

  useEffect(() => {
    if (document === null) return;

    const videoElem = document.querySelector('video');
    if (videoElem === null) return;

    const qrScanner = new QrScanner(
      videoElem,
      (result) => {
        let x = result.data;
        x = x.replace(/['"]+/g, '"')
        console.log(JSON.parse(x))

        const json_data: { "event_id": string, "qr_id": string } = JSON.parse(x)

        markAttendance(json_data.event_id, json_data.qr_id, qrScanner)

        // markAttendance("65e2263f-2953-497d-be63-05c31f88274c", "f76c6f08-d28b-4de3-ba65-0ae7a3c2cef6", qrScanner)

        qrScanner.pause();
      },
      {}
    );

    qrScanner.start();
  }, [isFetching]);

  const markAttendance = async (event_id: string, qr_id: string, qrScanner: QrScanner) => {
    const token = await user?.getIdToken();
    fetch(
      `${BASE_URL}/api/v1/vendor-app/mark-entry-event-attendance`,
      {
        method: "POST",
        mode: "cors",
        headers: {
          "Content-Type": "application/json",
          Authorization: `Bearer ${token}`,
        },
        body: JSON.stringify(
          {
            event_id: event_id,
            qr_id: qr_id
          }
        )
      }
    )
      .then(async (response) => {
        if (!response.ok) {
          const res = await response.json();
          setError(res.message);
          setIsFetching(false);
          setIsLoadingSpinner(false);
          setIsErrorModalOpen(true);
          qrScanner.start();
          throw new Error(`HTTP Error! Status: ${response.status}`);
        }
        return response.json();
      })
      .then((data) => {
        setIsFetching(false);
        setRes(data.data);
        setIsLoadingSpinner(false);
        setIsModalOpen(true);
        qrScanner.start();
      })
      .catch((error) => {
        console.error("Error fetching data:", error);
      });
  };

  return isFetching ? (
    <div className="flex min-h-screen flex-col items-center justify-between p-24">
      <TypeAnimation
        sequence={[
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
    <div className="flex min-h-screen flex-col items-center justify-between p-4">
      <div className="overflow-x-auto">
        <h1 className="" >Mark attendance</h1>

        <video></video>

        <dialog className={'modal ' + (isModalOpen ? 'modal-open' : '')}>
          <form method='dialog' className='modal-box'>
            <h5><b>Attendance Status</b></h5>
            {res?.already_marked ? (
              <div className="mt-4 success">Already marked</div>
            ) : (
              <div></div>
            )}
            <div className="mt-2"><b>Event Name: </b>{res?.attendance_data.event_name}</div>
            <div className="mt-2"><b>Name: </b>{res?.attendance_data.form_data[0].answer}</div>
            <div className="mt-2"><b>Phone Number: </b>{res?.attendance_data.form_data[1].answer}</div>
            <div className="mt-2"><b> Email: </b>{res?.attendance_data.form_data[2].answer}</div>
            <div className="mt-2 success"><b>Status: </b>{res?.attendance_data.attendance_status}</div>
            <div
              className='modal-action'
              onClick={() => setIsModalOpen(false)}
            >
              <button
                className='btn'
                onClick={() => setIsModalOpen(false)}
              >
                Cancel
              </button>
            </div>
          </form>

          {isLoadingSpinner && <LoadingOverlay />}
        </dialog>

        <dialog className={'modal ' + (isErrorModalOpen ? 'modal-open' : '')}>
          <form method='dialog' className='modal-box'>
            <h5><b>Attendance Status</b></h5>
            <div className="error-message"><b>Error: </b> {error}</div>
            <div
              className='modal-action'
              onClick={() => setIsErrorModalOpen(false)}
            >
              <button
                className='btn'
                onClick={() => setIsErrorModalOpen(false)}
              >
                Cancel
              </button>
            </div>
          </form>
          {isLoadingSpinner && <LoadingOverlay />}
        </dialog>
      </div>
    </div>
  );
}
