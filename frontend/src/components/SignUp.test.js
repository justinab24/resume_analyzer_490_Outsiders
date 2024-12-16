import React from 'react';
import { render, screen, fireEvent, waitFor } from '@testing-library/react';
import axios from 'axios';
import { BrowserRouter as Router } from 'react-router-dom';
import SignUp from './SignUp';

jest.mock('axios');

describe('SignUp Component Tests', () => {
  test('successful signup', async () => {
    axios.post.mockResolvedValueOnce({
      data: { message: 'User registered successfully' },
    });

    render(
      <Router>
        <SignUp />
      </Router>
    );

    fireEvent.change(screen.getByPlaceholderText('Email'), { target: { value: 'test@example.com' } });
    fireEvent.change(screen.getByPlaceholderText('Username'), { target: { value: 'testuser' } });
    fireEvent.change(screen.getByPlaceholderText('Password'), { target: { value: 'password' } });
    fireEvent.click(screen.getByRole('button', { name: 'Sign Up' }));

    await waitFor(() => {
      expect(screen.getByText('User registered successfully')).toBeInTheDocument();
    });
  });

  test('failed signup', async () => {
    axios.post.mockRejectedValueOnce({
      response: { data: { detail: 'Email already exists' } },
    });

    render(
      <Router>
        <SignUp />
      </Router>
    );

    fireEvent.change(screen.getByPlaceholderText('Email'), { target: { value: 'test@example.com' } });
    fireEvent.change(screen.getByPlaceholderText('Password'), { target: { value: 'password' } });
    fireEvent.click(screen.getByRole('button', { name: 'Sign Up' }));

    await waitFor(() => {
      expect(screen.getByText('Email already exists')).toBeInTheDocument();
    });
  });
});