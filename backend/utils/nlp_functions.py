from dotenv import load_dotenv
from fastapi import FastAPI, File, Request, UploadFile, Form, HTTPException
from fastapi.responses import JSONResponse
from utils.models import FeedbackItem, NLPInput, NLPOutput
from pydantic import BaseModel
import json
import os
import httpx
import time
from openai import OpenAI
import re

load_dotenv()

client = OpenAI(
    api_key = os.getenv("OPENAI_AI_KEY")
)

load_dotenv(dotenv_path="./backend/.env")
HF_API_KEY = os.getenv("HF_API_KEY")

async def nlp_analysis(nlp_input):

    print("We are in the nlp_analysis function")

    resume_text = nlp_input.resume_text
    job_description = nlp_input.job_description
    
    sim_score = await nlp_simscore(resume_text, job_description)

    nlp_response = openai_analysis(resume_text, job_description)

    nlp_output = NLPOutput(
        similarity_score=sim_score,
        keywords_matched=nlp_response["matched_skills"],
        feedback_raw=nlp_response["feedback_raw"]
    )

    return nlp_output

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
        print("We got the following sim score")
        print(simscore_result)
        sim_score = round(simscore_result[0] * 100, 1)
        return sim_score

def openai_analysis(resume_text, job_description):

    prompt = f"""
        I have a resume and a job description. I need you to compare the skills in the resume against the skills in the job description.
        Please provide:
        1. An array of skills that are common between the resume and job description. The exact word should be in both the resume and job description. Get ALL instances of this check thoroughly
        2. An array of objects that have a name and type field. Each object’s name should be a skill (just one word ie. teamwork, python, telemetry) that is in the job description but not the resume, and the type should be whether the skill is a required or preferred skill as per the job description.
        3. An array of feedback for improving the resume. This can cover skills, projects, experience, etc. Ensure the feedback isnt already on the resume

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
    

def token_filter(tokens):
    """
    Calculates the weight of each token based on its position in the job description.
    """
    prompt = f"""
        I have a list of words extracted from a resume, and I want to filter out any words that are not job-relevant skills.
        Skills include hard skills (e.g., tools, technologies, certifications, methodologies) and soft skills (e.g., communication, leadership).
        Use the job description to identify any industry-specific keywords.
        Return the following json object
       {{
            "filtered_words": [
                "Skill 1",
                "Skill 2",
            ]
        }}

        Words:
        {tokens}
    """

    
    try:
        # Correct API call for the latest OpenAI SDK
        response = client.chat.completions.create(
            model="gpt-4o-mini",  # Make sure the correct model is used (gpt-3.5-turbo, gpt-4, etc.)
            response_format={ "type": "json_object" },
            messages=[
                {"role": "system", "content": "You are an assistant that compares words to job descriptions."},
                {"role": "user", "content": prompt}
            ],
        )

        # Extract and return the result from the response
        result = response.choices[0].message.content.strip()
        print("raw result of weighted function")
        print(result)
        print("json result of weighted function")
        print(json.loads(result))

        return json.loads(result)

    except Exception as e:
        print(f"Error with OpenAI API: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error with OpenAI API: {str(e)}")
    
def job_description_sections(job_description):
    """
    Calculates the weight of each token based on its position in the job description.
    """
    prompt = f"""
        I have a job description. Typically a job description will tell you what skills are required and what skills are preferred. They'll use different phrasing to indicate this. Required sections will say things like "Basic Qualifications" "Required Skills" "Must haves" while preferred sections will say things like "Bonus" "Preferred skills" "Nice to have", things along these lines. I need you to tell me what sections of the job description are required skills and what sections are preferred skills. Return the following json object:
        1. Simply add all text in the section to its corresponding key in the object. Key and text should both be strings
       {{
            "required": "...",
            "preferred": "...",
        }}

        Job Description:
        {job_description}
    """

    
    try:
        # Correct API call for the latest OpenAI SDK
        response = client.chat.completions.create(
            model="gpt-4o-mini",  # Make sure the correct model is used (gpt-3.5-turbo, gpt-4, etc.)
            response_format={ "type": "json_object" },
            messages=[
                {"role": "system", "content": "You are an assistant that analyzes job descriptions."},
                {"role": "user", "content": prompt}
            ],
        )

        # Extract and return the result from the response
        result = response.choices[0].message.content.strip()
        print("raw result of weighted function")
        print(result)
        print("json result of weighted function")
        print(json.loads(result))

        return json.loads(result)

    except Exception as e:
        print(f"Error with OpenAI API: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error with OpenAI API: {str(e)}")