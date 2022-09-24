import React from "react";

export default function Loader() {
  return (
    <div className="min-h-screen flex flex-col">
      <div className="hero flex-grow">
        <progress className="progress progress-primary"></progress>
      </div>
    </div>
  );
}
