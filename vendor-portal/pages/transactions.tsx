import { onAuthStateChanged } from "firebase/auth";
import type { NextPage } from "next";
import { useRouter } from "next/router";
import React, { useEffect, useState } from "react";
import TextField from "../components/text-field";
import { auth, functions } from "../services/initialize-firebase";
import { User as FirebaseUser } from "firebase/auth";
import Navbar from "../components/navbar";
import { httpsCallable } from "firebase/functions";
import Swal from "sweetalert2";
import Loader from "../components/loader";

const KEY_PAD_CONFIG = [
  [1, 5, 10],
  [50, 100, 200],
  [500, 1000, 1500],
];

const Transactions: NextPage = () => {
  const router = useRouter();

  const [loading, setLoading] = useState(true);
  const [user, setUser] = useState<FirebaseUser | null>(null);
  const [amount, setAmount] = useState(0);
  const [rollNumber, setRollNumber] = useState(0);
  const [errorMessage, setErrorMessage] = useState("");
  const [shouldFocus, setShouldFocus] = useState(true);

  const getRandomInteger = (): number => {
    return Math.floor(Math.random() * 1000);
  };

  useEffect(() => {
    return onAuthStateChanged(auth, (user) => {
      if (user) {
        setUser(user);
        setLoading(false);
      } else {
        router.push("/");
      }
    });
  }, []);

  useEffect(() => {
    if (!shouldFocus) {
      return;
    }

    const intervalId = setInterval(() => {
      document.getElementById("roll-number-input")?.focus();
    }, 100);

    return () => clearInterval(intervalId);
  }, [shouldFocus]);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setErrorMessage("");
    setShouldFocus(false);
    setLoading(true);

    console.log(amount, rollNumber, user!.uid);

    const { value: userPin } = await Swal.fire({
      title: "Input your 4-digit pin",
      input: "text",
      inputLabel: "Your pin",
      inputPlaceholder: "Enter your pin",
    });

    if (!userPin) {
      setErrorMessage("Please enter pin");
      setShouldFocus(true);
      setLoading(false);
      return;
    }

    const makeTransaction = httpsCallable(functions, "makeTransaction");

    makeTransaction({
      amount: amount,
      senderRollNumber: rollNumber,
      pin: userPin,
    })
      .then((result) => {
        console.log(result);
        setShouldFocus(true);
        setLoading(false);

        Swal.fire({
          icon: "success",
          title: "Transaction was successful",
          showConfirmButton: false,
          timer: 2000,
        });
      })
      .catch((error) => {
        console.log(error.message);
        setErrorMessage(error.message);
        setShouldFocus(true);
        setLoading(false);
      });
  };

  const handleAmountClick = (value: number) => {
    setAmount((v) => v + value);
  };

  return loading ? (
    <Loader />
  ) : (
    <div className="min-h-screen flex flex-col">
      <Navbar />
      <div className="hero flex-grow">
        <div className="hero-content text-center">
          <div className="max-w-md">
            <h1 className="text-5xl font-bold">Transactions</h1>
            <p className="py-6">
              Commulatively add the amount using the below keypad
            </p>

            <div className="w-full flex flex-col items-center">
              {KEY_PAD_CONFIG.map((k, i) => {
                return (
                  <div key={getRandomInteger()} className="flex flex-row mb-4">
                    {k.map((value, j) => {
                      return (
                        <button
                          key={getRandomInteger()}
                          className="btn mr-4"
                          onClick={() => handleAmountClick(value)}
                        >
                          {value}
                        </button>
                      );
                    })}
                  </div>
                );
              })}
            </div>

            <button className="btn btn-secondary" onClick={() => setAmount(0)}>
              Clear amount
            </button>

            <div className="flex flex-col items-center">
              <form
                onSubmit={handleSubmit}
                className="form-control w-full max-w-xs"
              >
                <TextField
                  inputType="number"
                  labelText="Amount:"
                  placeholder="xxxx"
                  currentVal={amount}
                  valueSetter={setAmount}
                  readOnly={true}
                />

                <TextField
                  id="roll-number-input"
                  inputType="text"
                  labelText="Roll Number:"
                  placeholder="00000000"
                  valueSetter={setRollNumber}
                  readOnly={true}
                />

                <button
                  type="submit"
                  className="mt-6 btn btn-outline btn-primary hidden"
                >
                  Transact!
                </button>

                {errorMessage === "" ? null : (
                  <div className="mt-6 alert alert-error shadow-lg">
                    <div>
                      <svg
                        xmlns="http://www.w3.org/2000/svg"
                        className="stroke-current flex-shrink-0 h-6 w-6"
                        fill="none"
                        viewBox="0 0 24 24"
                      >
                        <path
                          strokeLinecap="round"
                          strokeLinejoin="round"
                          strokeWidth="2"
                          d="M10 14l2-2m0 0l2-2m-2 2l-2-2m2 2l2 2m7-2a9 9 0 11-18 0 9 9 0 0118 0z"
                        />
                      </svg>
                      <span>Error! {errorMessage}</span>
                    </div>
                  </div>
                )}
              </form>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default Transactions;
