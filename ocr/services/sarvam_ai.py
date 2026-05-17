import os
from dotenv import load_dotenv
import logging
import time
from sarvamai import SarvamAI

load_dotenv()
logger = logging.getLogger(__name__)


def run_batch_ocr(input_path: str, output_path: str, language: str = "en-IN") -> None:
    client = SarvamAI(api_subscription_key=os.getenv("SARVAM_API_KEY"))
    start = time.time()

    job = client.document_intelligence.create_job(language=language, output_format="md")
    job.upload_file(input_path)
    job.start()
    status = job.wait_until_complete()
    job.download_output(output_path)

    logger.info("job=%s state=%s elapsed=%.1fs", job.job_id, status.job_state, time.time() - start)


if __name__ == "__main__":
    run_batch_ocr(
        input_path="/Users/prajna/Downloads/Adobe Scan 15 Apr 2026_GADRambhila.pdf",
        output_path="/Users/prajna/Desktop/personal/projects/software/field-note-summarizer/files/output/working_report_april_3.zip",
    )



