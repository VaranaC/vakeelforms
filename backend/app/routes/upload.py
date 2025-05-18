from fastapi import APIRouter, UploadFile, File, Depends
from app.services.ocr import extract_text
from app.services.legal_ai import get_legal_explanation
from app.services.auth import get_current_user

router = APIRouter()

@router.post("/")
async def upload_and_explain(
    file: UploadFile = File(...),
    user: str = Depends(get_current_user)  # user is just a string
):
    try:
        print("✅ Upload by user:", user)
        extracted_text = await extract_text(file)
        explanation = await get_legal_explanation(extracted_text)
        return {
            "extracted_text": extracted_text,
            "explanation": explanation
        }
    except Exception as e:
        print("🚨 Exception during upload:", str(e))
        return {"error": str(e)}
