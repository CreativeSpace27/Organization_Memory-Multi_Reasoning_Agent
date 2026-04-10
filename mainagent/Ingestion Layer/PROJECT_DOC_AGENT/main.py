# main.py
import sys
import os
from core.pdf_parser import extract_text as parse_pdf
from core.docx_parser import extract_text as parse_docx # Agar alag function hai toh
from utils.cleaner import clean_document_text
import requests

BACKEND_URL = "http://127.0.0.1:8001/process-doc"
file_path = r"W:\Architecture_Decision_v1.pdf"


def run_agent(file_path):
    if not os.path.exists(file_path):
        print(f"❌ File nahi mili: {file_path}")
        return

    ext = os.path.splitext(file_path)[-1].lower()
    print(f"🕵️ Agent: Processing {ext} file...")


    # 1. Parse
    if ext == ".pdf":
        raw_text = parse_pdf(file_path)
    elif ext == ".docx":
        # Yahan apne docx_parser ka function call karein
        from core.docx_parser import extract_docx
        raw_text = extract_docx(file_path)
    else:
        print("🚫 Unsupported format")
        return

    # 2. Clean
    print("🧹 Agent: Cleaning text...")
    cleaned_text = clean_document_text(raw_text)

    # 3. Send to Backend
    payload = {
        "filename": os.path.basename(file_path),
        "content": cleaned_text,
        "file_type": ext
    }

    try:
        response = requests.post(BACKEND_URL, json=payload)
        if response.status_code == 200:
            print("✅ Agent: Data successfully synced to Organizational Memory!")
        else:
            print(f"⚠️ Backend Error: {response.status_code}")
    except Exception as e:
        print(f"🚨 Connection failed: {e}")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python main.py <file_path>")
    else:
        run_agent(sys.argv[1])