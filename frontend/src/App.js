import logo from './logo.svg';
import './App.css';
import ResumeForm from './components/ResumeForm';
import React, { useState } from "react";

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
  const sampleData = {
    fitScore: {
      total: 75, // Overall percentage
      matched: 50,
      partial: 15,
      missing: 35,
    },
    matchedSkills: ['JavaScript', 'React', 'Node.js', 'Git'],
    improvementSuggestions: [
      'Add proficiency in Python.',
      'Highlight leadership experience.',
      'Include more technical keywords like "REST APIs".',
    ],
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
          Learn React with Valli!
        </a>
      </header>
      <ResumeForm/>
    </div>
  );
}

export default App;