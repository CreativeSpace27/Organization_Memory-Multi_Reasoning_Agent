# services/ranker.py

from sentence_transformers import SentenceTransformer
import numpy as np

model = SentenceTransformer("all-MiniLM-L6-v2")

def rank_results(query, results, k=5):
    if not results:
        return []

    texts = [r["title"] for r in results]

    query_emb = model.encode(query)
    doc_embs = model.encode(texts)

    scores = np.dot(doc_embs, query_emb)

    ranked = sorted(zip(results, scores), key=lambda x: x[1], reverse=True)

    return [r[0] for r in ranked[:k]]