import React, { useState } from "react";
import logo from "./logo.svg";
import "./App.css";

function App() {
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [data, setData] = useState(null);

  const fetchData = async () => {
    setLoading(true);
    setError(null);
    try {
      // Simulate API call with a timeout
      const response = await new Promise((resolve) =>
        setTimeout(() => resolve({ data: "Sample API Data" }), 2000)
      );
      setData(response.data);
    } catch (err) {
      setError("Failed to fetch data. Try again");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="App">
      <header className="App-header">
        <img src={logo} className="App-logo" alt="logo" />
        <p>Edit <code>src/App.js</code> and save to reload.</p>
        <button className="fetch-button" onClick={fetchData}>
          {loading ? "Loading..." : "Fetch Data"}
        </button>
        {loading && <div className="spinner"></div>}
        {error && <div className="error-message">{error}</div>}
        {data && <div className="data-display">{data}</div>}
        <a
          className="App-link"
          href="https://reactjs.org"
          target="_blank"
          rel="noopener noreferrer"
        >
          Learn React
        </a>
      </header>
    </div>
  );
}

export default App;