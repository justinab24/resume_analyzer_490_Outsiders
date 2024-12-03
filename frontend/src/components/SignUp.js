<<<<<<< HEAD
import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import axios from 'axios';

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
      setMessage(error.response.data.detail || 'Error registering user');
=======
import React, { useState } from "react";
import axios from "axios";

const SignUp = () => {
  const [formData, setFormData] = useState({
    email: "",
    username: "",
    password: "",
    confirmPassword: "",
  });

  const [error, setError] = useState("");
  const [success, setSuccess] = useState("");

  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData({ ...formData, [name]: value });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (formData.password !== formData.confirmPassword) {
      setError("Passwords do not match");
      return;
    }
    try {
      const response = await axios.post("/api/register", {
        email: formData.email,
        username: formData.username,
        password: formData.password,
      });
      setSuccess(response.data.message);
      setError("");
    } catch (err) {
      setError(err.response?.data?.error || "An error occurred");
      setSuccess("");
>>>>>>> f2bd3a3 (Tasks 6 and 7)
    }
  };

  return (
    <div>
<<<<<<< HEAD
      <h1>Sign Up</h1>
      <form onSubmit={handleSubmit}>
        <input
          type="email"
          placeholder="Email"
          value={email}
          onChange={(e) => setEmail(e.target.value)}
=======
      <h2>Sign Up</h2>
      {error && <p style={{ color: "red" }}>{error}</p>}
      {success && <p style={{ color: "green" }}>{success}</p>}
      <form onSubmit={handleSubmit}>
        <input
          type="email"
          name="email"
          placeholder="Email"
          value={formData.email}
          onChange={handleChange}
          required
        />
        <input
          type="text"
          name="username"
          placeholder="Username"
          value={formData.username}
          onChange={handleChange}
>>>>>>> f2bd3a3 (Tasks 6 and 7)
          required
        />
        <input
          type="password"
<<<<<<< HEAD
          placeholder="Password"
          value={password}
          onChange={(e) => setPassword(e.target.value)}
=======
          name="password"
          placeholder="Password"
          value={formData.password}
          onChange={handleChange}
          required
        />
        <input
          type="password"
          name="confirmPassword"
          placeholder="Confirm Password"
          value={formData.confirmPassword}
          onChange={handleChange}
>>>>>>> f2bd3a3 (Tasks 6 and 7)
          required
        />
        <button type="submit">Sign Up</button>
      </form>
<<<<<<< HEAD

      <h1>Already have an account?</h1>
      <a href="/login">Sign In</a>
      <p>{message}</p>
=======
>>>>>>> f2bd3a3 (Tasks 6 and 7)
    </div>
  );
};

export default SignUp;
