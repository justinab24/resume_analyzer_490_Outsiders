from fastapi import FastAPI
from fastapi import Request
import bcrypt
import jwt
from datetime import datetime, timedelta
from dotenv import load_dotenv
import os

load_dotenv(dotenv_path="./backend/.env")
SECRET_KEY = os.getenv("JWT_SECRET_KEY")


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


