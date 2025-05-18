from PIL import Image, UnidentifiedImageError
from pdf2image import convert_from_bytes
import pytesseract
import io
import os

async def extract_text(file):
    contents = await file.read()
    poppler_path = "C:/poppler/poppler-24.08.0/Library/bin"

    try:
        # Try as image
        image = Image.open(io.BytesIO(contents))
        return pytesseract.image_to_string(image)

    except UnidentifiedImageError:
        try:
            # Try as PDF
            pages = convert_from_bytes(contents, poppler_path=poppler_path)
            text = ""
            for page in pages:
                text += pytesseract.image_to_string(page) + "\n"
            return text
        except Exception as e:
            return f"❌ Could not process document: {str(e)}"
