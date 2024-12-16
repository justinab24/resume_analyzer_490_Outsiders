from fastapi import HTTPException
import pytest
from unittest.mock import patch, AsyncMock, MagicMock
from utils.nlp_functions import openai_analysis, token_filter, job_description_sections
from tests.conftest import MockChatCompletion, MockChoice, MockChatCompletionMessage
from utils.models import NLPInput
from openai import OpenAIError
import json
import requests

@pytest.fixture
def mock_openai_client_with_invalid_or_missing_key():
    """Fixture to simulate invalid API key behavior."""
    # Simulate an invalid API response
    mock_client = MagicMock()
    
    # Create an OpenAIError and set the http_status attribute
    mock_error = OpenAIError("Invalid or missing API Key")
    mock_error.http_status = 401  # Set HTTP status code to 401 for invalid key
    
    # Simulating a request that raises an error due to invalid API key
    mock_client.chat.completions.create = MagicMock(side_effect=mock_error)
    
    return mock_client


@pytest.fixture
def mock_get_openai_client_for_invalid_or_missing_key(mock_openai_client_with_invalid_or_missing_key):
    """Fixture to mock get_openai_client with invalid key."""
    with patch('utils.nlp_functions.get_openai_client', return_value=mock_openai_client_with_invalid_or_missing_key):
        yield mock_openai_client_with_invalid_or_missing_key


print("testing invalid or missing key for openai_analysis...")
def test_openai_analysis_invalid_or_missing_api_key(mock_get_openai_client_for_invalid_or_missing_key):
    """Test token_filter function when API key is invalid."""
    resume_text = 'Experienced software engineer with expertise in Python and JavaScript.'
    job_description = 'Looking for a software engineer with experience in Python and JavaScript.'
    
    # Simulate invalid API key by raising an HTTP exception
    with pytest.raises(HTTPException) as excinfo:
        openai_analysis(resume_text, job_description)
    
    # Check that the exception is of type HTTPException with the correct status code and message
    assert excinfo.value.status_code == 401  # Expecting 401 for authentication errors
    assert "Invalid or missing API Key" in str(excinfo.value.detail)  # Matches the raised error message

print("testing invalid or missing key for token_filter...")
def test_token_filter_invalid_or_missing_api_key(mock_get_openai_client_for_invalid_or_missing_key):
    """Test token_filter function when API key is invalid."""
    tokens = ['javascript', 'python', 'java', 'build', 'computer']
    
    # Simulate invalid API key by raising an HTTP exception
    with pytest.raises(HTTPException) as excinfo:
        token_filter(tokens)
    
    # Check that the exception is of type HTTPException with the correct status code and message
    assert excinfo.value.status_code == 401  # Expecting 401 for authentication errors
    assert "Invalid or missing API Key" in str(excinfo.value.detail)  # Matches the raised error message

print("testing invalid or missing key for job_description_sections...")
def test_job_description_sections_invalid_or_missing_api_key(mock_get_openai_client_for_invalid_or_missing_key):
    """Test token_filter function when API key is invalid."""
    job_description = 'Required Skills: be a good software engineer Preferred Skills: be a great software engineer'
    
    
    # Simulate invalid API key by raising an HTTP exception
    with pytest.raises(HTTPException) as excinfo:
        job_description_sections(job_description)
    
    # Check that the exception is of type HTTPException with the correct status code and message
    assert excinfo.value.status_code == 401  # Expecting 401 for authentication errors
    assert "Invalid or missing API Key" in str(excinfo.value.detail)  # Matches the raised error message

@pytest.fixture
def mock_openai_client_for_analysis():
    """Fixture to mock OpenAI API client for openai_analysis"""
    openai_analysis_response_content = {
        "matched_skills": ["Java", "JavaScript", "SQL"],
        "missing_skills": [
            {"name": "Typescript", "type": "required"},
            {"name": "AWS", "type": "required"},
            {"name": "noSQL", "type": "preferred"},
            {"name": "DocumentDB", "type": "preferred"},
            {"name": "Lambda", "type": "preferred"},
            {"name": "serverless", "type": "preferred"}
        ],
        "feedback_raw": [
            "Consider adding experience with AWS Cloud services.",
            "Include Typescript in your skills section.",
            "Enhance your resume with serverless application experience."
        ]
    }
    
    # Create the mock response for openai_analysis
    mock_openai_analysis_response = MagicMock()
    mock_openai_analysis_response.choices = [MagicMock(message=MagicMock(content=json.dumps(openai_analysis_response_content)))]
    
    mock_client = MagicMock()
    mock_client.chat.completions.create = MagicMock(return_value=mock_openai_analysis_response)
    
    return mock_client

@pytest.fixture
def mock_openai_client_for_token_filter():
    """Fixture to mock OpenAI API client for token_filter"""
    token_filter_response_content = {
        "filtered_words": ['javascript', 'python', 'java']
    }
    
    # Create the mock response for token_filter
    mock_token_filter_response = MagicMock()
    mock_token_filter_response.choices = [MagicMock(message=MagicMock(content=json.dumps(token_filter_response_content)))]
    
    mock_client = MagicMock()
    mock_client.chat.completions.create = MagicMock(return_value=mock_token_filter_response)
    
    return mock_client

@pytest.fixture
def mock_openai_client_for_job_description():
    """Fixture to mock OpenAI API client for job_description_sections"""
    job_description_sections_response_content = {
        "required": "be a good software engineer",
        "preferred": "be a great software engineer"
    }
    
    # Create the mock response for job_description_sections
    mock_job_description_sections_response = MagicMock()
    mock_job_description_sections_response.choices = [MagicMock(message=MagicMock(content=json.dumps(job_description_sections_response_content)))]
    
    mock_client = MagicMock()
    mock_client.chat.completions.create = MagicMock(return_value=mock_job_description_sections_response)
    
    return mock_client

@pytest.fixture
def mock_get_openai_client_for_analysis(mock_openai_client_for_analysis):
    """Fixture to mock get_openai_client function for openai_analysis"""
    with patch('utils.nlp_functions.get_openai_client', return_value=mock_openai_client_for_analysis):
        yield mock_openai_client_for_analysis

@pytest.fixture
def mock_get_openai_client_for_token_filter(mock_openai_client_for_token_filter):
    """Fixture to mock get_openai_client function for token_filter"""
    with patch('utils.nlp_functions.get_openai_client', return_value=mock_openai_client_for_token_filter):
        yield mock_openai_client_for_token_filter

@pytest.fixture
def mock_get_openai_client_for_job_description(mock_openai_client_for_job_description):
    """Fixture to mock get_openai_client function for job_description_sections"""
    with patch('utils.nlp_functions.get_openai_client', return_value=mock_openai_client_for_job_description):
        yield mock_openai_client_for_job_description

print("testing openai_analysis...")
def test_openai_analysis(mock_get_openai_client_for_analysis):
    resume_text = 'Experienced software engineer with expertise in Python and JavaScript.'
    job_description = 'Looking for a software engineer with experience in Python and JavaScript.'
    
    # Create NLPInput instance
    nlp_input = NLPInput(resume_text=resume_text, job_description=job_description)

    # Call the openai_analysis function
    result = openai_analysis(nlp_input.resume_text, nlp_input.job_description)

    # Assert the results
    assert result['matched_skills'] == ["Java", "JavaScript", "SQL"]
    assert result['missing_skills'][0]['name'] == "Typescript"
    assert result['feedback_raw'][0] == "Consider adding experience with AWS Cloud services."

print("testing token_filter...")
def test_token_filter(mock_get_openai_client_for_token_filter):
    tokens = ['javascript', 'python', 'java', 'build', 'computer']
    
    result = token_filter(tokens)

    assert result['filtered_words'] == ['javascript', 'python', 'java']

print("testing job_description_sections...")
def test_job_description_sections(mock_get_openai_client_for_job_description):
    job_description = 'Required Skills: be a good software engineer Preferred Skills: be a great software engineer'
    
    result = job_description_sections(job_description)

    assert result['required'] == "be a good software engineer"
    assert result['preferred'] == "be a great software engineer"