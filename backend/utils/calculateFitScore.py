import string
from collections import Counter
from utils.nlp_functions import token_filter, job_description_sections
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize

nltk.download('punkt_tab')
nltk.download('punkt')
nltk.download('stopwords')

def preprocess_text(text):
    """
    Tokenizes and normalizes text by converting to lowercase, removing punctuation, and splitting into words.
    """
    if not text or not isinstance(text, str):
        return []
    
    # Remove punctuation and convert to lowercase
    text = text.translate(str.maketrans('', '', string.punctuation)).lower()

    tokens = word_tokenize(text)

    stop_words = set(stopwords.words('english'))

    filtered_tokens = [word for word in tokens if word.isalpha() and word not in stop_words]
    
    return filtered_tokens

def calculate_fit_score(resume_text, job_description):
    """
    Calculates a fit score based on keyword matching between the resume and job description.
    """
    print("we are in the calculate fit score function")
    if not resume_text or not job_description:
        return {
            "fit_score": 0,
            "matched_keywords": [],
            "unmatched_critical_keywords": []
        }

    description_sections = job_description_sections(job_description)
    required_tokens = preprocess_text(description_sections["required"])
    preferred_tokens = preprocess_text(description_sections["preferred"])
    
    resume_tokens = preprocess_text(resume_text)
    job_description_tokens = preprocess_text(job_description)
    
    print("Resume Tokens: ", resume_tokens)
    print("Job Description Tokens: ", job_description_tokens)
    
    job_description_counter = Counter(job_description_tokens)
    
    matched_keywords = set(resume_tokens) & set(job_description_tokens)
    matched_keywords_list = list(matched_keywords)

    print("Matched Keywords: ", matched_keywords)
    
    filtered_matched_keywords = token_filter(matched_keywords_list)
    print("Filtered Matched Keywords: ", filtered_matched_keywords)

    total_matched = len(matched_keywords)

    matched_count = sum(job_description_counter[key] for key in matched_keywords)


    requiredCounter = 0
    preferredCounter = 0
    neitherCounter = 0
    
    for word in filtered_matched_keywords["filtered_words"]:
        if word.lower() in required_tokens:
            requiredCounter += 1
        elif word.lower() in preferred_tokens:
            preferredCounter += 1
        else:
            neitherCounter += 1
    
    print("Here are the two counts")
    print(requiredCounter)
    print(preferredCounter)
    print(neitherCounter)
    print(total_matched)
    print(matched_count)

    total_filtered = len(filtered_matched_keywords["filtered_words"])
    if total_filtered == 0:
        weighted_token_score = 0
    else:
        # Weighted score calculation, capped at 100
        weighted_token_score = (
            (requiredCounter / (requiredCounter + preferredCounter)) * 70 +
            (preferredCounter / (requiredCounter + preferredCounter)) * 30
        )

    print("We generate this weighted fit score: ", weighted_token_score)
    
    total_count = sum(job_description_counter.values())

    unweighted_token_score = (matched_count / total_count) * 100 if total_count > 0 else 0

    print("We generate this unweighted fit score: ", unweighted_token_score)

    response = {
        "weighted_token_score": round(weighted_token_score, 2),
        "unweighted_token_score": round(unweighted_token_score, 2),
    }

    print("We generate this response: ")
    print(response)
    
    return response
