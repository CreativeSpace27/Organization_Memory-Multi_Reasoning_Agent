from fastapi import FastAPI
from pydantic import BaseModel
from typing import List

app = FastAPI()

class Decision(BaseModel):
    decision: str
    reasoning: List[str]
    alternatives: List[str]
    source: str
    impacts:list[str]

@app.post("/store-decision")
async def store_decision(data: Decision):
    print(f"🧠 BRAIN RECEIVED: {data.decision}")
    return {"status": "success"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8001)