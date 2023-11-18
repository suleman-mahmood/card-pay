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
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import { faCheck, faTrash, faX } from "@fortawesome/free-solid-svg-icons";

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
    full_name?: string,
    unique_identifier?: string
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
  const [isLoadingSpinner, setIsLoadingSpinner] = useState(false);
  const [isMarkingAttendance, setIsMarkingAttendance] = useState(false);

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
      (result: any) => {
        let x: string = result.data;
        x = x.replace(/['"]+/g, '"')
        let json_data: { "qr_id": string }
        if (x.includes("qr_id")) {
          json_data = JSON.parse(x)
          markAttendance(json_data.qr_id, qrScanner)
        }
        else {
          markAttendance(x, qrScanner)
        }

        qrScanner.pause();
      },
      {}
    );

    qrScanner.start();
  }, [isFetching]);

  const markAttendance = async (qr_id: string, qrScanner: QrScanner) => {
    if (isMarkingAttendance) return
    setIsMarkingAttendance(true);

    setIsLoadingSpinner(true);
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
            qr_id: qr_id
          }
        )
      }
    )
      .then(async (response) => {
        if (!response.ok) {
          const res = await response.json();
          setError(res.message);
          setIsMarkingAttendance(false);
          setIsFetching(false);
          setIsLoadingSpinner(false);
          setIsErrorModalOpen(true);
          qrScanner.start();
          throw new Error(`HTTP Error! Status: ${response.status}`);
        }
        return response.json();
      })
      .then((data) => {
        setIsMarkingAttendance(false);
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
        <h1 className="w-full text-center" >Mark attendance</h1>

        <video></video>

        {isLoadingSpinner && <LoadingOverlay />}

        <dialog className={'modal ' + (isModalOpen ? 'modal-open' : '')}>
          <form method='dialog' className='modal-box text-center items-center justify-center'>
            <h5><b>Attendance Status</b></h5>
            {res?.already_marked ? (
              <FontAwesomeIcon
                icon={faX}
                className="fas fa-x"
                style={{ color: "red", fontSize: 64 }}
              />
            ) : (
              <FontAwesomeIcon
                icon={faCheck}
                className="fas fa-check"
                style={{ color: "green", fontSize: 64 }}
              />
            )}
            {res?.already_marked ? (
              <div className="mt-4 error-message">Already marked</div>
            ) : (
              <div></div>
            )}
            <div className="mt-2"><b>Event Name: </b>{res?.attendance_data.event_name}</div>
            {
              res?.attendance_data.full_name ? <div><b>Name:</b> {res?.attendance_data.full_name}</div> : null
            }
            {
              res?.attendance_data.unique_identifier ? <div><b>Roll Number:</b> {res?.attendance_data.unique_identifier}</div> : null
            }
            {
              res?.attendance_data.form_data.map((item: any, index: any) => (
                <div className="mt-2" key={index}><b>{item.question}: </b>{item.answer}</div>
              ))
            }
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
            <FontAwesomeIcon
              icon={faX}
              className="fas fa-x"
              style={{ color: "red", fontSize: 64 }}
            />
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
