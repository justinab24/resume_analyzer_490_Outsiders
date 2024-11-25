import React, { useState } from 'react';
import axios from 'axios';

const ResumeForm = () => {
  //used later for validation
  const MAX_CHAR_LIMIT = 5000; 
  const MAX_FILE_SIZE = 2 * 1024 * 1024;

  const [resume, setResume] = useState(null);
  const [charCount, setCharcount] = useState(MAX_CHAR_LIMIT);
  const [jobDescription, setJobDescription] = useState('');
  const [resumeError, setResumeError] = useState('');
  const [descError, setDescError] = useState('');
  const [submissionMessage, setSubmissionMessage] = useState('');
  

  // Check if file meets standards for upload
  const fileUpload = (e) => {
    const file = e.target.files[0];
    if (file) {
      if (file.type !== 'application/pdf') {
        setResumeError('Only PDF files are allowed');
        setResume(null);
      } else if (file.size > MAX_FILE_SIZE) {
        setResumeError('File size must be less than 2MB');
        setResume(null);
      } else {
        setResumeError('');
        setResume(file);
      }
    }
  };

  // Check input fields
  const jobDescript = (e) => {
    const input = e.target.value;
    const remainingChars = MAX_CHAR_LIMIT - input.length;

    setJobDescription(input);
    setCharcount(remainingChars);

    if (remainingChars < 100) {
      setDescError('');
    } else if (remainingChars < 0) {
      setDescError('Input cannot exceed 5000 characters');
    } else {
      setDescError('');
    }
  };

  // Form submission
  const handleSubmit = async (e) => {
    e.preventDefault();

    // Check for errors before submission
    if (resumeError || descError || !resume || jobDescription.trim() === '') {
      setSubmissionMessage('Errors exist: please fix errors before trying again');
      return;
    }

    const formData = new FormData();
    formData.append('jobDescription', jobDescription);
    formData.append('resume', resume);

    try {
      // First, upload the resume to /api/resume-upload
      const resumeResponse = await axios.post('/api/resume-upload', formData, {
        headers: { 'Content-Type': 'multipart/form-data' },
      });

      if (resumeResponse.status !== 200) {
        throw new Error('Failed to upload resume');
      }

      // Now submit the job description to /api/job-description
      const jobDescriptionResponse = await axios.post('/api/job-description', { jobDescription });

      if (jobDescriptionResponse.status === 200) {
        setSubmissionMessage('Submission successful!');
      } else {
        setSubmissionMessage('Failed to submit job description.');
      }
    } catch (error) {
      setSubmissionMessage('Error during submission: ' + error.message);
    }
  };

  return (
    <div>
      <h1>Upload Resume and Job Description</h1>
      <form onSubmit={handleSubmit}>

        {/* Resume Upload Section */}
        <div>
          <label htmlFor="resume">Upload Resume (PDF Only):</label>
          <input type="file" id="resume" accept=".pdf" onChange={fileUpload} />
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
          {descError && <div className="error">{descError}</div>}
        </div>

        <br />

        {/* Submit Button */}
        <button type="submit">Submit</button>
        {submissionMessage && <div>{submissionMessage}</div>}
      </form>
    </div>
  );
};

export default ResumeForm;
