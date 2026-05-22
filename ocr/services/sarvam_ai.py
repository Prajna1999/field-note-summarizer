import os
import requests
from dotenv import load_dotenv
import logging
import time
from sarvamai import SarvamAI

load_dotenv()
logger = logging.getLogger(__name__)


def convert_ocr(file_path: str, language: str = "en-IN") -> str:
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

        download_response = client.document_intelligence.get_download_links(job_id=job.job_id)
        details = list(download_response.download_urls.values())[0]
        return requests.get(details.file_url).text
    except Exception as e:
        logger.error("OCR job failed: %s", e)
        raise




