import requests
from datetime import datetime
from pathlib import Path
import json
from google.cloud import storage
from dotenv import load_dotenv
import os

load_dotenv()

BASE_DIR = Path(__file__).resolve().parent.parent

today = datetime.today().strftime("%Y_%m_%d")

url = "https://remoteok.com/api"

project_id = os.getenv("GCP_PROJECT_ID")

bronze = os.getenv("GCS_BUCKET_BRONZE")

blob_path = f"remoteok/dt={today}/remoteok_{today}.json"

raw_file_path = f"{BASE_DIR}/data/raw/{today}_jobs.json"

try:
    response = requests.get(
        url,
        headers = {
            "User-Agent": "elt_pipeline"
        }
    )
    response.raise_for_status()
    data = response.json()
    with open(raw_file_path, "w") as f:
        json.dump(data, f, indent=4)
        
    client = storage.Client(project=project_id)
    bronze_bucket = client.bucket(bronze)
    bronze_blob = bronze_bucket.blob(blob_path)
    bronze_blob.upload_from_filename(raw_file_path)

    print(f"Uploaded to {blob_path}.")

except requests.exceptions.RequestException as error:
    print(f"Request failed: {error}")

except Exception as error:
    print(f"Unexpected error: {error}")