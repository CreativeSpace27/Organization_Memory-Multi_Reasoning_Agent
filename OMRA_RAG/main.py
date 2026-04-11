from fastapi import FastAPI
from api.routes import router as api_router
import uvicorn
import os

app = FastAPI(title="OMRA Standalone RAG Service")

# Create directories if they don't exist
os.makedirs("data_input", exist_ok=True)
os.makedirs("storage/chroma_db", exist_ok=True)

app.include_router(api_router, prefix="/rag")

@app.get("/health")
def health_check():
    return {"status": "RAG Engine Online"}

if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8080, reload=True)