<<<<<<< HEAD
import React, { useState } from 'react';
import axios from 'axios';
import { useNavigate } from 'react-router-dom';

const Login = () => {
  const navigate = useNavigate();
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [message, setMessage] = useState('');
=======
import React, { useState } from "react";
import axios from "axios";

const Login = () => {
  const [formData, setFormData] = useState({
    email: "",
    password: "",
  });

  const [error, setError] = useState("");
  const [success, setSuccess] = useState("");

  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData({ ...formData, [name]: value });
  };
>>>>>>> f2bd3a3 (Tasks 6 and 7)

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
<<<<<<< HEAD
      const response = await axios.post('http://localhost:8000/api/login', {
        email,
        password,
      });
      localStorage.setItem('token', response.data.token);
      setMessage('Login successful');
      navigate('/dashboard')
    } catch (error) {
      setMessage(error.response.data.detail || 'Error logging in');
=======
      const response = await axios.post("/api/login", formData);
      localStorage.setItem("token", response.data.token);
      setSuccess("Login successful");
      setError("");
    } catch (err) {
      setError(err.response?.data?.error || "Invalid credentials");
      setSuccess("");
>>>>>>> f2bd3a3 (Tasks 6 and 7)
    }
  };

  return (
    <div>
      <h2>Login</h2>
<<<<<<< HEAD
      <form onSubmit={handleSubmit}>
        <input
          type="email"
          placeholder="Email"
          value={email}
          onChange={(e) => setEmail(e.target.value)}
=======
      {error && <p style={{ color: "red" }}>{error}</p>}
      {success && <p style={{ color: "green" }}>{success}</p>}
      <form onSubmit={handleSubmit}>
        <input
          type="email"
          name="email"
          placeholder="Email"
          value={formData.email}
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
>>>>>>> f2bd3a3 (Tasks 6 and 7)
          required
        />
        <button type="submit">Login</button>
      </form>
<<<<<<< HEAD
      <p>{message}</p>
      <p>
        Don't have an account?{' '}
        <a href="/register">Register here</a>
      </p>
=======
>>>>>>> f2bd3a3 (Tasks 6 and 7)
    </div>
  );
};

export default Login;
