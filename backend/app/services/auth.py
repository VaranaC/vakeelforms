from passlib.hash import bcrypt
import jwt
from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/login")

# Fake DB (for MVP only)
fake_users = {}

SECRET = "vakeelforms_secret"  # TODO: move to env

def register_user(username: str, password: str):
    if username in fake_users:
        raise HTTPException(status_code=400, detail="User already exists")
    hashed = bcrypt.hash(password)
    fake_users[username] = hashed
    return {"msg": "User registered successfully"}

def authenticate_user(username: str, password: str):
    if username not in fake_users or not bcrypt.verify(password, fake_users[username]):
        return None
    token = jwt.encode({"sub": username}, SECRET, algorithm="HS256")
    return token

def get_current_user(token: str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(token, SECRET, algorithms=["HS256"])
        return payload["sub"]
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token expired")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401, detail="Invalid token")

