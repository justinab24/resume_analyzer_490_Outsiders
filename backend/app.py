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

@app.get("/")
def read_root():
    return {"Hello": "World"}

@app.get("/api")
def read_api():
    return {"Hello": "API"}

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


