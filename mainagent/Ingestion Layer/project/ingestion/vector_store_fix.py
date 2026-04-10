import chromadb
from sentence_transformers import SentenceTransformer
import uuid

class VectorStore:
    def __init__(self):
        self.client = chromadb.PersistentClient(path="./chroma_db")
        self.collection = self.client.get_or_create_collection(name="decisions")
        self.embedding_model = SentenceTransformer("all-MiniLM-L6-v2")

    def store(self, text, metadata):
        # Convert lists to comma-separated strings for ChromaDB compatibility
        cleaned_metadata = {}
        for key, value in metadata.items():
            if isinstance(value, list):
                # Join list items with comma, skip if empty
                cleaned_metadata[key] = ", ".join(str(item) for item in value) if value else None
            else:
                cleaned_metadata[key] = value
        
        # Remove None values (ChromaDB doesn't like them either)
        cleaned_metadata = {k: v for k, v in cleaned_metadata.items() if v is not None}
        
        embedding = self.embedding_model.encode(text).tolist()
        
        self.collection.add(
            embeddings=[embedding],
            documents=[text],
            metadatas=[cleaned_metadata],
            ids=[str(uuid.uuid4())]
        )

    def search(self, query):
        embedding = self.embedding_model.encode(query).tolist()
        results = self.collection.query(
            query_embeddings=[embedding],
            n_results=3
        )
        return results
