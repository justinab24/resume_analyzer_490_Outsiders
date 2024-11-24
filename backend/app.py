from fastapi import FastAPI, File, UploadFile, Form, HTTPException
from fastapi.responses import JSONResponse
from pydantic import BaseModel
import pdfplumber
import os
import io

#python3 -m uvicorn app:app --reload to run the api
#http://127.0.0.1:8000/docs for easy testing of the api - use try it out button

class TextSubmission(BaseModel):
    text: str

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

app = FastAPI()

users = []

@app.get("/")
def read_root():
    return {"Hello": "World"}

@app.get("/api")
def read_api():
    return {"Hello": "API"}

@app.post("/api/register")
async def register(request: Request):
    json_payload = await request.json()
    email = json_payload.get("email")
    for user in users:
        if user['email'] == email:
            return {"message": "Email already registered, please sign in"}
    password = json_payload.get("password")
    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), salt)
    newUser = {
        "email": email,
        "password": hashed_password,
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


@app.post("/api/login")
async def login(request: Request):
    json_payload = await request.json()
    email = json_payload.get("email")
    password = json_payload.get("password")
    for user in users:
        if user['email'] == email:
            if bcrypt.checkpw(password.encode('utf-8'), user['password']):
                token = jwt_generator(user['username'])
                return {"message": "Login successful", "token": token}
            else:
                return {"message": "Invalid password"}
    return {"message": "User not found"}

@app.post("/upload/resume")
async def upload_resume(file: UploadFile = File(...)):
    # Check if the uploaded file is a PDF
    if file.content_type != "application/pdf":
        raise HTTPException(status_code=400, detail="Invalid file type. Only PDF files are accepted.")

    try:
        # Read the uploaded file content into memory
        file_content = await file.read()

        # Extract text from the PDF stored in memory using pdfplumber
        extracted_text = extract_text_from_pdf_in_memory(file_content)

        return {
            "message": "Resume uploaded and processed successfully.",
            "extracted_text": extracted_text[:500]  # Limit response to 500 characters for brevity
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An error occurred: {str(e)}")


@app.post("/submit/text")
async def submit_text(submission: TextSubmission):
    """
    Endpoint to submit resume text directly.
    Validates that the text is not empty and meets a minimum length requirement.
    """
    if not submission.text.strip():
        raise HTTPException(
            status_code=400,
            detail="Text cannot be empty or only whitespace."
        )
    
    if len(submission.text) < 50:  # Example: Require at least 50 characters
        raise HTTPException(
            status_code=400,
            detail="Text is too short. Please provide at least 50 characters."
        )
    
    return JSONResponse(
        content={"message": "Text submitted successfully", "character_count": len(submission.text)}
    )


