import React, { useState } from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import SignUp from './components/SignUp';
import Login from './components/Login';
import Dashboard from './components/Dashboard';
import logo from './logo.svg';
import './App.css';
import ResumeForm from './components/ResumeForm';

function App() {
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [data, setData] = useState(null);

  // Simulated API call
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
      {/* Header Section */}
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
          Learn React with Valli!
        </a>
      </header>

      {/* Router Section */}
      <Router>
        <Routes>
          <Route path="/signup" element={<SignUp />} />
          <Route path="/login" element={<Login />} />
          <Route path="/dashboard" element={<Dashboard />} />
        </Routes>
      </Router>

      {/* Resume Form */}
      <ResumeForm />
    </div>
  );
}

export default App;
