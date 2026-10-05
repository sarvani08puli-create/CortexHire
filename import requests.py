import requests
import os
import json
from dotenv import load_dotenv
from datetime import datetime,timezone
load_dotenv()
API_KEY = os.getenv("ADZUNA_APP_KEY")
api_id = os.getenv("ADZUNA_APP_ID")
try:

    
    response = requests.get(
        "https://api.adzuna.com/v1/api/jobs/gb/search/1",
        params={ "app_key": API_KEY, 
                "app_id": api_id,
                "results_per_page": 5, 
                "what": "data engineer" },
                timeout=10)
    response.raise_for_status()
    val= response.status_code
    
except requests.exceptions.RequestException as e:    
    print(f"Error occurred while fetching job data: {e}")
    data = None
except requests.exceptions.JSONDecodeError as e:
    print(f"Error decoding JSON response: {e}")
    data = None
except requests.exceptions.Timeout as e:
    print(f"Request timed out: {e}")
    data = None
else:
    if val  ==200:
        data = response.json()  
        with open(f"datajobs_{datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}.json", "w", encoding="utf-8") as file:
            json.dump(data, file, ensure_ascii=False, indent=4)
            for job in data["results"]:
                print(f"Job Title: {job['title']}")
                print(f"Company: {job['company']['display_name']}")
                print(f"Location: {job['location']['display_name']}")
                print(f"Description: {job['description'][:200]}...")
    else:
        print(f"Failed to fetch job data. Status code: {val}")
                    

