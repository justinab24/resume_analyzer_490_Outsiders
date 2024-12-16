import React from 'react';
import { render, screen, waitFor, fireEvent } from '@testing-library/react';
import Dashboard from './Dashboard';

jest.mock('./ResumeForm', () => ({ setFitScore, setMatchedSkills, setImprovementSuggestions, setLoading, setShowDashboard }) => (
  <div>
    <button onClick={() => {
      setFitScore({ total: 75, matched: 50, partial: 15, missing: 35 });
      setMatchedSkills(['Skill 1', 'Skill 2', 'Skill 3']);
      setImprovementSuggestions([
        { category: 'skills', text: 'Suggestion 1' },
        { category: 'experience', text: 'Suggestion 2' },
        { category: 'skills', text: 'Suggestion 3' },
      ]);
      setShowDashboard(true);
    }}>Set Suggestions</button>
    <button onClick={() => {
      setFitScore({ total: 75, matched: 50, partial: 15, missing: 35 });
      setMatchedSkills(['Skill 1', 'Skill 2', 'Skill 3']);
      setImprovementSuggestions([]);
      setShowDashboard(true);
    }}>Set Suggestions Empty</button>
    <button onClick={() => {
      setFitScore(null); // No fit score
      setImprovementSuggestions([
        { category: 'skills', text: 'Suggestion 1' },
        { category: 'experience', text: 'Suggestion 2' },
        { category: 'skills', text: 'Suggestion 3' },
      ]);
      setShowDashboard(true);
    }}>Set Suggestions with No Fit Score</button>
    <button onClick={() => {
      setLoading(true);// Simulate loading state
    }}>Start Loading</button>
    <button onClick={() => {
      setLoading(false); // Simulate loading state
    }}>Stop Loading</button>
  </div>
));

describe('Dashboard Component Tests', () => {
  test('Dashboard renders fit score correctly', async () => {
    render(<Dashboard />);
    fireEvent.click(screen.getByText('Set Suggestions'));

    await waitFor(() => {
      expect(screen.getByText(/75%/)).toBeInTheDocument();
    });
  });

  test('Dashboard renders improvement suggestions correctly', async () => {
    render(<Dashboard />);
    fireEvent.click(screen.getByText('Set Suggestions'));

    await waitFor(() => {
      expect(screen.getByText('Suggestion 1')).toBeInTheDocument();
      expect(screen.getByText('Suggestion 2')).toBeInTheDocument();
      expect(screen.getByText('Suggestion 3')).toBeInTheDocument();
    });
  });

  test('Dashboard renders matched skills correctly', async () => {
    render(<Dashboard />);
    fireEvent.click(screen.getByText('Set Suggestions'));

    await waitFor(() => {
      expect(screen.getByText('Skill 1')).toBeInTheDocument();
      expect(screen.getByText('Skill 2')).toBeInTheDocument();
      expect(screen.getByText('Skill 3')).toBeInTheDocument();
    });
  })

  test('Progress bar has the right visual size depending on the percentage', async () => {
    render(<Dashboard />);
    fireEvent.click(screen.getByText('Set Suggestions'));

    await waitFor(() => {
      const progressBar = screen.getByRole('progressbar');
      expect(progressBar).toHaveStyle('width: 75%');
    });
  });

  test('No improvement suggestions renders no feedback', async () => {
    render(<Dashboard />);
    fireEvent.click(screen.getByText('Set Suggestions Empty'));

    await waitFor(() => {
      expect(screen.queryByText('Suggestion 1')).not.toBeInTheDocument();
      expect(screen.queryByText('Suggestion 2')).not.toBeInTheDocument();
      expect(screen.queryByText('Suggestion 3')).not.toBeInTheDocument();
    });
  });

  test('Filters improvement suggestions via dropdown', async () => {
    render(<Dashboard />);
    fireEvent.click(screen.getByText('Set Suggestions'));

    // Simulate filtering by 'skills'
    fireEvent.change(screen.getByLabelText('Filter by Category'), { target: { value: 'skills' } });

    await waitFor(() => {
      expect(screen.getByText('Suggestion 1')).toBeInTheDocument();
      expect(screen.getByText('Suggestion 3')).toBeInTheDocument();
      expect(screen.queryByText('Suggestion 2')).not.toBeInTheDocument();
    });

    // Simulate filtering by 'experience'
    fireEvent.change(screen.getByLabelText('Filter by Category'), { target: { value: 'experience' } });

    await waitFor(() => {
      expect(screen.getByText('Suggestion 2')).toBeInTheDocument();
      expect(screen.queryByText('Suggestion 1')).not.toBeInTheDocument();
      expect(screen.queryByText('Suggestion 3')).not.toBeInTheDocument();
    });

    // Simulate showing all suggestions
    fireEvent.change(screen.getByLabelText('Filter by Category'), { target: { value: 'all' } });

    await waitFor(() => {
      expect(screen.getByText('Suggestion 1')).toBeInTheDocument();
      expect(screen.getByText('Suggestion 2')).toBeInTheDocument();
      expect(screen.getByText('Suggestion 3')).toBeInTheDocument();
    });
  });

  test('Handles no fit score', async () => {
    render(<Dashboard />);
    fireEvent.click(screen.getByText('Set Suggestions with No Fit Score'));

    await waitFor(() => {
      expect(screen.queryByRole('progressbar')).not.toBeInTheDocument();
      expect(screen.queryByText('Suggestion 1')).not.toBeInTheDocument();
      expect(screen.queryByText('Suggestion 2')).not.toBeInTheDocument();
      expect(screen.queryByText('Suggestion 3')).not.toBeInTheDocument();
    });
  });

  test('Spinner appears when loading is true and does not appear when loading is false', async () => {
    render(<Dashboard />);
    
    // Initially, loading is false, so the spinner should not be in the document
    expect(screen.queryByTestId('spinner')).not.toBeInTheDocument();

    // Simulate starting the loading state
    fireEvent.click(screen.getByText('Start Loading'));

    // The spinner should now be in the document
    await waitFor(() => {
      expect(screen.getByTestId('spinner')).toBeInTheDocument();
    });

    fireEvent.click(screen.getByText('Stop Loading'));

    // Wait for the loading state to be set to false
    await waitFor(() => {
      expect(screen.queryByTestId('spinner')).not.toBeInTheDocument();
    });
    
  });

});