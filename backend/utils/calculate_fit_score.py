from services.skill_extraction import nlp_analyzer
from backend.utils.models import NLPInput

async def calculate_fit_score(resume_text, job_description):
    """
    Calculates the fit score using NLP analysis and keyword matching.
    """
    # Call nlp_analyzer for detailed analysis
    nlp_input = NLPInput(resume_text=resume_text, job_description=job_description)
    nlp_output = await nlp_analyzer(nlp_input)
    
    # Extract relevant data
    similarity_score = nlp_output['similarity_score']  # A percentage similarity score
    matched_keywords = nlp_output['keywords_matched']  # Keywords found in both
    feedback = nlp_output['feedback_raw']  # Feedback items

    # Calculate a weighted fit score
    total_keywords = len(nlp_output['keywords_matched']) + len(feedback)
    matches = len(matched_keywords)
    fit_score = int((matches / total_keywords) * 100) if total_keywords > 0 else 0

    return {
        "fit_score": fit_score,
        "similarity_score": similarity_score,
        "feedback": feedback
    }