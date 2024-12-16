import React, { useState } from 'react';
import axios from 'axios';
import '../stylesheet/resume.css';
import Popup from 'reactjs-popup';
import 'reactjs-popup/dist/index.css';

const ResumeForm = ({ setFitScore, setMatchedSkills, setImprovementSuggestions, setLoading, setShowDashboard }) => {
  const MAX_CHAR_LIMIT = 5000; 
  const MAX_FILE_SIZE = 2 * 1024 * 1024;

  const [resume, setResume] = useState(null);
  const [charCount, setCharcount] = useState(MAX_CHAR_LIMIT);
  const [jobDescription, setJobDescription] = useState('');
  const [resumeError, setResumeError] = useState('');
  const [descError, setDescError] = useState('');
  const [submissionMessage, setSubmissionMessage] = useState('');
  const [descWarning, setDescWarning] = useState('');
  const [errorMessage, setErrorMessage] = useState('');
  const [showErrorModal, setShowErrorModal] = useState(false);

  const fileUpload = (e) => {
    const file = e.target.files[0];
    if (file) {
      if (file.type !== 'application/pdf' && file.type !== 'application/vnd.openxmlformats-officedocument.wordprocessingml.document') {
        setResumeError('Only PDF and DOCX files are allowed');
        setResume(null);
      } else if (file.size > MAX_FILE_SIZE) {
        setResumeError('File size must be less than 2MB');
        setResume(null);
      } else {
        setResumeError('');
        setResume(file);
      }
    } else {
      setResumeError('');
    }
  };


  const jobDescript = (e) => {
    const input = e.target.value;
    const remainingChars = MAX_CHAR_LIMIT - input.length;

    setJobDescription(input);
    setCharcount(remainingChars);

    if (remainingChars < 0) {
      setDescError('Input cannot exceed 5000 characters');
      setDescWarning('');
    } else if (remainingChars < 20) {
      setDescError('');
      setDescWarning('Warning: Less than 20 characters remaining');
    } else {
      setDescWarning('');
      setDescError('');
    }
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
  
    // Immediately set loading to true
    setLoading(true);
    
    // Reset any previous error states
    setErrorMessage('');
    setShowErrorModal(false);
  
    if (resumeError || descError || !resume || jobDescription.trim() === '') {
      setErrorMessage('Please ensure resume is uploaded and job description is filled out.');
      setShowErrorModal(true);
      setLoading(false);
      return;
    }
  
    const formData = new FormData();
    formData.append('file', resume);
  
    try {
      const resumeResponse = await axios.post('http://localhost:8000/api/resume-upload', formData, {
        headers: { 'Content-Type': 'multipart/form-data' },
      });
  
      if (resumeResponse.status !== 200) {
        throw new Error('Failed to upload resume');
      }
  
      const jobDescriptionResponse = await axios.post('http://localhost:8000/api/job-description', 
        { text: jobDescription }, 
        { headers: { 'Content-Type': 'application/json' } }
      );
  
      if (jobDescriptionResponse.status === 200) {
        const analyzeResponse = await axios.post('http://localhost:8000/api/fit-score', 
          {
            resume_text: resumeResponse.data.extracted_text,
            job_description: jobDescription,
          },
          { headers: { 'Content-Type': 'application/json' } }
        );
  
        setFitScore({
          total: analyzeResponse.data.similarity_score,
          matched: 50,
          partial: 15,
          missing: 35,
        });
  
        setMatchedSkills(analyzeResponse.data.keywords_matched);
        setImprovementSuggestions(analyzeResponse.data.feedback_raw);
        setShowDashboard(true);
      } else {
        setSubmissionMessage('Failed to submit job description.');
        throw new Error('Job description submission failed');
      }
    } catch (error) {
      if (error.response) {
        if (error.response.status === 503) {
          setErrorMessage('Server is unavailable (503). Please refresh the page and try again.');
        } else {
          setErrorMessage('Error during submission: ' + error.message);
        }
      } else if (error.message === 'Network Error') {
        setErrorMessage('Server Network error. Please refresh the page and try again.');
      } else {
        setErrorMessage('An unexpected error occurred: ' + error.message);
      }
      setShowErrorModal(true);
    } finally {
      // Ensure loading is set to false in all scenarios
      setLoading(false);
    }
  };

  return (
    <div>
      <form onSubmit={handleSubmit}>
        {/* Resume Upload Section */}
        <div>
          <label htmlFor="resume">Upload Resume (PDF and Docx Only):</label>
          <input type="file" id="resume" accept=".pdf,.docx" onChange={fileUpload} />
          {resumeError && <div className="error">{resumeError}</div>}
        </div>

        <br />

        {/* Job Description Section */}
        <div>
          <label htmlFor="jobDescription">Job Description:</label>
          <textarea
            id="jobDescription"
            rows="10"
            cols="50"
            value={jobDescription}
            onChange={jobDescript}
            maxLength={MAX_CHAR_LIMIT}
          />
          <div>Characters remaining: {charCount}</div>
          {descWarning && <div className="warning">{descWarning}</div>}
          {descError && <div className="error">{descError}</div>}
        </div>

        <br />

        {/* Submit Button */}
        <button type="submit">Submit</button>
        {submissionMessage && <div>{submissionMessage}</div>}
      </form>

      {/* Error Popup */}
      <Popup open={showErrorModal} onClose={() => setShowErrorModal(false)} closeOnDocumentClick>
        <div className="error-popup">
          <h2>!!!</h2>
          <p>{errorMessage}</p>
          <button onClick={() => setShowErrorModal(false)}>Close</button>
        </div>
      </Popup>
    </div>
  );
};

export default ResumeForm;