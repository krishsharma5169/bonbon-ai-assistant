from backend.app.rag.embedder import get_embedding
from backend.app.rag.vectorstore import search, collection_count
from backend.app.config import RAG_TOP_K, RAG_MIN_SCORE, RAG_ENABLED


def retrieve_context(problem: str) -> str:
    """
    Given a DSA problem string, retrieve the most relevant
    algorithm explanations and problem patterns from ChromaDB.

    Returns a formatted context string to inject into the prompt,
    or an empty string if RAG is disabled / no relevant results found.
    """
    if not RAG_ENABLED:
        return ""

    if collection_count() == 0:
        return ""

    try:
        query_embedding = get_embedding(problem)
        hits = search(query_embedding, n_results=RAG_TOP_K)

        # Filter by minimum similarity score
        hits = [h for h in hits if h["score"] >= RAG_MIN_SCORE]

        if not hits:
            return ""

        # Format into a clean context block for the prompt
        context_parts = []
        for i, hit in enumerate(hits, 1):
            topic = hit["metadata"].get("topic", "General")
            kind = hit["metadata"].get("type", "note")
            context_parts.append(
                f"[Reference {i} | {kind} | {topic}]\n{hit['text']}"
            )

        return "\n\n".join(context_parts)

    except Exception as e:
        # RAG failure should never break the main pipeline
        print(f"[RAG] Retrieval failed (skipping): {e}")
        return ""