from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_core.documents import Document
import os

def process_document(file_path: str):
    # 1. Load PDF
    loader = PyPDFLoader(file_path)
    documents = loader.load()
    
    # 2. Split into Chunks
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=int(os.getenv("CHUNK_SIZE", 800)),
        chunk_overlap=int(os.getenv("CHUNK_OVERLAP", 100)),
        length_function=len,
        add_start_index=True,
    )
    chunks = text_splitter.split_documents(documents)
    print(f"Split {len(documents)} pages into {len(chunks)} chunks.")
    
    return chunks