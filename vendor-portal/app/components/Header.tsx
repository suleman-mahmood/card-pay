import React from "react";

function Header() {
  return (
    <div className="navbar bg-base-100">
      <div className="navbar-start">
        <a className="normal-case text-3xl text-black">CardPay</a>
      </div>
      <div className="navbar-end">
        <a className="btn btn-primary">Transactions</a>
      </div>
    </div>
  );
}

export default Header;
