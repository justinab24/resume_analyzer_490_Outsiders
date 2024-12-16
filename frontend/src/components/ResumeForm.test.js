import React from 'react';
import { render, screen, fireEvent, waitFor } from '@testing-library/react';
import axios from 'axios';
import ResumeForm from './ResumeForm';

jest.mock('axios');

describe('ResumeForm Component Tests', () => {
  test('renders the form elements correctly', () => {
    render(<ResumeForm setFitScore={jest.fn()} setMatchedSkills={jest.fn()} setImprovementSuggestions={jest.fn()} setLoading={jest.fn()} setShowDashboard={jest.fn()} />);
    
    expect(screen.getByLabelText(/Upload Resume/)).toBeInTheDocument();
    expect(screen.getByLabelText(/Job Description/)).toBeInTheDocument();
    expect(screen.getByText(/Submit/)).toBeInTheDocument();
  });

  test('displays error modal on submission error', async () => {
    axios.post.mockRejectedValueOnce({
      response: { status: 503 },
    });

    render(<ResumeForm setFitScore={jest.fn()} setMatchedSkills={jest.fn()} setImprovementSuggestions={jest.fn()} setLoading={jest.fn()} setShowDashboard={jest.fn()} />);

    fireEvent.change(screen.getByLabelText(/Upload Resume/), { target: { files: [new File(['resume'], 'resume.pdf', { type: 'application/pdf' })] } });
    fireEvent.change(screen.getByLabelText(/Job Description/), { target: { value: 'Job description text' } });
    fireEvent.click(screen.getByText(/Submit/));

    await waitFor(() => {
      expect(screen.getByText(/Server is unavailable/)).toBeInTheDocument();
    });
  });

  test('displays error message for invalid file type', () => {
    render(<ResumeForm setFitScore={jest.fn()} setMatchedSkills={jest.fn()} setImprovementSuggestions={jest.fn()} setLoading={jest.fn()} setShowDashboard={jest.fn()} />);

    fireEvent.change(screen.getByLabelText(/Upload Resume/), { target: { files: [new File(['resume'], 'resume.txt', { type: 'text/plain' })] } });

    expect(screen.getByText(/Only PDF and DOCX files are allowed/)).toBeInTheDocument();
  });

  test('displays error message for file size exceeding limit', () => {
    render(<ResumeForm setFitScore={jest.fn()} setMatchedSkills={jest.fn()} setImprovementSuggestions={jest.fn()} setLoading={jest.fn()} setShowDashboard={jest.fn()} />);

    const largeFile = new File(['a'.repeat(3 * 1024 * 1024)], 'large_resume.pdf', { type: 'application/pdf' });
    fireEvent.change(screen.getByLabelText(/Upload Resume/), { target: { files: [largeFile] } });

    expect(screen.getByText(/File size must be less than 2MB/)).toBeInTheDocument();
  });

  test('displays character count warning when job description is near limit', () => {
    render(<ResumeForm setFitScore={jest.fn()} setMatchedSkills={jest.fn()} setImprovementSuggestions={jest.fn()} setLoading={jest.fn()} setShowDashboard={jest.fn()} />);

    fireEvent.change(screen.getByLabelText(/Job Description/), { target: { value: 'a'.repeat(4981) } });

    expect(screen.getByText(/Warning: Less than 20 characters remaining/)).toBeInTheDocument();
  });

  test('displays error message when job description exceeds character limit', () => {
    render(<ResumeForm setFitScore={jest.fn()} setMatchedSkills={jest.fn()} setImprovementSuggestions={jest.fn()} setLoading={jest.fn()} setShowDashboard={jest.fn()} />);

    fireEvent.change(screen.getByLabelText(/Job Description/), { target: { value: 'a'.repeat(5001) } });

    expect(screen.getByText(/Input cannot exceed 5000 characters/)).toBeInTheDocument();
  });
});