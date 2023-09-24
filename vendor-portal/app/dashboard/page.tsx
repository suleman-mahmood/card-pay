"use client";
/* eslint-disable */

import React from "react";
import { useEffect, useState } from "react";
import { useRouter } from "next/navigation";
import { User as FirebaseUser } from "firebase/auth";
import { onAuthStateChanged } from "firebase/auth";
import { auth } from "../../services/initialize-firebase";
import Table from "./components/Table";
import { TypeAnimation } from "react-type-animation";

export interface Transaction {
  amount: number;
  created_at: string;
  last_updated: string;
  sender_name: string;
}

export default function page() {
  const router = useRouter();
  const [user, setUser] = useState<FirebaseUser | null>(null);
  const [txns, setTxns] = useState<Transaction[]>([]);
  const [isFetching, setIsFetching] = useState<boolean>(true);
  const [balance, setBalance] = useState<number>(0);
  const [vendor_name, setVendorName] = useState<string>("");

  useEffect(() => {
    return onAuthStateChanged(auth, (user: any) => {
      if (user) {
        setUser(user);
        fetchTransactions(user);
        fetchVendorBalance(user);
        fetchVendor(user);
      } else {
        router.push("/");
      }
    });
  }, []);

  const fetchTransactions = async (user: FirebaseUser) => {
    const token = await user?.getIdToken();
    fetch(
      `https://cardpay-1.el.r.appspot.com/api/v1/vendor-app/get-vendor-transactions-to-be-reconciled`,
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
        const retrieved_txns = data.data as Array<Transaction>;
        setTxns(retrieved_txns);
        setIsFetching(false);
      })
      .catch((error) => {
        console.error("Error fetching data:", error);
      });
  };

  const fetchVendorBalance = async (user: FirebaseUser) => {
    const token = await user?.getIdToken();
    fetch(
      `https://cardpay-1.el.r.appspot.com/api/v1/vendor-app/get-vendor-balance`,
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
    fetch(`https://cardpay-1.el.r.appspot.com/api/v1/vendor-app/get-vendor`, {
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
    <div className="flex min-h-screen flex-col items-center justify-between p-24">
      <Table txns={txns} balance={balance} vendor_name={vendor_name} />
    </div>
  );
}
