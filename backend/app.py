from fastapi import FastAPI, File, Request, UploadFile, Form, HTTPException
from starlette.middleware.cors import CORSMiddleware
from utils.nlp_functions import nlp_analysis
from utils.calculate_fit_score import calculate_fit_score
from services.authentication import register_user, login_user, jwt_generator
from utils.parse_file_upload import extract_text_from_pdf_in_memory, extract_text_from_docx_in_memory
from fastapi.responses import JSONResponse
from utils.models import NLPInput, NLPOutput
from pydantic import BaseModel
from datetime import datetime, timedelta
import httpx
import bcrypt
import jwt
import pdfplumber
import json
import os
import io
import docx
import re
from openai import OpenAI
from collections import Counter
import time


#python3 -m uvicorn app:app --reload to run the api
#http://127.0.0.1:8000/docs for easy testing of the api - use try it out button

timeout = httpx.Timeout(30.0, connect=60.0)  # 30 seconds for read, 60 seconds for connection



class TextSubmission(BaseModel):
    text: str

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # Allow frontend's origin (React app)
    allow_credentials=True,
    allow_methods=["*"],  # Allow all HTTP methods (GET, POST, etc.)
    allow_headers=["*"],  # Allow all headers
)

@app.get("/")
def read_root():
    return {"Hello": "World"}

@app.get("/api")
def read_api():
    return {"Hello": "API"}

@app.get("/dashboard")
async def dashboard(token: str):
    return {"message": f"Welcome to the dashboard"}


@app.post("/api/register")
async def register(request: Request):
    json_payload = await request.json()
    email = json_payload.get("email")
    password = json_payload.get("password")
    username = json_payload.get("username")
    register_response = register_user(email, password, username)
    return register_response

@app.post("/api/login")
async def login(request: Request):
    json_payload = await request.json()
    email = json_payload.get("email")
    password = json_payload.get("password")
    response = login_user(email, password)
    return response

@app.post("/api/resume-upload")
async def resumeUpload(file: UploadFile = File(...)):
    if file.content_type not in ["application/pdf", "application/vnd.openxmlformats-officedocument.wordprocessingml.document"]:
        raise HTTPException(status_code=400, detail="Invalid file type. Only PDF and DOCX files are accepted.")

    try:
        # Read the uploaded file content into memory
        file_content = await file.read()

        # Extract text from the PDF or DOCX stored in memory
        if file.content_type == "application/pdf":
            extracted_text = extract_text_from_pdf_in_memory(file_content)
        elif file.content_type == "application/vnd.openxmlformats-officedocument.wordprocessingml.document":
            extracted_text = extract_text_from_docx_in_memory(file_content)


        print(extracted_text)

        return {
            "message": "Resume uploaded and processed successfully.",
            "extracted_text": extracted_text[:5000]  # Limit response to 5000 characters for brevity
        }
    except Exception as e:
        print(f"An error occurred: {str(e)}");
        raise HTTPException(status_code=500, detail=f"An error occurred: {str(e)}")


@app.post("/api/job-description")
async def descriptionUpload(submission: TextSubmission):

    if not submission.text.strip():
        raise HTTPException(
            status_code=400,
            detail="Text cannot be empty or only whitespace."
        )
    
    if len(submission.text) > 5000:  # Example: Require at least 50 characters
        raise HTTPException(
            status_code=400,
            detail="Job description exceeds character limit. Please make sure input is less than 5000 characters."
        )
    
    return JSONResponse(
        content={"message": "Text submitted successfully", "character_count": len(submission.text)}
    )

@app.post("/api/fit-score")
async def calculate_fit_score_endpoint(request: Request):
    """
    Endpoint to calculate fit score based on resume and job description. Uses NLP analysis and keyword matching.
    """
    print("endpoint hit")
    json_payload = await request.json()
    resume_text = json_payload.get("resume_text")
    job_description = json_payload.get("job_description")
    if not resume_text.strip() or not job_description.strip():
        raise HTTPException(
            status_code=400,
            detail="Both resume text and job description must be provided."
        )
    print("justin we are getting this job description")
    print(job_description)
    try:
        nlp_input = NLPInput(resume_text=resume_text, job_description=job_description)
        nlp_output = NLPOutput(similarity_score=0.0, keywords_matched=[], feedback_raw=[])
        nlp_output = await analyze(nlp_input)
        similarity_score = nlp_output.similarity_score
        feedback = nlp_output.feedback_raw
        matched_skills = nlp_output.keywords_matched
        token_based_fitscores = calculate_fit_score(resume_text, job_description)
        weighted_token_score = token_based_fitscores["weighted_token_score"]
        unweighted_token_score = token_based_fitscores["unweighted_token_score"]
        matched_skills = token_based_fitscores["matched_keywords"]
        matched_skills_amount = len(matched_skills)
        missing_skills = token_based_fitscores["missing_keywords_total"]
        final_fit_score = ((weighted_token_score * 0.75) + (unweighted_token_score * 0.15) + (similarity_score * 0.1))

        if final_fit_score < 0:
            final_fit_score = 0

        response = {
            "similarity_score": {
            "total": round(final_fit_score, 2),
            "matched_total": matched_skills_amount,
            "missing_total": missing_skills,
            },
            "keywords_matched": matched_skills,
            "feedback_raw": feedback,
        }

        return response

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"An error occurred during fit score calculation: {str(e)}"
        )
    
@app.post("/api/analyze")
async def analyze(nlp_input: NLPInput):
    print("analyze endpoint has been hit")
    try:
        # Extract inputs from the request object
        resume_text = nlp_input.resume_text
        job_description = nlp_input.job_description
        nlp_input = NLPInput(resume_text=resume_text, job_description=job_description)
        # Perform NLP analysis
        nlp_output = await nlp_analysis(nlp_input)
        return nlp_output

    except ValueError as ve:
        # Handle specific NLP analysis errors
        raise HTTPException(
            status_code=422,  # Unprocessable Entity
            detail=f"Invalid data for NLP analysis: {str(ve)}"
        )
    except TimeoutError:
        # Handle potential timeouts during processing
        raise HTTPException(
            status_code=504,  # Gateway Timeout
            detail="NLP analysis took too long. Please try again later."
        )
    except Exception as e:
        # Generic error handling
        raise HTTPException(
            status_code=500,
            detail=f"An unexpected error occurred during analysis: {str(e)}"
        )
