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
    print("we are in the preprocess text function")
    print(text)

    if not text or not isinstance(text, str):
        print(f"Invalid input type: {type(text)}")
        print("we got an empty string")
        print(text)
        raise ValueError("Empty or non-string input provided to preprocess_text function")
    
    text = text.translate(str.maketrans('', '', string.punctuation)).lower()

    # # Check if text contains non-alphanumeric characters
    # non_alnum_chars = [char for char in text if not char.isalnum() and not char.isspace()]
    # if non_alnum_chars:
    #     print("we got non-alphanumeric characters:", non_alnum_chars)
    #     raise ValueError("Input text contains non-alphanumeric characters")
    
    # Check if text is purely numeric
    if text.isdigit():
        print("we got a numeric character")
        raise ValueError("Input text contains only numeric characters")

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

    required_section = description_sections["required"]
    preferred_section = description_sections["preferred"]
    
    resume_tokens = preprocess_text(resume_text)
    job_description_tokens = preprocess_text(job_description)
    
    job_description_counter = Counter(job_description_tokens)
    
    matched_keywords = set(resume_tokens) & set(job_description_tokens)

    missing_keywords = set(job_description_tokens) - set(resume_tokens)

    missing_keywords_list = list(missing_keywords)

    filtered_missing_keywords = token_filter(missing_keywords_list)

    missing_keywords_total = len(filtered_missing_keywords["filtered_words"])

    matched_keywords_list = list(matched_keywords)
    
    filtered_matched_keywords = token_filter(matched_keywords_list)

    total_matched = len(matched_keywords)

    matched_count = sum(job_description_counter[key] for key in matched_keywords)

    total_filtered = len(filtered_matched_keywords["filtered_words"])

    if total_filtered == 0:
        weighted_token_score = 0
    elif not required_section or not preferred_section:
        weighted_token_score = 0
    else:
        required_tokens = preprocess_text(description_sections["required"])
        preferred_tokens = preprocess_text(description_sections["preferred"])

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
        "matched_keywords": filtered_matched_keywords["filtered_words"],
        "missing_keywords_total": missing_keywords_total,
    }

    print("We generate this response: ")
    print(response)
    
    return response
