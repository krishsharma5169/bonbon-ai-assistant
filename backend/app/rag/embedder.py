import requests

OLLAMA_EMBED_URL = "http://localhost:11434/api/embeddings"
EMBED_MODEL = "nomic-embed-text"


def get_embedding(text: str) -> list[float]:
    """
    Generate an embedding vector for the given text
    using nomic-embed-text via Ollama.
    """
    try:
        response = requests.post(
            OLLAMA_EMBED_URL,
            json={
                "model": EMBED_MODEL,
                "prompt": text
            },
            timeout=30
        )
        response.raise_for_status()
        return response.json()["embedding"]

    except requests.exceptions.RequestException as e:
        raise RuntimeError(f"Embedding failed: {e}")