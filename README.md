# ⚖️ VakeelForms.ai – India’s Legal Document Explainer & Drafting Assistant

VakeelForms is a cutting-edge AI-powered legal assistant that helps Indian users understand, classify, and auto-generate legal documents. Just upload a legal PDF or take a photo of a paper document — VakeelForms does the rest.

> Built for law students, professionals, and citizens seeking clarity, compliance, and action.

---

## Features

- 📄 Upload legal PDFs or capture documents with your phone camera
- 🧾 Automatically extract legal text using OCR (Tesseract + PDF parser)
- ⚖️ Get an AI-generated legal explanation of your document
- ✍️ Coming Soon: Draft legal notices, complaints, affidavits based on the document
- 🔐 JWT-based authentication and token storage
- 📱 Mobile-first UI built with React Native + Expo

---

## 🛠️ Tech Stack

| Layer           | Tech Used                            |
|------------------|---------------------------------------|
| Frontend         | React Native (Expo SDK 53)            |
| Backend          | FastAPI + Uvicorn                    |
| Auth             | JWT via OAuth2PasswordBearer         |
| OCR              | pytesseract, pdf2image, poppler      |
| AI Explanation   | HuggingFace (temp) → Local model soon|
| Drafting (Planned)| python-docx, PDF export, legal templates |
| Hosting (Planned)| Render / EC2 / Expo Build            |

---

## Setup Instructions

### ✅ Backend Setup

```bash
cd backend
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
