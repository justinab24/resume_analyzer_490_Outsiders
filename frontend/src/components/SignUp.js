import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import axios from 'axios';
import '../stylesheet/signup.css';

const SignUp = () => {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [message, setMessage] = useState('');
  const navigate = useNavigate();

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      const response = await axios.post('http://localhost:8000/api/register', {
        email,
        password,
      });
      setMessage(response.data.message);
  
      if (response.data.message === 'User registered successfully') {
        navigate('/dashboard'); // Navigate to the dashboard
      }
    } catch (error) {
      console.error('Error details:', error); // Log the error details for debugging
      let errorMessage;
      if (error.response) {
        errorMessage = error.response.data && error.response.data.detail 
          ? error.response.data.detail 
          : error.response.statusText || 'Error registering user';
      } else if (error.request) {
        errorMessage = 'Network error: Please check your connection or try again later.';
      } else {
        errorMessage = error.message || 'An unexpected error occurred';
      }
      setMessage(errorMessage);
    }
  };

  return (
    <div>
      <h1>Sign Up</h1>
      <form id="signup" onSubmit={handleSubmit}>
        <input
          type="email"
          placeholder="Email"
          value={email}
          onChange={(e) => setEmail(e.target.value)}
          required
        />
        <input
          type="password"
          placeholder="Password"
          value={password}
          onChange={(e) => setPassword(e.target.value)}
          required
        />
        <button type="submit">Sign Up</button>
      </form>

      <h1>Already have an account?</h1>
      <a href="/login">Sign In</a>
      <p>{message}</p>
    </div>
  );
};

export default SignUp;