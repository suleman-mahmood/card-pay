import { signOut } from 'firebase/auth'
import React from 'react'
import { auth } from '../services/initialize-firebase';

export default function Navbar() {

    const handleLogout = () => {
        signOut(auth);
    }

    return (
        <div className="navbar bg-base-100 py-4 px-8">
            <div className="flex-1">
                <a className="btn btn-ghost normal-case text-xl">CardPay</a>
            </div>
            <div className="flex-none">
                <button className="btn btn-accent" onClick={handleLogout}>Logout</button>
            </div>
        </div>
    )
}
