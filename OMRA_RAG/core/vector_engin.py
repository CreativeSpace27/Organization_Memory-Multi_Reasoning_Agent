from langchain_community.vectorstores import Chroma
from .embedding_model import get_embedding_function
import os

CHROMA_PATH = os.getenv("CHROMA_PATH")

def save_to_chroma(chunks):
    db = Chroma.from_documents(
        chunks, 
        get_embedding_function(), 
        persist_directory=CHROMA_PATH
    )
    db.persist()

def query_chroma(query_text: str, k: int = 3):
    db = Chroma(persist_directory=CHROMA_PATH, embedding_function=get_embedding_function())
    
    # Search for top K relevant chunks
    results = db.similarity_search_with_relevance_scores(query_text, k=k)
    
    return results