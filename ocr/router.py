from fastapi import APIRouter, UploadFile, File
from ocr.services.sarvam_ai import convert_ocr

router = APIRouter(prefix="/ocr", tags=["ocr"])


@router.post("/")
def run_ocr(file: UploadFile = File(...), language: str = "en-IN"):
    input_path = f"/tmp/{file.filename}"
    with open(input_path, "wb") as f:
        f.write(file.file.read())
    markdown = convert_ocr(input_path, language)
    return {"markdown": markdown}
