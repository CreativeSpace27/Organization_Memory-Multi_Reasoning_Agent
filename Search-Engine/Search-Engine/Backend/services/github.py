import httpx
from config import GITHUB_API_BASE, GITHUB_TOKEN

headers = {
    "Authorization": f"token {GITHUB_TOKEN}"
}

# services/github.py

import httpx

async def fetch_github(query: str, k: int = 5):
    url = "https://api.github.com/search/repositories"
    params = {"q": query, "per_page": k}

    async with httpx.AsyncClient() as client:
        res = await client.get(url, params=params)
        data = res.json()

    results = []
    for item in data.get("items", []):
        results.append({
            "url": item.get("html_url"),
            "title": item.get("full_name"),
            "source": "github"
        })

    return results
    async with httpx.AsyncClient() as client:
        params = {
            "q": query,
            "sort": "comments",
            "order": "desc"
        }

        res = await client.get(GITHUB_API_BASE, params=params, headers=headers)
        data = res.json()

        results = []
        for item in data.get("items", []):
            if item.get("comments", 0) >= 5:
                results.append({
                    "url": item["html_url"],
                    "score": item["comments"],
                    "source": "github"
                })

        return results