import React, { useEffect } from "react";
import { useState } from "react";
import moment from "moment";
import "moment-timezone";

interface Transaction {
  amount: number;
  created_at: string;
  last_updated: string;
  sender_name: string;
}

interface Props {
  txns: Transaction[]; // Define the txns prop here
}

const Table: React.FC<Props> = ({ txns }) => {
  const [times, setTimes] = useState<string[]>([]);

  useEffect(() => {
    txns.map((txn) => {
      const timeStringGMT = txn.created_at;
      const parsedTimeGMT = moment.tz(
        timeStringGMT,
        "ddd, DD MMM YYYY HH:mm:ss [GMT]",
        "GMT"
      );
      const currentTimeGMT5 = moment().tz("Asia/Karachi");
      const timeAgo = parsedTimeGMT.from(currentTimeGMT5);
      setTimes((times) => [...times, timeAgo]);
    });
  }, [txns]);

  return (
    <div className="overflow-x-auto">
      <h1 className="mb-2 text-4xl font-bold text-center text-black">
        Transactions
      </h1>
      {/*<h2 className="mb-2 text-2xl font-bold text-center">CardPay Cafe</h2>*/}
      <h3 className="mb-2 text-md text-center text-violet-600">
        Balance: 1000000
      </h3>
      <table className="table table-lg">
        {/* head */}
        <thead>
          <tr className="bg-white">
            <th></th>
            <th>Sender Name</th>
            <th>Amount</th>
            <th>Time</th>
          </tr>
        </thead>
        <tbody>
          {txns.map((txn, index) => (
            <tr key={index}>
              <th>{index + 1}</th>
              <td>{txn.sender_name}</td>
              <td>{txn.amount}</td>
              <td>{times[index]}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
};

export default Table;
