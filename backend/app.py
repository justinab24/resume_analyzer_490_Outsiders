from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import BaseModel
import jwt
import datetime

app = FastAPI()

origins = ["http://localhost:3000"]  
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class UserCredentials(BaseModel):
    email: str
    password: str

users = {}

JWT_SECRET = "your_jwt_secret"
JWT_ALGORITHM = "HS256"
JWT_EXPIRATION_MINUTES = 30

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

@app.post("/register")
async def register(user: UserCredentials):
    if user.email in users:
        raise HTTPException(status_code=400, detail="Email already registered")
    
    users[user.email] = {"password": user.password}
    return {"message": "User registered successfully"}

@app.post("/login")
async def login(user: UserCredentials):
    if user.email not in users or users[user.email]["password"] != user.password:
        raise HTTPException(status_code=401, detail="Invalid email or password")
    
    token = create_jwt_token({"sub": user.email})
    return {"token": token}

@app.get("/dashboard")
async def dashboard(token: str):
    payload = verify_jwt_token(token)
    return {"message": f"Welcome to the dashboard, {payload['sub']}"}
