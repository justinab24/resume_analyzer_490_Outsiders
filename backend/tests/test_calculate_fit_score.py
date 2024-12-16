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

def test_preprocess_text_with_bad_inputs():
    # Test for numeric input that is not a string
    with pytest.raises(ValueError, match="Empty or non-string input provided to preprocess_text function"):
        preprocess_text("")
    
    # Test for non-string input
    with pytest.raises(ValueError, match="Empty or non-string input provided to preprocess_text function"):
        preprocess_text(None)  # Non-string input
    
    with pytest.raises(ValueError, match="Input text contains only numeric characters"):
        preprocess_text("1234567890")

def test_preprocess_text_with_normal_input():
    """
    Test preprocess_text with normal inputs.
    """
    text = "Experienced Python Developer! Skilled in Java, AWS, and Docker."
    expected_tokens = ["experienced", "python", "developer", "skilled", "java", "aws", "docker"]
    
    # Mock nltk's word_tokenize and stopwords.words
    with patch('utils.calculate_fit_score.word_tokenize', return_value=expected_tokens), \
         patch('utils.calculate_fit_score.stopwords.words', return_value=["in", "and"]):
        
        result = preprocess_text(text)
    
        assert result == expected_tokens

def preprocess_side_effect_partial(arg):
    if arg == "Skilled Python developer with expertise in Java, AWS, Docker":
        return ["java", "python", "aws", "docker"]
    elif arg == "Required: Python, Java, AWS. Preferred: Docker and Kubernetes":
        return ["python", "java", "aws", "docker", "kubernetes"]
    elif arg == "Required: Python, Java, AWS":
        return ["python", "java", "aws"]
    else:
        return ["docker", "kubernetes"]
    
def preprocess_side_effect_full(arg):
    if arg == "Skilled Python developer with expertise in Java, AWS, Docker":
        return ["java", "python", "aws", "docker"]
    elif arg == "Required: Python, Java, AWS. Preferred: Docker":
        return ["python", "java", "aws", "docker"]
    elif arg == "Required: Python, Java, AWS":
        return ["python", "java", "aws"]
    else:
        return ["docker"]


def test_calculate_fit_score_partial_matches():
    """
    Test calculate_fit_score function.
    """
    resume_text = "Skilled Python developer with expertise in Java, AWS, Docker"
    job_description = "Required: Python, Mongo, SQL. Preferred: Azure and Salesforces"

    mock_token_filter_response = {
        "filtered_words": ['java', 'aws', 'python', 'docker']
    }

    mock_job_description_sections_response_content = {
        "required": "Required: Python, Java, AWS",
        "preferred": "Preferred: Docker and Kubernetes"
    }

    with patch('utils.calculate_fit_score.token_filter', return_value=mock_token_filter_response), \
         patch('utils.calculate_fit_score.preprocess_text', side_effect=preprocess_side_effect_partial), \
         patch('utils.calculate_fit_score.job_description_sections', return_value=mock_job_description_sections_response_content):

        result = calculate_fit_score(resume_text, job_description)

        assert result["weighted_token_score"] == 60.0
        assert result["unweighted_token_score"] == 50.0

def test_calculate_fit_score_full_matches():
    """
    Test calculate_fit_score function.
    """
    resume_text = "Skilled Python developer with expertise in Java, AWS, Docker"
    job_description = "Required: Python, Java, AWS. Preferred: Docker"

    mock_token_filter_response = {
        "filtered_words": ['java', 'aws', 'python', 'docker']
    }

    mock_job_description_sections_response_content = {
        "required": "Required: Python, Java, AWS",
        "preferred": "Preferred: Docker"
    }

    with patch('utils.calculate_fit_score.token_filter', return_value=mock_token_filter_response), \
         patch('utils.calculate_fit_score.preprocess_text', side_effect=preprocess_side_effect_full), \
         patch('utils.calculate_fit_score.job_description_sections', return_value=mock_job_description_sections_response_content):

        result = calculate_fit_score(resume_text, job_description)

        assert result["weighted_token_score"] == 60.0
        assert result["unweighted_token_score"] == 100.0

# def test_calculate_fit_score_empty_input(mock_job_description_sections, mock_token_filter):
#     """
#     Test calculate_fit_score with empty resume text or job description.
#     """
#     assert calculate_fit_score("", "Required: Python, Java, AWS.") == {
#         "fit_score": 0,
#         "matched_keywords": [],
#         "unmatched_critical_keywords": []
#     }

#     assert calculate_fit_score("Skilled Python developer.", "") == {
#         "fit_score": 0,
#         "matched_keywords": [],
#         "unmatched_critical_keywords": []
#     }


# def test_calculate_fit_score_no_match(mock_job_description_sections, mock_token_filter):
#     """
#     Test calculate_fit_score with no overlapping keywords.
#     """
#     resume_text = "Skilled in Ruby and Perl."
#     job_description = "Required: Python, Java, AWS. Preferred: Docker and Kubernetes."

#     result = calculate_fit_score(resume_text, job_description)

#     assert result["weighted_token_score"] == 0.0
#     assert result["unweighted_token_score"] == 0.0


# def test_calculate_fit_score_partial_match(mock_job_description_sections, mock_token_filter):
#     """
#     Test calculate_fit_score with some matching keywords.
#     """
#     resume_text = "Experienced Python and Docker developer."
#     job_description = "Required: Python, Java, AWS. Preferred: Docker and Kubernetes."

#     result = calculate_fit_score(resume_text, job_description)

#     # Check weighted score
#     assert result["weighted_token_score"] > 0.0
#     # Check unweighted score based on partial matches
#     assert result["unweighted_token_score"] > 0.0
