"use client";
/* eslint-disable */
import React from "react";
import { useEffect, useState } from "react";
import { useRouter } from "next/navigation";
import { User as FirebaseUser } from "firebase/auth";
import LoadingOverlay from "./spinner";
import { useSearchParams } from 'next/navigation'

import '../globals.css'
import Link from "@/node_modules/next/link";

export default function page() {
    const router = useRouter();
    const [isLoadingSpinner, setIsLoadingSpinner] = useState(false);
    const [animate, setAnimate] = useState(false);

    useEffect(() => {
        const timeout = setTimeout(() => {
            setAnimate(true);
        }, 500);

        return () => clearTimeout(timeout);
    }, []);


    return <div className={`flex min-h-screen flex-col items-center justify-center p-5 artboard phone-3 events-page overflow-scroll ${animate ? 'animate' : ''}`}>

        <img src={'../../cardpay.png'} />

        <div className="text-2xl text-white">Welcome To CardPay</div>

        <div className="text-lg text-white">Your one stop ticketing platform</div>

        <Link href={"/events/all"} className="btn mt-4">Browse Events</Link>

    </div>
}