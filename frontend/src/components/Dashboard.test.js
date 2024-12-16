import React from 'react';
import { render, screen, fireEvent } from '@testing-library/react';
import Dashboard from './Dashboard';

describe('Dashboard Component', () => {
  test('renders fit score visualization correctly', () => {
    const { getByText } = render(<Dashboard />);
    const fitScore = { total: 50, matched: 30, partial: 10, missing: 10 };
    expect(getByText(`${fitScore.total}%`)).toBeInTheDocument();
  });

  test('renders feedback list correctly', () => {
    const feedback = [
      { category: 'skills', text: 'Include experience with AWS services.' },
      { category: 'experience', text: 'Add projects demonstrating REST API development.' },
    ];
    render(<Dashboard />);
    feedback.forEach(item => {
      expect(screen.getByText(item.text)).toBeInTheDocument();
    });
  });

  test('filters feedback correctly', () => {
    const feedback = [
      { category: 'skills', text: 'Include experience with AWS services.' },
      { category: 'experience', text: 'Add projects demonstrating REST API development.' },
    ];
    render(<Dashboard />);
    fireEvent.change(screen.getByLabelText('Filter by Category'), { target: { value: 'skills' } });
    expect(screen.getByText('Include experience with AWS services.')).toBeInTheDocument();
    expect(screen.queryByText('Add projects demonstrating REST API development.')).toBeNull();
  });

  test('handles missing fit score', () => {
    render(<Dashboard />);
    expect(screen.getByText('0%')).toBeInTheDocument();
  });

  test('handles empty feedback list', () => {
    render(<Dashboard />);
    expect(screen.queryByText('Include experience with AWS services.')).toBeNull();
    expect(screen.queryByText('Add projects demonstrating REST API development.')).toBeNull();
  });
});
