# app.py

from fastapi import FastAPI
from services.pipeline import run_pipeline

app = FastAPI()

@app.get("/references")
async def get_references(q: str, k: int = 5):
    links = await run_pipeline(q, k)
    return {
        "query": q,
        "links": links
    }