
from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from app.services.auth import register_user, authenticate_user, get_current_user
from fastapi.security import OAuth2PasswordRequestForm

router = APIRouter()

class UserRegister(BaseModel):
    username: str
    password: str

@router.post("/register")
def register(user: UserRegister):
    return register_user(user.username, user.password)

@router.post("/login")
def login(form_data: OAuth2PasswordRequestForm = Depends()):
    token = authenticate_user(form_data.username, form_data.password)
    if not token:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    return {"access_token": token, "token_type": "bearer"}

@router.get("/profile")
def profile(current_user: str = Depends(get_current_user)):
    return {"username": current_user}
