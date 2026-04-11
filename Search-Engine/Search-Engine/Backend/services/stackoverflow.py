import httpx

STACK_API_BASE = "https://api.stackexchange.com/2.3/search/advanced"

async def fetch_stackoverflow(query: str, k: int = 5):
    params = {
        "order": "desc",
        "sort": "relevance",
        "q": query,
        "site": "stackoverflow",
        "pagesize": k
    }

    async with httpx.AsyncClient() as client:
        response = await client.get(STACK_API_BASE, params=params)
        data = response.json()

    results = []
    for item in data.get("items", []):
        results.append({
            "url": item.get("link"),
            "title": item.get("title"),
            "source": "stackoverflow"
        })

    return results
    params = {
        "order": "desc",
        "sort": "relevance",
        "q": query,
        "site": "stackoverflow",
        "pagesize": k
    }

    async with httpx.AsyncClient() as client:
        response = await client.get(STACK_API_BASE, params=params)
        data = response.json()

    links = []
    for item in data.get("items", []):
        links.append(item.get("link"))

    return links