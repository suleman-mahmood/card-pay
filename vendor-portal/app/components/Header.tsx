import React from "react";

function Header() {
  return (
    <div className="navbar bg-base-100">
      <div className="navbar-start">
        <a className="btn btn-ghost normal-case text-3xl">CardPay</a>
      </div>
      <div className="navbar-end">
        <a className="btn btn-primary">Transactions</a>
      </div>
    </div>
  );
}

export default Header;
