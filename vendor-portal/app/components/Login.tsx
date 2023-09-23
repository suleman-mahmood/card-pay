"use client";
/* eslint-disable */

import React from "react";
import { useState, useEffect } from "react";
import Link from "next/link";
import { useRouter } from "next/navigation";
import { auth } from "../../services/initialize-firebase";
import { signInWithEmailAndPassword } from "firebase/auth";

function Login() {
  const router = useRouter();

  const [phone, setPhone] = useState<string>("");
  const [password, setPassword] = useState<string>("");
  const [phoneToSend, setPhoneToSend] = useState<string>("");
  const [errorPhone, setErrorPhone] = useState<string>("");
  const [errorPassword, setErrorPassword] = useState<string>("");

  useEffect(() => {
    return auth.onAuthStateChanged((user) => {
      if (user) {
        router.push("/dashboard");
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

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (validateInput(phone)) {
      if (phone.length == 10 && phone[0] != "0") {
        setPhoneToSend("92" + phone + "@cardpay.com.pk");
      }
      if (phone.length == 11 && phone[0] == "0") {
        setPhoneToSend("92" + phone.slice(1) + "@cardpay.com.pk");
      }
    }
  };

  useEffect(() => {
    signInWithEmailAndPassword(auth, phoneToSend, password)
      .then(() => {
        setErrorPassword("");
        router.push("/dashboard");
      })
      .catch((error) => {
        setErrorPassword(error.code);
      });
  }, [phoneToSend, password]);

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
        <Link
          href="/dashboard"
          className="btn btn-primary mt-6 max-w-xs w-full"
          onClick={handleSubmit}
        >
          Login
        </Link>
      </form>
    </div>
  );
}

export default Login;
