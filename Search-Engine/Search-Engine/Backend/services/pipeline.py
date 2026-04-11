
import asyncio
from services.stackoverflow import fetch_stackoverflow
from services.github import fetch_github
from services.docs import fetch_docs
from services.ranker import rank_results
from utils.dedup import deduplicate

async def run_pipeline(query: str, k: int = 5):

    tasks = [
        fetch_stackoverflow(query, k),
        fetch_github(query, k),
        fetch_docs(query, k)
    ]

    results = await asyncio.gather(*tasks)

    merged = []
    for r in results:
        merged.extend(r)

    unique = deduplicate(merged)

    ranked = rank_results(query, unique, k)

    return [r["url"] for r in ranked]