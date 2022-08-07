import { onAuthStateChanged } from 'firebase/auth';
import type { NextPage } from 'next'
import { useRouter } from 'next/router';
import React, { useEffect, useState } from 'react';
import TextField from '../components/text-field';
import { auth, functions } from '../services/initialize-firebase';
import { User as FirebaseUser } from 'firebase/auth';
import Navbar from '../components/navbar';
import { httpsCallable } from 'firebase/functions';

const Transactions: NextPage = () => {

    const router = useRouter();

    const [loading, setLoading] = useState(true);
    const [user, setUser] = useState<FirebaseUser | null>(null);
    const [amount, setAmount] = useState(0);
    const [rollNumber, setRollNumber] = useState(0);
    const [errorMessage, setErrorMessage] = useState('');

    useEffect(() => {
        return onAuthStateChanged(auth, (user) => {
            if (user) {
                setUser(user);
                setLoading(false);
            } else {
                router.push('/');
            }
        })

    }, []);

    const handleSubmit = (e: React.FormEvent) => {
        e.preventDefault();
        setErrorMessage('');

        console.log(amount, rollNumber, user!.uid);

        const makeTransaction = httpsCallable(functions, 'makeTransaction');

        makeTransaction({ amount: amount, senderRollNumber: rollNumber })
            .then(result => {
                console.log(result);
            })
            .catch(error => {
                console.log(error.message);
                setErrorMessage(error.code);
            });
    }

    return (
        loading ?
            <div>Loading...</div> :
            <div className='min-h-screen flex flex-col'>
                <Navbar />
                <div className="hero bg-base-200 flex-grow">
                    <div className="hero-content text-center">
                        <div className="max-w-md">
                            <h1 className="text-5xl font-bold">Transactions</h1>
                            <p className="py-6">Create transactions for customers here!</p>

                            <div className='flex flex-col items-center'>
                                <form onSubmit={handleSubmit} className="form-control w-full max-w-xs">

                                    <TextField inputType='number' labelText='Amount:' placeholder='5' valueSetter={setAmount} />

                                    <TextField inputType='text' labelText='Roll Number:' placeholder='00000000' valueSetter={setRollNumber} />

                                    <button type="submit" className="mt-6 btn btn-outline btn-primary hidden">Transact!</button>

                                    {errorMessage === '' ? null :
                                        <div className="mt-6 alert alert-error shadow-lg">
                                            <div>
                                                <svg xmlns="http://www.w3.org/2000/svg" className="stroke-current flex-shrink-0 h-6 w-6" fill="none" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M10 14l2-2m0 0l2-2m-2 2l-2-2m2 2l2 2m7-2a9 9 0 11-18 0 9 9 0 0118 0z" /></svg>
                                                <span>Error! {errorMessage}</span>
                                            </div>
                                        </div>}
                                </form>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
    )
}

export default Transactions;
