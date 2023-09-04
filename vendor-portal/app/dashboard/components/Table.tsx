import React from "react";

function Table() {
  return (
    <div className="overflow-x-auto">
      <h1 className="mb-2 text-4xl font-bold text-center text-slate-700">
        Transactions
      </h1>
      {/*<h2 className="mb-2 text-2xl font-bold text-center">CardPay Cafe</h2>*/}
      <h3 className="mb-2 text-md text-center text-violet-600">
        Balance: 1000000
      </h3>
      <table className="table table-lg">
        {/* head */}
        <thead>
          <tr className="bg-base-200">
            <th></th>
            <th>Sender Name</th>
            <th>Amount</th>
            <th>Time</th>
          </tr>
        </thead>
        <tbody>
          {/* row 1 */}
          <tr>
            <th>1</th>
            <td>Moaz</td>
            <td>100</td>
            <td>10 seconds ago</td>
          </tr>
          {/* row 2 */}
          <tr>
            <th>2</th>
            <td>Talha</td>
            <td>200</td>
            <td>30 days ago</td>
          </tr>
          {/* row 3 */}
          <tr>
            <th>3</th>
            <td>Suleman</td>
            <td>300</td>
            <td>1 month ago</td>
          </tr>
        </tbody>
      </table>
    </div>
  );
}

export default Table;
