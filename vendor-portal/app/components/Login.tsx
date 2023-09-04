"use client";

import React from "react";
import { useState, useEffect } from "react";
import Link from "next/link";
import { useRouter } from "next/navigation";
import { auth } from "../../services/initialize-firebase";
import { signInWithEmailAndPassword } from "firebase/auth";

function Login() {
  const router = useRouter();

  const [phone, setPhone] = useState("");
  const [password, setPassword] = useState("");
  const [phoneToSend, setPhoneToSend] = useState("");
  const [errorMessage, setErrorMessage] = useState("");

  //  useEffect(() => {
  //    return auth.onAuthStateChanged((user) => {
  //      if (user) {
  //        // User is logged in
  //        router.push("/dashboard");
  //      }
  //    });
  //  }, []);

  const validateInput = (phone: String) => {
    if (phone.length < 10 || phone.length > 11) {
      setErrorMessage("Phone number is too short");
      alert("ghalat");
      return false;
    } else {
      return true;
    }
  };

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (validateInput(phone)) {
      if (phone.length == 10 && phone[0] != "0") {
        setPhoneToSend("92" + phone + " @cardpay.com.pk");
      }
      if (phone.length == 11 && phone[0] == "0") {
        setPhoneToSend("92" + phone.slice(1) + "@cardpay.com.pk");
      }
      console.log(phoneToSend);
      signInWithEmailAndPassword(auth, phoneToSend, password)
        .then(() => {
          router.push("/dashboard");
          //setLoading(false);
        })
        .catch((error) => {
          setErrorMessage(error.code);
          //setLoading(false);
        });
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
