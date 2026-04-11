# services/serpapi.py

from serpapi import GoogleSearch
import os
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("SERPAPI_KEY")

async def fetch_serpapi(query: str, k: int = 5):
    params = {
        "q": query,
        "api_key": API_KEY,
        "engine": "google"
    }

    search = GoogleSearch(params)
    results = search.get_dict()

    output = []

    for item in results.get("organic_results", [])[:k]:
        output.append({
            "url": item.get("link"),
            "title": item.get("title"),
            "source": "google"
        })

    return output