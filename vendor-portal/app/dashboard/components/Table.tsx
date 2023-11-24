import React, { useEffect } from "react";
import { useState } from "react";
import moment from "moment";
import "moment-timezone";
import { Transaction } from "../page";

interface Props {
  txns: Transaction[]; // Define the txns prop here
  balance: number;
  vendor_name: string;
  currentReconciledTxnBalance: number | null;
}

const Table: React.FC<Props> = ({
  txns,
  balance,
  vendor_name,
  currentReconciledTxnBalance,
}) => {
  const [times, setTimes] = useState<string[]>([]);
  const [createdAt, setCreatedAt] = useState<string[]>([]);

  useEffect(() => {
    createdAt && setCreatedAt([]);
    times && setTimes([]);
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
      setCreatedAt((createdAt) => [
        ...createdAt,
        parsedTimeGMT.tz("Asia/Karachi").format("LLL").toString(),
      ]);
    });
  }, [txns]);

  function refreshPage() {
    window.location.reload();
  }

  return (
    <div className="overflow-x-auto">
      <h1 className="mb-2 text-4xl font-bold text-center text-violet-600">
        {vendor_name}
      </h1>
      <h1 className="mb-2 text-2xl font-bold text-center text-black">
        Transactions
      </h1>
      <h3 className="mb-2 text-center text-md text-violet-600">
        Today's Balance: {balance}
      </h3>
      {currentReconciledTxnBalance && (
        <h3 className="mb-2 text-center text-md text-violet-600">
          Reconciled Amount: {currentReconciledTxnBalance}
        </h3>
      )}
      <h6 className="mb-2 text-center text-yellow-500 text-md">
        *Yellow Colored Rows are Top Ups*
      </h6>
      <table className="table lg:table-lg md:table-md sm:table-sm">
        <thead>
          <tr className="bg-white">
            <th>Name</th>
            <th>Amount</th>
            <th>Time</th>
            <th>
              {" "}
              <svg
                xmlns="http://www.w3.org/2000/svg"
                height="1em"
                viewBox="0 0 512 512"
                onClick={refreshPage}
                className="cursor-pointer"
              >
                <path d="M105.1 202.6c7.7-21.8 20.2-42.3 37.8-59.8c62.5-62.5 163.8-62.5 226.3 0L386.3 160H336c-17.7 0-32 14.3-32 32s14.3 32 32 32H463.5c0 0 0 0 0 0h.4c17.7 0 32-14.3 32-32V64c0-17.7-14.3-32-32-32s-32 14.3-32 32v51.2L414.4 97.6c-87.5-87.5-229.3-87.5-316.8 0C73.2 122 55.6 150.7 44.8 181.4c-5.9 16.7 2.9 34.9 19.5 40.8s34.9-2.9 40.8-19.5zM39 289.3c-5 1.5-9.8 4.2-13.7 8.2c-4 4-6.7 8.8-8.1 14c-.3 1.2-.6 2.5-.8 3.8c-.3 1.7-.4 3.4-.4 5.1V448c0 17.7 14.3 32 32 32s32-14.3 32-32V396.9l17.6 17.5 0 0c87.5 87.4 229.3 87.4 316.7 0c24.4-24.4 42.1-53.1 52.9-83.7c5.9-16.7-2.9-34.9-19.5-40.8s-34.9 2.9-40.8 19.5c-7.7 21.8-20.2 42.3-37.8 59.8c-62.5 62.5-163.8 62.5-226.3 0l-.1-.1L125.6 352H176c17.7 0 32-14.3 32-32s-14.3-32-32-32H48.4c-1.6 0-3.2 .1-4.8 .3s-3.1 .5-4.6 1z" />
              </svg>
            </th>
          </tr>
        </thead>
        <tbody>
          {txns.map((txn, index) => (
            <tr
              key={index}
              className={`${
                times[index] === "a few seconds ago"
                  ? "bg-lime-500"
                  : txn.transaction_type === "TOP_UP"
                  ? "bg-yellow-300"
                  : ""
              }`}
            >
              <td>
                {txn.transaction_type === "TOP_UP"
                  ? txn.recipient_name
                  : txn.sender_name}
              </td>
              <td>{txn.amount}</td>
              <td>{createdAt[index]}</td>
              <td>
                <em>{times[index]}</em>
              </td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
};

export default Table;
