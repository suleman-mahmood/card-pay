"use client";

import React from "react";
import { useEffect } from "react";
import Table from "./components/Table";

function page() {
  useEffect(() => {
    fetchTransactions();
  }, []);

  const fetchTransactions = () => {
    fetch(
      `https://cardpay-1.el.r.appspot.com/api/v1/api/v1/payment-retools-get-transactions-to-be-reconciled?vendor_id=6a0aeaaf-e9c6-5ed6-87f4-cfa355aa05de`,
      {
        method: "GET",
        headers: {
          "Content-Type": "application/json",
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
