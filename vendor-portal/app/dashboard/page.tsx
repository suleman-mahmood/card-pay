"use client";

import React from "react";
import { useEffect, useState } from "react";
import { useRouter } from "next/navigation";
import { User as FirebaseUser } from "firebase/auth";
import { onAuthStateChanged } from "firebase/auth";
import { auth } from "../../services/initialize-firebase";
import Table from "./components/Table";

interface Transaction {
  amount: number;
  id: string;
  recipientName: string;
  senderName: string;
  status: string;
  timestamp: string;
}

function page() {
  const router = useRouter();
  const [user, setUser] = useState<FirebaseUser | null>(null);

  useEffect(() => {
    return onAuthStateChanged(auth, (user: any) => {
      if (user) {
        setUser(user);
        fetchTransactions(user);
      } else {
        router.push("/");
      }
    });
  }, []);

  const fetchTransactions = async (user: FirebaseUser) => {
    const token = await user?.getIdToken();
    console.log(user);
    console.log(token);
    fetch(
      `https://cardpay-1.el.r.appspot.com/api/v1/get-vendor-transactions-to-be-reconciled`,
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
        console.log(data);
        //setTransactions(data.transactions);
      })
      .catch((error) => {
        console.error("Error fetching data:", error);
      });
  };

  return (
    <div className="flex min-h-screen flex-col items-center justify-between p-24">
      <Table />
    </div>
  );
}

export default page;
