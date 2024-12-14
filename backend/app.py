from fastapi import FastAPI, File, Request, UploadFile, Form, HTTPException
from starlette.middleware.cors import CORSMiddleware
from services.skill_extraction import nlp_analyzer
from services.authentication import register_user, login_user, jwt_generator
from utils.parsing import extract_text_from_pdf_in_memory, extract_text_from_docx_in_memory
from fastapi.responses import JSONResponse
from services.models import NLPInput, NLPOutput
from pydantic import BaseModel
from datetime import datetime, timedelta
import httpx
import bcrypt
import jwt
import pdfplumber
import os
import io
import docx
import re
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
    register_user(email, password, username)
    return {"message": "User registered successfully"}

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
            detail="Job description exceeds character limit."
        )
    
    return JSONResponse(
        content={"message": "Text submitted successfully", "character_count": len(submission.text)}
    )

def calculate_fit_score(resume_text, job_description):
    # Tokenize and normalize text
    def tokenize(text):
        return re.findall(r'\b\w+\b', text.lower())

    resume_tokens = tokenize(resume_text)
    job_tokens = tokenize(job_description)

    # Count matching keywords
    resume_counter = Counter(resume_tokens)
    job_counter = Counter(job_tokens)

    matches = sum((resume_counter & job_counter).values())
    total_keywords = len(job_tokens)

    return int((matches / total_keywords) * 100) if total_keywords > 0 else 0

@app.post("/api/calculate-fit-score")
async def calculate_fit_score_endpoint(
    resume_text: str = Form(...), 
    job_description: str = Form(...)
):
    
    if not resume_text.strip() or not job_description.strip():
        raise HTTPException(
            status_code=400, 
            detail="Both resume text and job description must be provided."
        )

    try:
        fit_score = calculate_fit_score(resume_text, job_description)
        return JSONResponse(
            content={
                "message": "Fit score calculated successfully.",
                "fit_score": fit_score
            }
        )
    except Exception as e:
        raise HTTPException(
            status_code=500, 
            detail=f"An error occurred during fit score calculation: {str(e)}"
        )
    
@app.post("/api/analyze", response_model=NLPOutput)
async def analyze(nlp_input: NLPInput):
    try:
        print("analyze endpoint has been hit")
        # Call the nlp_analyzer function
        nlp_output = await nlp_analyzer(nlp_input)
        return nlp_output  # FastAPI will serialize the output
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An error occurred: {str(e)}")
