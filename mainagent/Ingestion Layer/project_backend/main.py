import sys
import os
from fastapi import FastAPI
from pydantic import BaseModel
from typing import List

# --- MULTI-AGENT PATH SETUP ---
# PROJECT folder ko path mein add kar rahe hain (Future integration ke liye)
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_PATH = os.path.abspath(os.path.join(BASE_DIR, "..", "PROJECT"))
if PROJECT_PATH not in sys.path:
    sys.path.append(PROJECT_PATH)

app = FastAPI()

# --- CENTRALIZED MEMORY PATH ---
# Yeh file PROJECT/data/meeting.txt mein save hogi
MEETING_FILE = os.path.join(PROJECT_PATH, "data", "meeting.txt")

# --- DATA MODELS ---

class SlackMessage(BaseModel):
    user: str
    text: str
    ts: str = "0.0"

class SlackExport(BaseModel):
    messages: List[SlackMessage]

class EmailData(BaseModel):
    subject: str
    body: str
    from_email: str

class DocumentData(BaseModel):
    filename: str
    content: str
    file_type: str

# --- UTILITY FUNCTIONS ---

def sync_to_file(content: str):
    """Data ko meeting.txt mein save karta hai."""
    try:
        os.makedirs(os.path.dirname(MEETING_FILE), exist_ok=True)
        with open(MEETING_FILE, "a", encoding="utf-8") as f:
            f.write(content + "\n")
        print(f"📝 Memory Updated: {MEETING_FILE}")
    except Exception as e:
        print(f"❌ File Save Error: {e}")

# --- ENDPOINTS ---

@app.post("/process-slack")
async def ingest_slack(data: SlackExport):
    combined_text = "\n".join([f"{m.user}: {m.text}" for m in data.messages])
    sync_to_file(f"\n--- SLACK IMPORT ---\n{combined_text}\n--- END SLACK ---")
    return {"status": "success", "source": "slack"}

@app.post("/process-email")
async def ingest_email(data: EmailData):
    full_text = f"Subject: {data.subject}\nFrom: {data.from_email}\nContent: {data.body}"
    sync_to_file(f"\n--- EMAIL IMPORT ---\n{full_text}\n--- END EMAIL ---")
    return {"status": "success", "source": "email"}

@app.post("/process-doc")
async def ingest_doc(data: DocumentData):
    header = f"--- DOCUMENT IMPORT: {data.filename} ({data.file_type}) ---"
    full_text = f"\n{header}\n{data.content}\n--- END DOCUMENT ---"
    sync_to_file(full_text)
    return {"status": "success", "filename": data.filename}

# --- SERVER START ---



# 1. Naya Model add karein (aapke requested format ke hisab se)
class FinalDecision(BaseModel):
    decision: str
    reason: str
    alternatives: list
    impacts: list
    source: str

# 2. Naya Endpoint add karein


if __name__ == "__main__":
    import uvicorn
    print(f"📡 Multi-Agent Backend is LIVE!")
    print(f"📁 Target Memory: {MEETING_FILE}")
    uvicorn.run(app, host="0.0.0.0", port=8001)