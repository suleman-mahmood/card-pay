"use client";
/* eslint-disable */

import React from "react";
import { useState, useEffect } from "react";
import Link from "next/link";
import { useRouter } from "next/navigation";
import { auth } from "../../services/initialize-firebase";
import { signInWithEmailAndPassword } from "firebase/auth";
import { User as FirebaseUser } from "firebase/auth";
import { BASE_URL } from "@/services/remote-config";

function Login() {
  const router = useRouter();

  const [phone, setPhone] = useState<string>("");
  const [password, setPassword] = useState<string>("");
  const [errorPhone, setErrorPhone] = useState<string>("");
  const [errorPassword, setErrorPassword] = useState<string>("");
  const [vendor_type, setVendorType] = useState<string>("");

  useEffect(() => {
    return auth.onAuthStateChanged(async (user: any) => {
      if (user) {
        await fetchVendor(user)
      }
    });
  }, []);

  const validateInput = (phone: String) => {
    if (phone.length < 10 || phone.length > 11) {
      setErrorPhone("Phone number is too short.");
      return false;
    } else {
      setErrorPhone("");
      return true;
    }
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
        setVendorType(data.data.user_type)
        if (data.data.user_type === '6') {
          router.push("/events/dashboard")
        }
        else {
          router.push("/dashboard")
        }
      })
      .catch((error) => {
        console.error("Error fetching data:", error);
      });
  };

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (validateInput(phone)) {
      let phoneToSend = "";

      if (phone.length == 10 && phone[0] != "0") {
        phoneToSend = "92" + phone + "@cardpay.com.pk";
      }
      if (phone.length == 11 && phone[0] == "0") {
        phoneToSend = "92" + phone.slice(1) + "@cardpay.com.pk";
      }

      if (phoneToSend) {
        signInWithEmailAndPassword(auth, phoneToSend, password)
          .then(() => {
            setErrorPassword("");
            router.push("/dashboard");
          })
          .catch((error) => {
            setErrorPassword(error.code);
          });
      }
    }
  };

  return (
    <div className="form-control w-full max-w-xs">
      <form>
        <label className="label">
          <span className="label-text">Phone Number</span>
        </label>
        <input
          type="text"
          placeholder="03034952255"
          className="input input-bordered w-full max-w-xs"
          onChange={(e) => setPhone(e.target.value)}
          value={phone}
        />
        {errorPhone && (
          <span className="italic text-xs text-red-500">{errorPhone}</span>
        )}
        <label className="label">
          <span className="label-text">Password</span>
        </label>
        <input
          type="password"
          placeholder="********"
          className="input input-bordered w-full max-w-xs password"
          onChange={(e) => setPassword(e.target.value)}
          value={password}
        />
        {errorPassword && (
          <span className="italic text-xs text-red-500">{errorPassword}</span>
        )}
        <div
          className="btn btn-primary mt-6 max-w-xs w-full"
          onClick={handleSubmit}
        >
          Login
        </div>
      </form>
    </div>
  );
}

export default Login;
