from pydantic import BaseModel
from typing import List, Optional

class QueryRequest(BaseModel):
    question: str
    top_k: Optional[int] = 3

class ContextSnippet(BaseModel):
    content: str
    source: str
    score: float

class QueryResponse(BaseModel):
    context: List[ContextSnippet]

class RAGResponse(BaseModel):
    answer: str
    context: List[ContextSnippet]