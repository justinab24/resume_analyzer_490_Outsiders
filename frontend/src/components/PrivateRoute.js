import React from 'react';
import { Navigate } from 'react-router-dom';

const PrivateRoute = ({ element, ...rest }) => {
  const token = localStorage.getItem('token');

  console.log("we got this token: ", token);
  // Function to check if the token is expired
  const isTokenExpired = (token) => {
    if (!token) return true; // No token means it's expired or doesn't exist
    const decoded = JSON.parse(atob(token.split('.')[1])); // Decode the token to get the payload
    const expiration = decoded.exp * 1000; // Convert expiration to milliseconds
    console.log("we got this expiration: ", expiration, Date.now());
    return Date.now() > expiration; // Compare current time with expiration time
  };

  console.log("is the token expired, ", isTokenExpired(token));

  const isAuthenticated = token && !isTokenExpired(token);

  // If the token is not present or expired, redirect to register
  return isAuthenticated ? element : <Navigate to="/register" />;
};

export default PrivateRoute;