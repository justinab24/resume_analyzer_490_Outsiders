from dotenv import load_dotenv
from fastapi import FastAPI, File, Request, UploadFile, Form, HTTPException
from fastapi.responses import JSONResponse
from utils.models import FeedbackItem, NLPInput, NLPOutput
from utils.parse_nlp_response import parse_nlp_response
from pydantic import BaseModel
import json
import os
import httpx
import time
from openai import OpenAIError
from openai import OpenAI
import re

load_dotenv()

def get_openai_client():
    return OpenAI(api_key=os.getenv("OPEN_AI_KEY"))

load_dotenv(dotenv_path="./backend/.env")

async def nlp_analysis(nlp_input):

    resume_text = nlp_input.resume_text
    job_description = nlp_input.job_description

    nlp_response = openai_analysis(resume_text, job_description)

    nlp_output = parse_nlp_response(nlp_response)

    return nlp_output

def openai_analysis(resume_text, job_description):

    client = get_openai_client()

    prompt = f"""
        I have a resume and a job description. I need you to compare the skills in the resume against the skills in the job description.
        Please provide:
        1: A similarity score between the two pieces of text as a percent (from 0 to 1)
        2. An array of skills that are common between the resume and job description. The exact word should be in both the resume and job description. Get ALL instances of this check thoroughly
        3. An array of feedback for improving the resume. This can cover skills, projects, experience, etc. Ensure the feedback isnt already on the resume. Also for each feedback categorize it as "skills" or "experience"

        Format your response as a json object like:

       {{
            "results": {{
                "similiarity_score": 0.85,
                "matched_skills": ["Skill 1", "Skill 2", ...],
                "feedback_raw": [
                    {{
                        "text": "Add skills related to project management.",
                        "category": "skills"
                    }},
                ]
            }}
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
    
    except OpenAIError as e:
        if e.http_status == 401:
            print(f"Authentication error: {str(e)}")
            raise HTTPException(status_code=401, detail=f"Invalid or missing API Key: {str(e)}")
        else:
            print(f"Error with OpenAI API: {str(e)}")
            raise HTTPException(status_code=500, detail=f"Error with OpenAI API: {str(e)}")
    

def token_filter(tokens):
    client = get_openai_client()

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
        print(json.loads(result))

        return json.loads(result)

    except OpenAIError as e:
        if e.http_status == 401:
            print(f"Authentication error: {str(e)}")
            raise HTTPException(status_code=401, detail=f"Invalid or missing API Key: {str(e)}")
        else:
            print(f"Error with OpenAI API: {str(e)}")
            raise HTTPException(status_code=500, detail=f"Error with OpenAI API: {str(e)}")
    
def job_description_sections(job_description):
    client = get_openai_client()
    
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
        print(json.loads(result))

        return json.loads(result)

    except OpenAIError as e:
        if e.http_status == 401:
            print(f"Authentication error: {str(e)}")
            raise HTTPException(status_code=401, detail=f"Invalid or missing API Key: {str(e)}")
        else:
            print(f"Error with OpenAI API: {str(e)}")
            raise HTTPException(status_code=500, detail=f"Error with OpenAI API: {str(e)}")