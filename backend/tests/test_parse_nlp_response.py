import pytest
from unittest.mock import MagicMock
from utils.models import NLPInput, NLPOutput, FeedbackItem
from utils.parse_nlp_response import parse_nlp_response  # adjust import based on your structure

# Test case for a valid API response
def test_parse_nlp_response_valid():
    api_response = {
        "results": {
            "similarity_score": 0.85,
            "matched_skills": ["Python", "Machine Learning"],
            "feedback_raw": [
                {"category": "strength", "text": "Great experience in Python."},
                {"category": "improvement", "text": "Could improve on machine learning concepts."}
            ]
        }
    }

    result = parse_nlp_response(api_response)

    assert isinstance(result, NLPOutput)
    assert result.similarity_score == 0.85
    assert result.keywords_matched == ["Python", "Machine Learning"]
    assert len(result.feedback_raw) == 2
    assert result.feedback_raw[0].category == "strength"
    assert result.feedback_raw[0].text == "Great experience in Python."

# Test case for a malformed response (missing results)
def test_parse_nlp_response_missing_results():
    api_response = {}  # No "results" key
    
    result = parse_nlp_response(api_response)

    assert "error" in result
    assert result["error"] == "Failed to generate analysis results."

# Test case for a valid response with missing fields (e.g., missing feedback)
def test_parse_nlp_response_missing_fields():
    api_response = {
        "results": {
            "similarity_score": 0.75,
            "matched_skills": ["Data Science"]
        }
    }

    result = parse_nlp_response(api_response)

    assert isinstance(result, NLPOutput)
    assert result.similarity_score == 0.75
    assert result.keywords_matched == ["Data Science"]
    assert result.feedback_raw == []  # Should be empty since feedback_raw is missing

# Test case for an empty API response
def test_parse_nlp_response_empty():
    api_response = None  # Empty response
    
    result = parse_nlp_response(api_response)

    assert "error" in result
    assert result["error"] == "Failed to generate analysis results."

# Test case for an invalid feedback structure
def test_parse_nlp_response_invalid_feedback():
    api_response = {
        "results": {
            "similarity_score": 0.90,
            "matched_skills": ["AI", "Deep Learning"],
            "feedback_raw": "Invalid feedback format, should be list."
        }
    }

    result = parse_nlp_response(api_response)

    assert "error" in result
    assert result["error"] == "Failed to generate analysis results."