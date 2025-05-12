from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routes import upload, auth

app = FastAPI()

# Enable frontend access
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(upload.router, prefix="/api/v1/upload")
app.include_router(auth.router, prefix="/api/v1/auth")

