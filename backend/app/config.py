MODEL_NAME = "qwen2.5-coder:7b"

OLLAMA_URL = "http://localhost:11434/api/generate"

MODEL_CONFIG = {
    "temperature": 0.15,      # low = deterministic
    "top_p": 0.8,
    "repeat_penalty": 1.1,
    "num_ctx": 8192
}

MAX_ATTEMPTS = 4
DEBUG = True
FAST_MODE = True
AUTO_ESCALATE = True
ESCALATE_ON_REPAIR = True
ESCALATE_ON_CRITIC_REWRITE = True

# ─────────────────────────────────────────────────
# RAG Settings
# ─────────────────────────────────────────────────
RAG_ENABLED = True           # Toggle RAG on/off globally
RAG_TOP_K = 3                # How many chunks to retrieve
RAG_MIN_SCORE = 0.45         # Minimum cosine similarity (0-1) to include a result