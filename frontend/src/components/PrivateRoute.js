import React from 'react';
import { Route, Navigate } from 'react-router-dom';

const PrivateRoute = ({ element, ...rest }) => {
  const token = localStorage.getItem('token');

  // Function to check if the token is expired
  const isTokenExpired = (token) => {
    if (!token) return true; // No token means it's expired or doesn't exist
    const decoded = JSON.parse(atob(token.split('.')[1])); // Decode the token to get the payload
    const expiration = decoded.exp * 1000; // Convert expiration to milliseconds
    return Date.now() > expiration; // Compare current time with expiration time
  };

  const isAuthenticated = token && !isTokenExpired(token);

  // If the token is not present or expired, redirect to login
  return isAuthenticated ? element : <Navigate to="/login" />;
};

export default PrivateRoute;