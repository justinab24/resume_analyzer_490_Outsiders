from fastapi import HTTPException
from dotenv import load_dotenv
from datetime import datetime, timedelta
import bcrypt
import jwt
import os

users = []

load_dotenv(dotenv_path="./backend/.env")
SECRET_KEY = os.getenv("JWT_SECRET_KEY")

def register_user(email, password, username):
    for user in users:
        if user['email'] == email:
            raise HTTPException(status_code=400, detail="Email already registered, please sign in")
    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), salt)

    newUser = {
        "email": email,
        "password": hashed_password,
        "username": username,
    }
    print("we received this username in the backend, ", username)
    users.append(newUser)

    token = jwt_generator(username)

    print(token)

    return {"message": "User registered successfully", "token": token}

def login_user(email, password):
    for user in users:
        if user['email'] == email:
            if bcrypt.checkpw(password.encode('utf-8'), user['password']):
                token = jwt_generator(user['username'])
                return {"message": "Login successful", "token": token}
            else:
                raise HTTPException(status_code=401, detail="Invalid password")
    raise HTTPException(status_code=404, detail="User not found")

def jwt_generator(username):
    expiration = datetime.now() + timedelta(hours=3)
    print(username)
    token = jwt.encode(
        {"sub": username, "exp": expiration},
        SECRET_KEY,
        algorithm="HS256",
    )
    return token
