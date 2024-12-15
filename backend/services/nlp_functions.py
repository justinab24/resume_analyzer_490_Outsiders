from dotenv import load_dotenv
from fastapi import FastAPI, File, Request, UploadFile, Form, HTTPException
from fastapi.responses import JSONResponse
from services.models import FeedbackItem, NLPInput, NLPOutput
from utils.parsing import split_description_by_headers
from pydantic import BaseModel
import json
import os
import httpx
import time
from openai import OpenAI
import re


client = OpenAI(
    api_key = os.getenv("OPEN_AI_KEY")
)



load_dotenv(dotenv_path="./backend/.env")
HF_API_KEY = os.getenv("HF_API_KEY")

async def nlp_analysis(nlp_input):
    resume_text = nlp_input.resume_text
    job_description = nlp_input.job_description
    
    sim_score = await nlp_simscore(resume_text, job_description)

    nlp_response = openai_analysis(resume_text, job_description)

    formatted_response = {
        "similarity_score": sim_score,
        "keywords_matched": nlp_response["matched_skills"],
        "feedback_raw": nlp_response["feedback_raw"]
    }


    return formatted_response

async def nlp_simscore(resume_text, job_description):
    url = "https://api-inference.huggingface.co/models/sentence-transformers/all-MiniLM-L6-v2"
    headers = {"Authorization": f"Bearer {HF_API_KEY}"}
    simscore_data = {
        "inputs": {
            "source_sentence": resume_text,
            "sentences": [job_description]
        }
    }
    async with httpx.AsyncClient() as client:
        simscore_response = await client.post(url, headers=headers, json=simscore_data)
        if simscore_response.status_code != 200:
            simscore_error = simscore_response.json()
            print(f"Similarity API Error: {simscore_error}")
            raise HTTPException(status_code=simscore_response.status_code, detail=simscore_error)
        simscore_result = simscore_response.json()
        sim_score = simscore_result[0]
        return sim_score

async def nlp_skill_extraction(text):
    url = "https://api-inference.huggingface.co/models/algiraldohe/lm-ner-linkedin-skills-recognition"
    headers = {"Authorization": f"Bearer {HF_API_KEY}"}
    async with httpx.AsyncClient() as client:
        retries = 3
        for attempt in range(retries):
            skills_response = await client.post(url, headers=headers, json={"inputs": text})
            if skills_response.status_code == 503:
                if attempt < retries - 1:
                    print(f"Attempt {attempt + 1} failed with status 403. Retrying...")
                    time.sleep(1) 
                    continue
                else:
                    skills_response.raise_for_status()
            else:
                skills_response.raise_for_status()
            break

        skills_result = skills_response.json()

        skills = [entity for entity in skills_result if entity["entity_group"] == "TECHNOLOGY" or entity["entity_group"] == "TECHNICAL" or entity["entity_group"] == "BUS"]

        return skills

def openai_analysis(resume_text, job_description):

    prompt = f"""
        I have a resume and a job description. I need you to compare the skills in the resume against the skills required in the job description.
        Please provide:
        1. An array of skills that match between the resume and job description.
        2. An array of objects that have a name and type field. Each object’s name should be a skill (just one word ie. teamwork, python, telemetry) that is in the job description but not the resume, and the type should be whether the skill is a required or preferred skill as per the job description.
        3. An array of feedback for improving the resume. This can cover skills, projects, experience, etc.

        Format your response as a json object like:

       {{
            "matched_skills": ["Skill 1", "Skill 2", ...],
            "missing_skills": [
                {{ "name": "Skill A", "type": "required" }},
                {{ "name": "Skill B", "type": "preferred" }},
                ...
            ],
            "feedback_raw": ["Feedback 1", "Feedback 2", ...]
        }}

        Resume:
        {resume_text}

        Job Description:
        {job_description}
    """

    try:
        # Correct API call for the latest OpenAI SDK
        response = client.chat.completions.create(
            model="gpt-4o-mini",  # Make sure the correct model is used (gpt-3.5-turbo, gpt-4, etc.)
            response_format={ "type": "json_object" },
            messages=[
                {"role": "system", "content": "You are an assistant that compares resumes to job descriptions."},
                {"role": "user", "content": prompt}
            ],
        )

        # Extract and return the result from the response
        result = response.choices[0].message.content.strip()
        print("raw result")
        print(result)
        print("json result")
        print(json.loads(result))

        return json.loads(result)

    except Exception as e:
        print(f"Error with OpenAI API: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error with OpenAI API: {str(e)}")