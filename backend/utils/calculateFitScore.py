import string
from collections import Counter

def preprocess_text(text):
    """
    Tokenizes and normalizes text by converting to lowercase, removing punctuation, and splitting into words.
    """
    if not text or not isinstance(text, str):
        return []
    
    # Remove punctuation and convert to lowercase
    text = text.translate(str.maketrans('', '', string.punctuation)).lower()
    
    # Split into words
    tokens = text.split()
    
    return tokens

def calculate_fit_score(resume_text, job_description):
    """
    Calculates a fit score based on keyword matching between the resume and job description.
    """
    if not resume_text or not job_description:
        return {
            "fit_score": 0,
            "matched_keywords": [],
            "unmatched_critical_keywords": []
        }
    
    resume_tokens = preprocess_text(resume_text)
    job_description_tokens = preprocess_text(job_description)
    
    job_description_counter = Counter(job_description_tokens)
    
    matched_keywords = set(resume_tokens) & set(job_description_tokens)
    unmatched_keywords = set(job_description_tokens) - set(resume_tokens)
    
    matched_count = sum(job_description_counter[key] for key in matched_keywords)
    total_count = sum(job_description_counter.values())
    fit_score = (matched_count / total_count) * 100 if total_count > 0 else 0
    
    return {
        "fit_score": round(fit_score, 2),
        "matched_keywords": list(matched_keywords),
        "unmatched_critical_keywords": list(unmatched_keywords)
    }

