import os
from fastapi import FastAPI, UploadFile, File, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from pydantic import BaseModel
from jose import jwt, JWTError
from passlib.context import CryptContext
from dotenv import load_dotenv
from typing import Optional
import pytesseract
from PIL import Image
import io
import PyPDF2
import docx2txt
import tempfile
import requests

# Load environment variables from .env
load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), '.env'))
JWT_SECRET = os.getenv('JWT_SECRET', 'changeme')
ALGORITHM = 'HS256'
HF_TOKEN = os.getenv('HF_TOKEN', '')

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- Auth Models and Database ---
class User(BaseModel):
    username: str
    password: str

# Use in-memory users for demo/testing only
db_users = {}
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/login")


def get_password_hash(password):
    return pwd_context.hash(password)

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def create_access_token(data: dict):
    return jwt.encode(data, JWT_SECRET, algorithm=ALGORITHM)

def get_current_user(token: str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(token, JWT_SECRET, algorithms=[ALGORITHM])
        username = payload.get("sub")
        if username not in db_users:
            raise HTTPException(status_code=401, detail="Invalid credentials")
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    return username

# --- Auth Endpoints ---
@app.post('/api/v1/auth/register')
def register(user: User):
    if user.username in db_users:
        raise HTTPException(status_code=409, detail="Username already exists")
    db_users[user.username] = {
        "username": user.username,
        "hashed_password": get_password_hash(user.password)
    }
    return {"msg": "Registered!"}

@app.post('/api/v1/auth/login')
def login(form_data: OAuth2PasswordRequestForm = Depends()):
    user = db_users.get(form_data.username, None)
    if not user or not verify_password(form_data.password, user["hashed_password"]):
        raise HTTPException(status_code=401, detail="Incorrect username or password")
    token = create_access_token({"sub": form_data.username})
    return {"access_token": token, "token_type": "bearer"}

# --- File Handling & AI Endpoint ---
class UploadResponse(BaseModel):
    extracted_text: str
    explanation: str


def extract_text_from_file(file: UploadFile) -> str:
    # Detect file type
    filename = file.filename.lower()
    contents = file.file.read()
    with tempfile.NamedTemporaryFile(delete=False) as tmp:
        tmp.write(contents)
        tmpfile_path = tmp.name
    text = ""
    try:
        if filename.endswith('.pdf'):
            with open(tmpfile_path, 'rb') as fpdf:
                pdf = PyPDF2.PdfReader(fpdf)
                for page in pdf.pages:
                    text += page.extract_text() or ''
        elif filename.endswith('.docx'):
            text = docx2txt.process(tmpfile_path)
        elif filename.endswith(('.png', '.jpg', '.jpeg', '.bmp', '.tiff')):
            img = Image.open(tmpfile_path)
            text = pytesseract.image_to_string(img)
        else:
            # fallback plain text
            text = contents.decode(errors='ignore')
    finally:
        os.remove(tmpfile_path)
    return text.strip()

# --- AI Prompting ---
def get_legal_explanation(text: str) -> str:
    """
    Uses HuggingFace Inference API to summarize/explain legal docs in layman's terms.
    For advanced, plug in OpenAI API here instead.
    """
    if not text.strip():
        return "No text found in document."
    api_url = "https://api-inference.huggingface.co/models/google/flan-t5-large"
    headers = {"Authorization": f"Bearer {HF_TOKEN}"}
    payload = {
        "inputs": f"Summarize and explain this legal document in plain language: {text[:4000]}"
    }
    try:
        resp = requests.post(api_url, headers=headers, json=payload, timeout=60)
        if resp.status_code == 200:
            output = resp.json()
            if isinstance(output, list) and len(output) and "generated_text" in output[0]:
                return output[0]["generated_text"]
            elif isinstance(output, dict) and "generated_text" in output:
                return output["generated_text"]
            return str(output)
        else:
            return f"HuggingFace API error: {resp.status_code} {resp.text}"  
    except Exception as e:
        return f"[AI MODEL ERROR] {str(e)}"

@app.post('/api/v1/upload/', response_model=UploadResponse)
def upload_file(file: UploadFile = File(...), username: str = Depends(get_current_user)):
    text = extract_text_from_file(file)
    explanation = get_legal_explanation(text)
    return {"extracted_text": text, "explanation": explanation}

@app.get("/")
def root():
    return {"msg": "VakeelForms backend running!"}
