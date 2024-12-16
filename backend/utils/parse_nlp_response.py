from utils.models import NLPInput, NLPOutput, FeedbackItem

def parse_nlp_response(api_response):
    print("Do we hit this parser point")
    """
    Parses the AI API response to extract the fit score and feedback.

    Parameters:
    - api_response (dict): Raw response from the NLP API.

    Returns:
    - NLP Output data structure defined in models.py
    """
    try:
        if not api_response or "results" not in api_response or not api_response["results"]:
            raise ValueError("Malformed API response")
        
        print("we got this api response")
        print(api_response)

        result = api_response["results"]

        similarity_score = result.get("similarity_score")
        matched_skills = result.get("matched_skills", [])
        feedback_raw = result.get("feedback_raw", [])

        print("Similarity Score:", similarity_score)
        print("Matched Skills:", matched_skills)
        print("Feedback Raw:", feedback_raw)
        
        feedback_items = []
        for feedback in feedback_raw:
            feedback_item = FeedbackItem(
            category=feedback.get("category"),
            text=feedback.get("text")
            )
            feedback_items.append(feedback_item)
        
        print("Feedback Items:", feedback_items)

        nlp_output = NLPOutput(
            similarity_score=similarity_score,
            keywords_matched=matched_skills,
            feedback_raw=feedback_items
        )


        return nlp_output
    
    except Exception as e:
        return {
            "error": "Failed to generate analysis results."
        }
