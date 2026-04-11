# services/docs.py

async def fetch_docs(query: str, k: int = 5):
    base = "https://developer.mozilla.org/en-US/search?q="
    return [{
        "url": f"{base}{query}",
        "title": f"MDN search: {query}",
        "source": "mdn"
    }]