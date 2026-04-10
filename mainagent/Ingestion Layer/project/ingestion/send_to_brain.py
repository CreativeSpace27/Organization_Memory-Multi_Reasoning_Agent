# ingestion/send_to_brain.py

import requests

API_URL = "http://localhost:8000/store-decision"

def send_to_brain(data):
    try:
        response = requests.post(API_URL, json=data)
        print("✅ Sent to brain:", response.status_code)
    except Exception as e:
        print("❌ Failed to send:", e)