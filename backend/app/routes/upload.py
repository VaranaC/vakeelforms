from fastapi import APIRouter, UploadFile, File, Depends
from app.services.ocr import extract_text
from app.services.legal_ai import get_legal_explanation
from app.services.auth import get_current_user

router = APIRouter()

@router.post("/")
async def upload_and_explain(file: UploadFile = File(...), user: str = Depends(get_current_user)):
    print("✅ Upload by user:", user)
    extracted_text = await extract_text(file)
    try:
        explanation = get_legal_explanation(extracted_text)  # ⬅️ FIXED (removed await)
    except Exception as e:
        return {"error": f"🚨 Exception during upload: {str(e)}"}

    return {
        "extracted_text": extracted_text,
        "explanation": explanation
    }
