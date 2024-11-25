from fastapi import FastAPI, HTTPException, File, UploadFile, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import BaseModel
import bcrypt
import jwt
import datetime
import pdfplumber
import io

app = FastAPI()

origins = ["http://localhost:3000"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

JWT_SECRET = "your_jwt_secret"
JWT_ALGORITHM = "HS256"
JWT_EXPIRATION_MINUTES = 30

users = []

class UserCredentials(BaseModel):
    email: str
    password: str
    username: str = None

class TextSubmission(BaseModel):
    text: str

def create_jwt_token(data: dict):
    expiration = datetime.datetime.utcnow() + datetime.timedelta(minutes=JWT_EXPIRATION_MINUTES)
    data.update({"exp": expiration})
    return jwt.encode(data, JWT_SECRET, algorithm=JWT_ALGORITHM)

def verify_jwt_token(token: str):
    try:
        return jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALGORITHM])
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token expired")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401, detail="Invalid token")

def extract_text_from_pdf_in_memory(file_content: bytes) -> str:
    with pdfplumber.open(io.BytesIO(file_content)) as pdf:
        text = ""
        for page in pdf.pages:
            text += page.extract_text() + "\n"
    return text

@app.get("/")
def read_root():
    return {"message": "Welcome to the API"}

@app.get("/api")
def read_api():
    return {"message": "API is live"}

@app.post("/api/register")
async def register(request: Request):
    json_payload = await request.json()
    email = json_payload.get("email")
    for user in users:
        if user['email'] == email:
            raise HTTPException(status_code=400, detail="Email already registered")
    password = json_payload.get("password")
    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), salt)
    new_user = {
        "email": email,
        "password": hashed_password,
        "username": json_payload.get("username", email.split("@")[0]),
    }
    users.append(new_user)
    return {"message": "User registered successfully"}

@app.post("/api/login")
async def login(request: Request):
    json_payload = await request.json()
    email = json_payload.get("email")
    password = json_payload.get("password")
    for user in users:
        if user['email'] == email:
            if bcrypt.checkpw(password.encode('utf-8'), user['password']):
                token = create_jwt_token({"sub": user["username"]})
                return {"message": "Login successful", "token": token}
            else:
                raise HTTPException(status_code=401, detail="Invalid password")
    raise HTTPException(status_code=404, detail="User not found")

@app.get("/dashboard")
async def dashboard(token: str):
    payload = verify_jwt_token(token)
    return {"message": f"Welcome to the dashboard, {payload['sub']}"}

@app.post("/upload/resume")
async def upload_resume(file: UploadFile = File(...)):
    if file.content_type != "application/pdf":
        raise HTTPException(status_code=400, detail="Invalid file type. Only PDF files are accepted.")
    try:
        file_content = await file.read()
        extracted_text = extract_text_from_pdf_in_memory(file_content)
        return {"message": "Resume processed successfully", "extracted_text": extracted_text[:500]}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An error occurred: {str(e)}")

@app.post("/submit/text")
async def submit_text(submission: TextSubmission):
    if not submission.text.strip():
        raise HTTPException(status_code=400, detail="Text cannot be empty")
    if len(submission.text) < 50:
        raise HTTPException(status_code=400, detail="Text is too short")
    return {"message": "Text submitted successfully", "character_count": len(submission.text)}
