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
import { BASE_URL } from "@/services/remote-config";

export interface Transaction {
  amount: number;
  created_at: string;
  last_updated: string;
  sender_name: string;
  recipient_name: string;
  transaction_type: string;
}

export default function page() {
  const router = useRouter();
  const [user, setUser] = useState<FirebaseUser | null>(null);
  const [txns, setTxns] = useState<Transaction[]>([]);
  const [isFetching, setIsFetching] = useState<boolean>(true);
  const [balance, setBalance] = useState<number>(0);
  const [vendor_name, setVendorName] = useState<string>("");
  const [currentReconciledTxnId, setCurrentReconciledTxnId] = useState<string>(
    ""
  );
  const [lastestReconciledTxnId, setLatestReconciledTxnId] = useState<string>(
    ""
  );
  const [
    currentReconciledTxnBalance,
    setCurrentReconciledTxnBalance,
  ] = useState<number | null>(null);

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
      `${BASE_URL}/api/v1/vendor-app/get-vendor-transactions-to-be-reconciled`,
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
    fetch(`${BASE_URL}/api/v1/vendor-app/get-vendor-balance`, {
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

  const handlePrevious = async (currentReconciledTxnId: string) => {
    setIsFetching(true);
    const token = await user?.getIdToken();
    let currentTx = "";

    if (token === undefined) return;

    if (currentReconciledTxnId === "") {
      const response = await fetch(
        `${BASE_URL}/api/v1/vendor-app/get-vendor-latest-reconciliation-txn-id`,
        {
          method: "GET",
          mode: "cors",
          headers: {
            "Content-Type": "application/json",
            Authorization: `Bearer ${token}`,
          },
        }
      );
      if (!response.ok) {
        return;
      }
      const data = await response.json();

      currentTx = data.data.latest_reconciliation_txn_id;
      setCurrentReconciledTxnId(currentTx);
      setLatestReconciledTxnId(currentTx);
    } else {
      const response = await fetch(
        `${BASE_URL}/api/v1/vendor-app/get-vendor-previous-reconciliation-txn-id?reconciled_txn_id=${currentReconciledTxnId}`,
        {
          method: "GET",
          mode: "cors",
          headers: {
            "Content-Type": "application/json",
            Authorization: `Bearer ${token}`,
          },
        }
      );
      if (!response.ok) {
        alert("No Previous Transactions Found.");
        return;
      }
      const data = await response.json();
      currentTx = data.data.previous_reconciliation_txn_id;
      setCurrentReconciledTxnId(currentTx);
    }

    if (currentTx === undefined) {
      return;
    }

    const response = await fetch(
      `${BASE_URL}/api/v1/vendor-app/get-vendor-reconciled-transactions?reconciled_txn_id=${currentTx}`,
      {
        method: "GET",
        mode: "cors",
        headers: {
          "Content-Type": "application/json",
          Authorization: `Bearer ${token}`,
        },
      }
    );
    if (!response.ok) {
      return;
    }
    const data = await response.json();
    const retrieved_txns = data.data as Array<Transaction>;
    setTxns(retrieved_txns);
    const totalBalance: number = retrieved_txns.reduce(
      (sum, txn) => sum + txn.amount,
      0
    );
    setCurrentReconciledTxnBalance(totalBalance);
    setIsFetching(false);
  };

  const handleNext = async (currentReconciledTxnId: string) => {
    setIsFetching(true);

    if (currentReconciledTxnId === lastestReconciledTxnId) {
      if (user === null) return;
      setCurrentReconciledTxnId("");
      setCurrentReconciledTxnBalance(null);
      fetchTransactions(user);
      return;
    }
    const token = await user?.getIdToken();
    let currentTx = "";
    const response1 = await fetch(
      `${BASE_URL}/api/v1/vendor-app/get-vendor-next-reconciliation-txn-id?reconciled_txn_id=${currentReconciledTxnId}`,
      {
        method: "GET",
        mode: "cors",
        headers: {
          "Content-Type": "application/json",
          Authorization: `Bearer ${token}`,
        },
      }
    );

    if (!response1.ok) {
      alert("No Next Transactions Found.");
      return;
    }
    const data1 = await response1.json();
    currentTx = data1.data.next_reconciliation_txn_id;
    setCurrentReconciledTxnId(currentTx);

    if (currentTx === undefined) {
      return;
    }

    const response = await fetch(
      `${BASE_URL}/api/v1/vendor-app/get-vendor-reconciled-transactions?reconciled_txn_id=${currentTx}`,
      {
        method: "GET",
        mode: "cors",
        headers: {
          "Content-Type": "application/json",
          Authorization: `Bearer ${token}`,
        },
      }
    );
    if (!response.ok) {
      return;
    }
    const data = await response.json();
    const retrieved_txns = data.data as Array<Transaction>;
    setTxns(retrieved_txns);
    const totalBalance: number = retrieved_txns.reduce(
      (sum, txn) => sum + txn.amount,
      0
    );
    setCurrentReconciledTxnBalance(totalBalance);
    setIsFetching(false);
  };

  return isFetching ? (
    <div className="flex flex-col items-center justify-between min-h-screen p-24">
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
    <div className="flex flex-col items-center justify-between min-h-screen p-24">
      <Table
        txns={txns}
        balance={balance}
        vendor_name={vendor_name}
        currentReconciledTxnBalance={currentReconciledTxnBalance}
      />
      <div className="flex">
        {currentReconciledTxnId && (
          <div
            className="max-w-xs mr-2 w-half btn btn-primary"
            onClick={() => handleNext(currentReconciledTxnId)}
          >
            Next
          </div>
        )}
        <div
          className="max-w-xs w-half btn btn-primary"
          onClick={() => handlePrevious(currentReconciledTxnId)}
        >
          Previous
        </div>
      </div>
    </div>
  );
}
