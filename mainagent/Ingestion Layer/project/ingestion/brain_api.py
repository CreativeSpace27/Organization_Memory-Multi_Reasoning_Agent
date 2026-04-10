from fastapi import FastAPI
from pydantic import BaseModel
from typing import List, Optional

app = FastAPI()

# This matches the "Contract" your ingestion layer expects
class DecisionSchema(BaseModel):
    decision: Optional[str]
    reasoning: List[str]
    alternatives: List[str]
    source: str

@app.post("/store-decision")
async def store_decision(data: DecisionSchema):
    print("\n--- 🧠 BRAIN RECEIVED NEW DATA ---")
    print(f"DECISION: {data.decision}")
    print(f"REASONING: {data.reasoning}")
    print(f"SOURCE: {data.source}")
    print("----------------------------------\n")
    return {"message": "Decision stored in memory!"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8001)