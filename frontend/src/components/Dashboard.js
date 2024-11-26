import React, { useEffect, useState } from 'react';
import axios from 'axios';
import ResumeForm from './ResumeForm';

const Dashboard = () => {
  const [message, setMessage] = useState('');

  useEffect(() => {
    const fetchDashboard = async () => {
      try {
        const token = localStorage.getItem('token');
        const response = await axios.get('http://localhost:8000/dashboard', {
          params: { token },
        });
        setMessage(response.data.message);
      } catch (error) {
        setMessage(error.response.data.detail || 'Error loading dashboard');
      }
    };
    fetchDashboard();
  }, []);

  return (
    <div>
      <h2>Dashboard</h2>
      <p>{message}</p>
      <ResumeForm />
    </div>
  );
};

export default Dashboard;
