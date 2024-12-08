from fastapi import FastAPI, File, Request, UploadFile, Form, HTTPException
from starlette.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from datetime import datetime, timedelta
from dotenv import load_dotenv
import httpx
import bcrypt
import jwt
import pdfplumber
import os
import os
import io
import docx
import time

#python3 -m uvicorn app:app --reload to run the api
#http://127.0.0.1:8000/docs for easy testing of the api - use try it out button

load_dotenv(dotenv_path="./backend/.env")
SECRET_KEY = os.getenv("JWT_SECRET_KEY")
HF_API_KEY = os.getenv("HF_API_KEY")

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

users = []

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
    for user in users:
        if user['email'] == email:
            raise HTTPException(status_code=400, detail="Email already registered, please sign in")
    password = json_payload.get("password")
    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), salt)

    newUser = {
        "email": email,
        "password": hashed_password,
        "username": json_payload.get("username"),
        "username": json_payload.get("username"),
    }

    users.append(newUser)

    return {"message": "User registered successfully"}

def jwt_generator(username):
    expiration = datetime.now() + timedelta(hours=3)
    print(username)
    token = jwt.encode(
        {"sub": username, "exp": expiration},
        SECRET_KEY,
        algorithm="HS256",
    )
    return token


def jwt_generator(username):
    expiration = datetime.now() + timedelta(hours=3)
    print(username)
    token = jwt.encode(
        {"sub": username, "exp": expiration},
        SECRET_KEY,
        algorithm="HS256",
    )
    return token


@app.post("/api/login")
async def login(request: Request):
    json_payload = await request.json()
    print(users)
    email = json_payload.get("email")
    password = json_payload.get("password")
    for user in users:
        if user['email'] == email:
            if bcrypt.checkpw(password.encode('utf-8'), user['password']):
                token = jwt_generator(user['username'])
                return {"message": "Login successful", "token": token}
            else:
                raise HTTPException(status_code=401, detail="Invalid password")
    raise HTTPException(status_code=404, detail="User not found")

@app.post("/api/resume-upload")
async def resumeUpload(file: UploadFile = File(...)):
    print("did we hit this endpoint")
    # Check if the uploaded file is a PDF
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
    """
    Endpoint to submit resume text directly.
    Validates that the text is not empty and meets a minimum length requirement.
    """
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


def extract_text_from_pdf_in_memory(file_content: bytes) -> str:
    """
    Extract text from a PDF file stored in memory.

    Args:
        file_content (bytes): The binary content of the PDF file.

    Returns:
        str: Extracted text from the PDF file.
    """
    with pdfplumber.open(io.BytesIO(file_content)) as pdf:
        text = ""
        for page in pdf.pages:
            text += page.extract_text() + "\n"
    return text

def extract_text_from_docx_in_memory(file_content: bytes) -> str:
    """
    Extract text from a DOCX file stored in memory.

    Args:
        file_content (bytes): The binary content of the DOCX file.

    Returns:
        str: Extracted text from the DOCX file.
    """
    doc = docx.Document(io.BytesIO(file_content))
    text = ""
    for paragraph in doc.paragraphs:
        text += paragraph.text + "\n"
    return text

@app.post("/api/analyze")
async def analyze(request: Request):
    print("analyze endpoint has been hit")
    json_payload = await request.json()
    resume_text = json_payload.get("resume_text")
    job_description = json_payload.get("job_description")
    print("We got the following arguments from the request")
    print(resume_text)
    print(job_description)
    
    fitscore_url = "https://api-inference.huggingface.co/models/sentence-transformers/all-MiniLM-L6-v2"
    skill_ner_url = "https://api-inference.huggingface.co/models/nucha/nucha_skillner_bert"
    headers = {"Authorization": f"Bearer {HF_API_KEY}"}

    fitscore_data = {
        "inputs": {
            "source_sentence": resume_text,
            "sentences": [job_description]
        }
    }

    feedback_data = {
        "inputs": job_description
    }

    missing_skills = []
    matched_keywords = []

    async with httpx.AsyncClient() as client:
        # Fetch similarity score
        fitscore_response = await client.post(fitscore_url, headers=headers, json=fitscore_data)
        if fitscore_response.status_code != 200:
            fitscore_error = fitscore_response.json()
            print(f"Similarity API Error: {fitscore_error}")
            raise HTTPException(status_code=fitscore_response.status_code, detail=fitscore_error)
        fitscore_result = fitscore_response.json()
        fit_score = fitscore_result[0]

        retries = 5
        for attempt in range(retries):
            skill_response = await client.post(skill_ner_url, headers=headers, json=feedback_data)
            if skill_response.status_code == 200:
                # Extracting skills from the response
                skill_result = skill_response.json()
                print("we got this skill response")
                print(skill_result)
                extracted_skills = [skill['word'] for skill in skill_result if skill['entity_group'] == 'B-SKILL']

                # Match extracted skills with the resume and job description
                for skill in extracted_skills:
                    if skill.lower() in resume_text.lower():
                        matched_keywords.append(skill)

                # Find missing skills
                missing_skills = [
                    skill.strip()
                    for skill in extracted_skills
                    if skill.lower() not in resume_text.lower()
                ]
                
                # Generate feedback based on missing skills
                feedback_raw = [f"Consider adding skills like {skill}." for skill in missing_skills]
                if not feedback_raw:
                    feedback_raw.append("Your resume matches the job description well.")
                break
            else:
                # If the model is still loading, retry after a delay
                print(f"Model loading, retrying in {2**attempt} seconds...")
                time.sleep(2**attempt)  # Exponential backoff

        if not feedback_raw:
            raise HTTPException(status_code=503, detail="Model is taking too long to load or respond.")

    # Prepare final response
    response = {
        "similarity_score": round(fit_score * 100, 2),  # Convert similarity to percentage
        "keywords_matched": matched_keywords,
        "feedback_raw": feedback_raw
    }

    print("endpoint response")
    print(response)
    # Response
    return response