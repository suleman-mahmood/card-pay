"use client";
/* eslint-disable */
import React from "react";
import { useEffect, useState } from "react";

import '../globals.css'
import Link from "@/node_modules/next/link";

export default function page() {
    const [animate, setAnimate] = useState(false);

    useEffect(() => {
        const timeout = setTimeout(() => {
            setAnimate(true);
        }, 500);

        return () => clearTimeout(timeout);
    }, []);


    return <div className={`flex min-h-screen flex-col items-center justify-center p-5 artboard xs:phone-3 events-page overflow-scroll ${animate ? 'animate' : ''}`}>

        <img src={'../../cardpay.png'} />

        <div className="text-2xl text-white">Welcome To CardPay</div>

        <div className="text-lg text-white">Your one stop ticketing platform</div>

        <Link href={"/events/all"} className="btn mt-4">Browse Events</Link>

    </div>
}