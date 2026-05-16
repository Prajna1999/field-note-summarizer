import os
from dotenv import load_dotenv
import logging
import time
from sarvamai import SarvamAI
load_dotenv()
logger = logging.getLogger(__name__)


if __name__=="__main__":
    
    api_key=os.getenv("SARVAM_API_KEY")
    client = SarvamAI(
        api_subscription_key=api_key
    )

    start_time=time.time()
    # Create a document intelligence job
    job = client.document_intelligence.create_job(
        language="en-IN",
        output_format="md"
    )
    print(f"Job created: {job.job_id}")

    # Upload document
    job.upload_file("/Users/prajna/Downloads/Adobe Scan 15 Apr 2026_GADRambhila.pdf")
    print("File uploaded")

    # Start processing
    job.start()
    print("Job started")

    # Wait for completion
    status = job.wait_until_complete()
    print(f"Job completed with state: {status.job_state}")

    # Get processing metrics
    metrics = job.get_page_metrics()
    print(f"Page metrics: {metrics}")

    # Download output (ZIP file containing the processed document)
    job.download_output("/Users/prajna/Desktop/personal/projects/software/field-note-summarizer/files/output/working_report_april.zip")
    end_time=time.time()

    print(f"Output saved to ./output.zip; time taken {end_time-start_time}")



