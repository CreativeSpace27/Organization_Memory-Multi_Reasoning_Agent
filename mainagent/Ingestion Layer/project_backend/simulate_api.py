import requests

BASE_URL = "http://127.0.0.1:8001"

def send_data_to_ingestion():
    # 1. Slack Data (Added 'ts' to fix 422 error)
    slack_data = {
        "messages": [
            {"user": "Abhishek", "text": "We need to choose between Redis and Memcached.", "ts": "1712736000"},
            {"user": "Team", "text": "Redis is better for persistence.", "ts": "1712736005"},
            {"user": "Lead", "text": "Okay, let's use Redis.", "ts": "1712736010"}
        ]
    }
    r1 = requests.post(f"{BASE_URL}/process-slack", json=slack_data)
    print(f"📤 Slack push status: {r1.status_code}")

    # 2. Email Data
    email_data = {
        "subject": "Cloud Provider",
        "from_email": "cto@company.com",
        "body": "Final decision: Use AWS for all production workloads."
    }
    r2 = requests.post(f"{BASE_URL}/process-email", json=email_data)
    print(f"📤 Email push status: {r2.status_code}")

if __name__ == "__main__":
    send_data_to_ingestion()