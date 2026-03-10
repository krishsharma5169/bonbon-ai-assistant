import chromadb
from chromadb.config import Settings
import os

# Persistent storage path — stored inside your backend folder
DB_PATH = os.path.join(os.path.dirname(__file__), "..", "..", "chromadb_store")
COLLECTION_NAME = "bonbon_knowledge"

_client = None
_collection = None


def _get_collection():
    global _client, _collection

    if _collection is None:
        _client = chromadb.PersistentClient(path=os.path.abspath(DB_PATH))
        _collection = _client.get_or_create_collection(
            name=COLLECTION_NAME,
            metadata={"hnsw:space": "cosine"}  # cosine similarity for text
        )

    return _collection


def add_documents(documents: list[dict], embeddings: list[list[float]]):
    """
    Add documents to the vector store.

    Each document dict should have:
        - id: str (unique identifier)
        - text: str (the raw content)
        - metadata: dict (e.g. {"type": "algorithm", "topic": "sorting"})
    """
    collection = _get_collection()

    ids = [doc["id"] for doc in documents]
    texts = [doc["text"] for doc in documents]
    metadatas = [doc.get("metadata", {}) for doc in documents]

    collection.add(
        ids=ids,
        documents=texts,
        embeddings=embeddings,
        metadatas=metadatas
    )


def search(query_embedding: list[float], n_results: int = 3) -> list[dict]:
    """
    Search the vector store and return top-n matching chunks.
    Returns list of dicts with 'text' and 'metadata'.
    """
    collection = _get_collection()

    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=n_results,
        include=["documents", "metadatas", "distances"]
    )

    hits = []
    for text, meta, dist in zip(
        results["documents"][0],
        results["metadatas"][0],
        results["distances"][0]
    ):
        hits.append({
            "text": text,
            "metadata": meta,
            "score": round(1 - dist, 4)  # convert distance to similarity score
        })

    return hits


def collection_count() -> int:
    """Return how many documents are in the store."""
    return _get_collection().count()