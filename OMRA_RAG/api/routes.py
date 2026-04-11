from fastapi import APIRouter, UploadFile, File, HTTPException
from .schemas import QueryRequest, QueryResponse, ContextSnippet, RAGResponse
from core.ingestor import process_document
from core.vector_engin import save_to_chroma, query_chroma
from core.llm_generator import generate_answer
import shutil
import os

router = APIRouter()

@router.post("/upload")
async def upload_document(file: UploadFile = File(...)):
    temp_path = f"data_input/{file.filename}"
    
    # Save file locally
    with open(temp_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    
    try:
        chunks = process_document(temp_path)
        save_to_chroma(chunks)
        return {"status": "success", "message": f"Processed {len(chunks)} chunks from {file.filename}"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/retrieve", response_model=QueryResponse)
async def retrieve_context(request: QueryRequest):
    results = query_chroma(request.question, k=request.top_k)
    
    context = [
        ContextSnippet(
            content=doc.page_content,
            source=doc.metadata.get("source", "Unknown"),
            score=score
        ) for doc, score in results
    ]
    
    return QueryResponse(context=context)


@router.post("/ask", response_model=RAGResponse)
async def ask_question(request: QueryRequest):
    """Full RAG: Retrieve context + Generate answer using LLM"""
    results = query_chroma(request.question, k=request.top_k)
    
    # Generate answer using LLM
    answer = generate_answer(request.question, results)
    
    # Prepare context snippets
    context = [
        ContextSnippet(
            content=doc.page_content,
            source=doc.metadata.get("source", "Unknown"),
            score=score
        ) for doc, score in results
    ]
    
    return RAGResponse(answer=answer, context=context)
