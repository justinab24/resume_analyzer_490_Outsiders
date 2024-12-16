import pytest
from collections import Counter
from unittest.mock import patch, MagicMock
from utils.nlp_functions import token_filter, job_description_sections
from utils.calculate_fit_score import preprocess_text, calculate_fit_score
import json

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
def mock_get_openai_client_for_token_filter(mock_openai_client_for_token_filter):
    """Fixture to mock get_openai_client function for token_filter"""
    with patch('utils.nlp_functions.get_openai_client', return_value=mock_openai_client_for_token_filter):
        yield mock_openai_client_for_token_filter

@pytest.fixture
def mock_job_description_sections():
    """
    Mock job_description_sections to return required and preferred sections.
    """
    with patch('utils.nlp_functions.job_description_sections') as mock_job_description:
        mock_job_description.return_value = {
            "required": "Python Java AWS",
            "preferred": "Docker Kubernetes CI/CD"
        }
        yield mock_job_description

def test_preprocess_text():
    """
    Test preprocess_text function.
    """
    # Normal case
    text = "Experienced Python Developer! Skilled in Java, AWS, and Docker."
    expected_tokens = ["experienced", "python", "developer", "skilled", "java", "aws", "docker"]
    assert preprocess_text(text) == expected_tokens

    # Edge cases
    assert preprocess_text("") == []
    assert preprocess_text(None) == []
    assert preprocess_text("!@#$%^&*()") == []
    assert preprocess_text("123456") == []
    assert preprocess_text(123) == []  # Non-string input


def test_calculate_fit_score(mock_job_description_sections, mock_token_filter):
    """
    Test calculate_fit_score function.
    """
    resume_text = "Skilled Python developer with expertise in Java and AWS."
    job_description = "Required: Python, Java, AWS. Preferred: Docker and Kubernetes."

    # Expected response structure
    expected_response = {
        "weighted_token_score": 70.0,  # All matches are required, so weighted score is 70
        "unweighted_token_score": pytest.approx(100.0, 0.1)  # All tokens match in job description
    }

    result = calculate_fit_score(resume_text, job_description)

    assert result["weighted_token_score"] == expected_response["weighted_token_score"]
    assert result["unweighted_token_score"] == expected_response["unweighted_token_score"]


def test_calculate_fit_score_empty_input(mock_job_description_sections, mock_token_filter):
    """
    Test calculate_fit_score with empty resume text or job description.
    """
    assert calculate_fit_score("", "Required: Python, Java, AWS.") == {
        "fit_score": 0,
        "matched_keywords": [],
        "unmatched_critical_keywords": []
    }

    assert calculate_fit_score("Skilled Python developer.", "") == {
        "fit_score": 0,
        "matched_keywords": [],
        "unmatched_critical_keywords": []
    }


def test_calculate_fit_score_no_match(mock_job_description_sections, mock_token_filter):
    """
    Test calculate_fit_score with no overlapping keywords.
    """
    resume_text = "Skilled in Ruby and Perl."
    job_description = "Required: Python, Java, AWS. Preferred: Docker and Kubernetes."

    result = calculate_fit_score(resume_text, job_description)

    assert result["weighted_token_score"] == 0.0
    assert result["unweighted_token_score"] == 0.0


def test_calculate_fit_score_partial_match(mock_job_description_sections, mock_token_filter):
    """
    Test calculate_fit_score with some matching keywords.
    """
    resume_text = "Experienced Python and Docker developer."
    job_description = "Required: Python, Java, AWS. Preferred: Docker and Kubernetes."

    result = calculate_fit_score(resume_text, job_description)

    # Check weighted score
    assert result["weighted_token_score"] > 0.0
    # Check unweighted score based on partial matches
    assert result["unweighted_token_score"] > 0.0
