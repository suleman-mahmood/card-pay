"use client";

import React from "react";
import { auth } from "../../services/initialize-firebase";
import { signOut } from "firebase/auth";
import { useRouter } from "next/navigation";

function Header() {
  const router = useRouter();

  const handleSignOut = () => {
    signOut(auth)
      .then(() => {
        router.push("/");
      })
      .catch((error) => {
        alert(error.message);
      });
  };

  return (
    <div className="navbar bg-base-100">
      <div className="navbar-start">
        <a className="normal-case text-3xl text-black">CardPay</a>
      </div>
      <div className="navbar-end" onClick={handleSignOut}>
        <a className="btn btn-primary">Log Out</a>
      </div>
    </div>
  );
}

export default Header;
