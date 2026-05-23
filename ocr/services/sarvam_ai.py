import os
import logging
import time
import tempfile, zipfile
import requests
import json
from sarvamai import SarvamAI
from dotenv import load_dotenv


load_dotenv()
logger = logging.getLogger(__name__)
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(name)s | %(levelname)s | %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)

def convert_ocr(file_path: str, language: str = "en-IN"):
    api_key = os.getenv("SARVAM_API_KEY")
    if not api_key:
        raise ValueError("Missing SARVAM_API_KEY")

    try:
        client = SarvamAI(api_subscription_key=api_key)
        start = time.time()

        job = client.document_intelligence.create_job(language=language, output_format="md")
        job.upload_file(file_path)
        job.start()
        status = job.wait_until_complete()

        logger.info("job=%s state=%s elapsed=%.1fs", job.job_id, status.job_state, time.time() - start)
    except Exception as e:
        logger.error(f"OCR job failed {str(e)}")
        raise
    
    tmp_path=None
    try:

        with tempfile.NamedTemporaryFile(
            suffix=".zip", delete=False, prefix="ocr_markdown_" 
        ) as tmp:
            tmp_path=tmp.name
            logger.info(f'tmp_pathname {tmp_path}')


        job.download_output(output_path=tmp_path)

        with zipfile.ZipFile(tmp_path) as zf:
            logger.info(f'zipped files are {zf.namelist()}')
            for file_name in zf.namelist():
                logger.info(f'file name {file_name} having size {zf.getinfo(file_name).file_size} bytes')
            md_contents=zf.read("document.md").decode("utf-8")

            page_names=sorted(
                page_name for page_name in zf.namelist()
                if page_name.startswith("metadata/") and page_name.endswith(".json")
            )

            page_contents=[json.loads(zf.read(page_name)) for page_name in page_names]

            return {
                "page_details":{
                    # "md_content":md_contents,
                    "json_contents":page_contents
                }
               
            }
    except Exception as e:
        logger.error(f"Download/Extract failed : {str(e)}")
        raise
    finally:
        if tmp_path and os.path.exists(tmp_path):
            os.remove(tmp_path)




