from dotenv import load_dotenv
from fastapi import FastAPI, File, Request, UploadFile, Form, HTTPException
from services.models import FeedbackItem, NLPInput, NLPOutput
from utils.parsing import split_description_by_headers
from pydantic import BaseModel
from nltk.corpus import stopwords
import os
import httpx
import time
import re
from collections import Counter


load_dotenv(dotenv_path="./backend/.env")
HF_API_KEY = os.getenv("HF_API_KEY")

STOP_WORDS = set(stopwords.words("english"))

def extract_missing_keywords(resume_text, job_description):
   
    def tokenize(text):
        return re.findall(r'\b\w+\b', text.lower())

    resume_tokens = tokenize(resume_text)
    job_tokens = tokenize(job_description)

    filtered_resume_tokens = [token for token in resume_tokens if token not in STOP_WORDS]
    filtered_job_tokens = [token for token in job_tokens if token not in STOP_WORDS]

    missing_keywords = [
        word for word in filtered_job_tokens if word not in filtered_resume_tokens
    ]

    suggestions = [
        f"Include skills or experience related to '{keyword}'."
        for keyword in missing_keywords
    ]

    return {
        "missing_keywords": missing_keywords,
        "suggestions": suggestions
    }

async def nlp_analyzer(nlp_input):
    print("We got the following arguments from the request")
    resume_text = nlp_input.resume_text
    job_description = nlp_input.job_description
    
    fitscore_url = "https://api-inference.huggingface.co/models/sentence-transformers/all-MiniLM-L6-v2"
    linkedin_skills_url = "https://api-inference.huggingface.co/models/algiraldohe/lm-ner-linkedin-skills-recognition"
    headers = {"Authorization": f"Bearer {HF_API_KEY}"}

    description_sections = split_description_by_headers(job_description)

    print("This is the job description sections we received: ", description_sections)

    print("This is the description sections")
    print(description_sections)

    fitscore_data = {
        "inputs": {
            "source_sentence": resume_text,
            "sentences": [job_description]
        }
    }

    async with httpx.AsyncClient() as client:
        # Fetch similarity score
        fitscore_response = await client.post(fitscore_url, headers=headers, json=fitscore_data)
        if fitscore_response.status_code != 200:
            fitscore_error = fitscore_response.json()
            print(f"Similarity API Error: {fitscore_error}")
            raise HTTPException(status_code=fitscore_response.status_code, detail=fitscore_error)
        fitscore_result = fitscore_response.json()
        fit_score = fitscore_result[0]

        # Extract skills from resume
        skill_extraction_data = {"inputs": resume_text}

        retries = 3
        for attempt in range(retries):
            resume_skills_response = await client.post(linkedin_skills_url, headers=headers, json=skill_extraction_data)
            if resume_skills_response.status_code == 503:
                if attempt < retries - 1:
                    print(f"Attempt {attempt + 1} failed with status 503. Retrying...")
                    time.sleep(1)  # Wait for 1 second before retrying
                    continue
                else:
                    resume_skills_response.raise_for_status()
            else:
                resume_skills_response.raise_for_status()
            break

        resume_skills_result = resume_skills_response.json()

        # Wait for 10 seconds before proceeding
        time.sleep(10)
        # Extract only the 'TECHNOLOGY' skills
        resume_skills = [entity["word"] for entity in resume_skills_result if entity["entity_group"] == "TECHNOLOGY" or entity["entity_group"] == "TECHNICAL" or entity["entity_group"] == "BUS"]

        # Extract skills from job description with retry logic
        retries = 3
        for attempt in range(retries):
            jd_skills_response = await client.post(linkedin_skills_url, headers=headers, json={"inputs": job_description})
            if jd_skills_response.status_code == 503:
                if attempt < retries - 1:
                    print(f"Attempt {attempt + 1} failed with status 403. Retrying...")
                    time.sleep(1)  # Wait for 1 second before retrying
                    continue
                else:
                    jd_skills_response.raise_for_status()
            else:
                jd_skills_response.raise_for_status()
            break

        jd_skills_result = jd_skills_response.json()

        job_skills = [entity for entity in jd_skills_result if entity["entity_group"] == "TECHNOLOGY" or entity["entity_group"] == "TECHNICAL" or entity["entity_group"] == "BUS"]

    # Calculate matched skills
    matched_skills = []
    matched_skills = [skill for skill in resume_skills if skill.lower() in [s["word"].lower() for s in job_skills] and skill.lower() not in matched_skills]

    missing_skills = []
    missing_projects = []
    missing_experiences = []

    for entity in job_skills:
        if entity["entity_group"] == "TECHNOLOGY":
            if entity["word"].lower() not in [s.lower() for s in resume_skills]:
                if entity["word"] in description_sections["required"]:
                    missing_skills.append({
                        "name": entity["word"],
                        "weight": "required"
                    })
                elif entity["word"] in description_sections["preferred"]:
                    missing_skills.append({
                        "name": entity["word"],
                        "weight": "preferred"
                    })
                else:
                    missing_skills.append({
                        "name": entity["word"],
                        "weight": "neither"
                    })
        elif entity["entity_group"] == "TECHNICAL":
            if entity["word"].lower() not in [s.lower() for s in resume_skills]:
                if entity["word"] in description_sections["required"]:
                    missing_projects.append({
                        "name": entity["word"],
                        "weight": "required"
                    })
                elif entity["word"] in description_sections["preferred"]:
                    missing_projects.append({
                        "name": entity["word"],
                        "weight": "preferred"
                    })
                else:
                    missing_projects.append({
                        "name": entity["word"],
                        "weight": "neither"
                    })
        elif entity["entity_group"] == "BUS":
            if entity["word"].lower() not in [s.lower() for s in resume_skills]:
                if entity["word"] in description_sections["required"]:
                    missing_experiences.append({
                        "name": entity["word"],
                        "weight": "required"
                    })
                elif entity["word"] in description_sections["preferred"]:
                    missing_experiences.append({
                        "name": entity["word"],
                        "weight": "preferred"
                    })
                else:
                    missing_experiences.append({
                        "name": entity["word"],
                        "weight": "neither"
                    })    
    # # Calculate missing skills
    analysis_result = extract_missing_keywords(resume_text, job_description)


    # missing_skills = [entity["word"] for entity in job_skills if entity["entity_group"] == "TECHNOLOGY" and entity["word"].lower() not in [s.lower() for s in resume_skills]]

    # # Calculate missing technology
    # missing_projects = [entity["word"] for entity in job_skills if entity["entity_group"] == "TECHNICAL" and entity["word"].lower() not in [s.lower() for s in resume_skills]]
    
    # missing_experience = [entity["word"] for entity in job_skills if entity["entity_group"] == "BUS" and entity["word"].lower() not in [s.lower() for s in resume_skills]]
    # Prepare feedback message for missing skills
    feedback = [
        FeedbackItem(message=suggestion, feedback_type="skills")
        for suggestion in analysis_result["suggestions"]
    ]

    for skill in missing_skills:
        feedback_message = f"Consider adding {skill['name']} ({skill['weight']}) to your skills."
        feedback_item = FeedbackItem(
            message=feedback_message,
            feedback_type="skills"
        )
        feedback.append(feedback_item)

    for project in missing_projects:
        feedback_message = f"Consider adding a project in {project['name']} ({project['weight']}) to your resume."
        feedback_item = FeedbackItem(
            message=feedback_message,
            feedback_type="projects"
        )
        feedback.append(feedback_item)

    for experience in missing_experiences:
        feedback_message = f"Consider highlighting professional experience with {experience['name']} ({experience['weight']}) on your resume."
        feedback_item = FeedbackItem(
            message=feedback_message,
            feedback_type="professional experience"
        )
        feedback.append(feedback_item)


    response = {
        "similarity_score": round(fit_score * 100, 2),
        "keywords_matched": matched_skills,
        "missing_keywords": analysis_result["missing_keywords"],
        "feedback_raw": feedback,
    }

    print("This is the response we are getting now")
    print(response)

    return response