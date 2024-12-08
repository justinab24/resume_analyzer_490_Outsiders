def parse_ai_api_response(api_response):
    """
    Parses the AI API response to extract the fit score and feedback.

    Parameters:
    - api_response (dict): Raw response from the NLP API.

    Returns:
    - dict: Parsed response with fit score (percentage) and formatted feedback, or an error message.
    """
    try:
        if not api_response or "results" not in api_response or not api_response["results"]:
            raise ValueError("Malformed API response")

        result = api_response["results"][0]

        fit_score = result.get("fit_score", 0) * 100

        feedback = result.get("feedback", [])

        return {
            "fit_score": round(fit_score),
            "feedback": feedback
        }

    except Exception as e:
        return {
            "error": "Failed to generate analysis results."
        }
