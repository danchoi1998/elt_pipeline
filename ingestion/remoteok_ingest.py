import requests
from datetime import datetime
from pathlib import Path
import json

today = datetime.today().strftime("%Y_%m_%d")

BASE_DIR = Path(__file__).resolve().parent.parent

url = "https://remoteok.com/api"

try:
    response = requests.get(
        url,
        headers = {
        "User-Agent": "elt_pipeline"
        }
    )
    response.raise_for_status()
    data = response.json()
    with open(f"{BASE_DIR}/data/raw/{today}_jobs.json", "w") as f:
        json.dump(data, f)


except requests.exceptions.RequestException as error:
    print(f"Request failed: {error}")
