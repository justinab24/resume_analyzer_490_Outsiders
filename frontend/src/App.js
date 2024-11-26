import logo from './logo.svg';
import './App.css';
import ResumeForm from './components/ResumeForm';
import React, { useState } from "react";

function App() {
  return (
      <Router>
        <Routes>
          <Route path="/" element={<SignUp />} />
          <Route path="/login" element={<Login />} />
          <Route path="/dashboard" element={<Dashboard />} />
        </Routes>
      </Router>
  );
}

export default App;