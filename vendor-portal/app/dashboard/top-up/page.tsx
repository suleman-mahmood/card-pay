"use client";
/* eslint-disable */

import React from "react";
import { useEffect, useState } from "react";
import { useRouter } from "next/navigation";
import { User as FirebaseUser } from "firebase/auth";
import { onAuthStateChanged } from "firebase/auth";
import { auth } from "../../../services/initialize-firebase";
import { BASE_URL } from "@/services/remote-config";
import LoadingOverlay from "@/app/events/spinner";

export default function page() {
  const router = useRouter();
  const [user, setUser] = useState<FirebaseUser | null>(null);
  const [isFetching, setIsFetching] = useState<boolean>(true);
  const [errorMessage, setErrorMessage] = useState<string>("");

  const [balance, setBalance] = useState<number>(0);
  const [vendor_name, setVendorName] = useState<string>("");

  const [recipientUniqueIdentifier, setRecipientUniqueIdentifier] = useState<string>("");
  const [amount, setAmount] = useState<number>(0);
  const [closedLoopId, setClosedLoopId] = useState<string>("");
  const [recipientName, setRecipientName] = useState<string>("");

  useEffect(() => {
    return onAuthStateChanged(auth, (user: any) => {
      if (user) {
        setUser(user);
        fetchVendorBalance(user);
        fetchVendor(user);
      } else {
        router.push("/");
      }
    });
  }, []);

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
        setIsFetching(false);
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
        const closedLoopId = Object.keys(data.data.closed_loops)[0];
        setVendorName(vendor_name);
        setClosedLoopId(closedLoopId);
      })
      .catch((error) => {
        console.error("Error fetching data:", error);
      });
  };

  const topUp = async () => {
    setIsFetching(true);
    const token = await user?.getIdToken();
    fetch(
      `${BASE_URL}/api/v1/vendor-app/execute-top-up-transaction`,
      {
        method: "POST",
        mode: "cors",
        headers: {
          "Content-Type": "application/json",
          Authorization: `Bearer ${token}`,
        },
        body: JSON.stringify(
          {
            recipient_unique_identifier: recipientUniqueIdentifier,
            amount: amount,
            closed_loop_id: closedLoopId,
          }
        )
      }
    )
      .then(async (response) => {
        if (!response.ok) {
          const res = await response.json();
          throw new Error(res.message);
        }
        return response.json();
      })
      .then((data) => {
        // Success
        setIsFetching(false);
        (document.getElementById('success_modal') as any).showModal();
        if (user) fetchVendorBalance(user);
        console.log(data);
      })
      .catch((error) => {
        // Failure
        setIsFetching(false);
        (document.getElementById('error_modal') as any).showModal()
        setErrorMessage(error.message);
      });
  };

  const fetchNameFromRollnumber = async () => {
    setIsFetching(true);
    const token = await user?.getIdToken();

    fetch(
      `${BASE_URL}/api/v1/vendor-app/get-name-from-unique-identifier-and-closed-loop?` + new URLSearchParams({
        unique_identifier: recipientUniqueIdentifier,
        closed_loop_id: closedLoopId,
      }),
      {
        method: "GET",
        mode: "cors",
        headers: {
          "Content-Type": "application/json",
          Authorization: `Bearer ${token}`,
        },
      }
    )
      .then(async (response) => {
        if (!response.ok) {
          const res = await response.json();
          throw new Error(res.message);
        }
        return response.json();
      })
      .then((data) => {
        // Success
        setIsFetching(false);
        const recipientName = data.data.full_name;
        setRecipientName(recipientName);
        (document.getElementById('confirm_modal') as any).showModal()
      })
      .catch((error) => {
        // Failure
        setIsFetching(false);
        (document.getElementById('error_modal') as any).showModal()
        setErrorMessage(error.message);
      });
  };

  return (
    <div className="flex flex-col items-center">
      <h1 className="mb-2 mt-8 text-4xl font-bold text-center text-violet-600">
        {vendor_name}
      </h1>
      <h3 className="mb-2 text-center text-md text-violet-600">
        Balance: {balance}
      </h3>

      <div className="form-control w-full max-w-xs">
        <label className="label">
          <span className="label-text">Roll number</span>
        </label>
        <input
          type="text"
          placeholder="23100011"
          className="input input-bordered w-full max-w-xs"
          onChange={(e) => setRecipientUniqueIdentifier(e.target.value)}
        />
      </div>

      <div className="form-control w-full max-w-xs">
        <label className="label">
          <span className="label-text">Amount</span>
        </label>
        <input
          type="number"
          placeholder="0000"
          className="input input-bordered w-full max-w-xs"
          onChange={(e) => setAmount(parseInt(e.target.value))}
        />
      </div>

      <button className="btn btn-secondary mt-4" onClick={fetchNameFromRollnumber}>Skadoosh!</button>

      {isFetching && <LoadingOverlay />}

      {/* Modals */}

      {/* Confirm top up */}
      <dialog id="confirm_modal" className="modal">
        <div className="modal-box">
          <h3 className="font-bold text-lg">
            <span>
              You sure...?
            </span>
          </h3>
          <p className="py-2">Name: {recipientName}</p>
          <p className="py-2">Roll number: {recipientUniqueIdentifier}</p>
          <p className="py-2">Amount: {amount}</p>
          <div className="modal-action">
            <form method="dialog">
              <button className="mx-2 btn btn-success" onClick={topUp}>Absolutely!</button>
              <button className="mx-2 btn btn-outline btn-error">Nope</button>
            </form>
          </div>
        </div>
      </dialog>

      {/* Success */}
      <dialog id="success_modal" className="modal">
        <div className="modal-box">
          <h3 className="font-bold text-lg">
            <span>
              Top up successful!
            </span>
          </h3>
          <div className="modal-action">
            <form method="dialog">
              <button className="mx-2 btn btn-success">Keep it goin!</button>
            </form>
          </div>
        </div>
      </dialog>

      {/* Error */}
      <dialog id="error_modal" className="modal">
        <div className="modal-box">
          <h3 className="font-bold text-lg">
            <span>
              Error! 💥
            </span>
          </h3>
          <p>{errorMessage}</p>
          <div className="modal-action">
            <form method="dialog">
              <button className="mx-2 btn btn-error">Oh noess, try again!</button>
            </form>
          </div>
        </div>
      </dialog>
    </div>
  )
}
