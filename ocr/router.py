import os
import uuid
import filetype
from fastapi import APIRouter, UploadFile, File, HTTPException, status
from ocr.services.sarvam_ai import convert_ocr
from common.utils import read_capped

router = APIRouter(prefix="/ocr", tags=["ocr"])

ALLOWED_CONTENT_TYPES = {"application/pdf", "image/png", "image/jpeg"}
EXT_BY_TYPE = {"application/pdf": ".pdf", "image/png": ".png", "image/jpeg": ".jpg"}
MAX_BYTES= 10 * 1024 * 1024 #10 MB

@router.post("/")
def run_ocr(file: UploadFile = File(...), language: str = "en-IN"):
    if file.content_type not in ALLOWED_CONTENT_TYPES:
        raise HTTPException(status.HTTP_415_UNSUPPORTED_MEDIA_TYPE, f"Unsupported type: {file.content_type}")
    
    try:
        data=read_capped(file, MAX_BYTES)
    except ValueError as e:
        raise HTTPException(status.HTTP_413_CONTENT_TOO_LARGE, str(e))
    
    # guess the filetype from the first 8 bytes
    file_content_signature=filetype.guess(data)

    if file_content_signature is None or file_content_signature.mime not in ALLOWED_CONTENT_TYPES:
        raise HTTPException(status.HTTP_415_UNSUPPORTED_MEDIA_TYPE, f"File content is not a valid PDF, PNG, or JPEG")
    

    input_path =  f"/tmp/{uuid.uuid4().hex}{EXT_BY_TYPE[file_content_signature.mime]}"

    try:

        with open(input_path, "wb") as f:
            f.write(data)
        converted_files = convert_ocr(input_path, language)
        return converted_files
    finally:
        if os.path.exists(input_path):
            os.remove(input_path)
    
    
