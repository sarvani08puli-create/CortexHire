import json
from datetime import datetime, timezone
import logging

logging.basicConfig(
    level=logging.INFO,
    filename='cortexHire.log',
    filemode='a',
    format='%(asctime)s - %(levelname)s - %(message)s'
)

try:
    with open("job_data_1_2026-09-27_20.json", "r", encoding="utf-8") as f:
        data = json.load(f)

    jobs = data["results"]
    print("Number of jobs found: ", len(jobs))
    logging.info("Number of jobs found: %s", len(jobs))

    timenow = datetime.now(timezone.utc).strftime("%Y-%m-%d_%H-%M-%S")
    clean_jobs = []
    rejected_jobs = []
    filename = f"Cleaned_jobs_{timenow}.json"
    rejected_filename = f"rejected_jobs_{timenow}.json"

    for job in jobs:
        job_id = job.get("id")

        if job_id is None: 
            rejected_jobs.append({
                "reason": "Missing job id",
                "result": job
            })
            continue

        clean_job = {
            "job_id": job_id,
            "title": job.get("title"),
            "company": job.get("company", {}).get("display_name"),
            "location": job.get("location", {}).get("display_name")
        }
        clean_jobs.append(clean_job)

    print("The jobs are in list now", clean_jobs)
    logging.info("The jobs are in list now: %s", clean_jobs)

    with open(filename, 'w', encoding='utf-8') as file:
        json.dump(clean_jobs, file, indent=2)

    with open(rejected_filename, 'w', encoding='utf-8') as file:
        json.dump(rejected_jobs, file, indent=2)

except FileNotFoundError:
    logging.error("Error: Input file not found.")
except json.JSONDecodeError:
    logging.error("Error: The JSON file is invalid or unreadable.")
except OSError:
    logging.error("Error: File could not be opened or written.")
logging.info(
    "Transformation completed: input=%d, accepted=%d, rejected=%d",
    len(jobs),
    len(clean_jobs),
    len(rejected_jobs),
)