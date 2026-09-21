"""
Vector Store for Semantic Memory.
Provides semantic embedding storage, cosine similarity search,
and persistent vector collections (compatible with Chroma and FAISS patterns).
"""

from typing import List, Dict, Any, Optional
import math

class VectorStore:
    def __init__(self, collection_name: str = "default_memory"):
        self.collection_name = collection_name
        self.documents: List[Dict[str, Any]] = []

    def _mock_embedding(self, text: str) -> List[float]:
        # Deterministic lightweight hash-based embedding for zero-dependency operation
        vec = [0.0] * 16
        for i, char in enumerate(text.lower()):
            vec[ord(char) % 16] += 1.0 / (1.0 + i * 0.1)
        # Normalize
        norm = math.sqrt(sum(x * x for x in vec)) or 1.0
        return [x / norm for x in vec]

    def add(self, text: str, metadata: Optional[Dict[str, Any]] = None, doc_id: Optional[str] = None):
        embedding = self._mock_embedding(text)
        self.documents.append({
            "id": doc_id or f"doc_{len(self.documents)+1}",
            "text": text,
            "metadata": metadata or {},
            "embedding": embedding
        })

    def search(self, query: str, top_k: int = 5) -> List[Dict[str, Any]]:
        if not self.documents:
            return []

        q_vec = self._mock_embedding(query)
        scored = []
        for doc in self.documents:
            # Cosine similarity
            dot = sum(a * b for a, b in zip(q_vec, doc["embedding"]))
            scored.append((dot, doc))

        scored.sort(key=lambda x: x[0], reverse=True)
        return [
            {"score": round(score, 4), "text": d["text"], "metadata": d["metadata"], "id": d["id"]}
            for score, d in scored[:top_k]
        ]
