import sys
import os

# Ensure root project folder is in Python path (fix for packaged app)
CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.abspath(os.path.join(CURRENT_DIR, ".."))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)


from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from backend.app.pipeline import solve
from backend.app.llm import ask_model
from backend.app.rag.retriever import retrieve_context


app = FastAPI()

# -------- Conversation Memory --------
conversation_history = []
MAX_HISTORY = 12


class PromptRequest(BaseModel):
    prompt: str


# -------- Intelligent Mode Detection --------
def detect_mode(prompt: str):
    p = prompt.lower()

    if "```" in prompt:
        return "DEV"

    if any(word in p for word in [
        "error", "exception", "stack trace",
        "why is", "doesn't work", "bug",
        "fix this", "debug"
    ]):
        return "DEV"

    if any(word in p for word in [
        "leetcode", "optimal", "time complexity",
        "hard problem", "binary tree", "dfs", "bfs",
        "dynamic programming", "find", "given an array",
        "most frequent", "k elements", "subarray",
        "linked list", "graph", "matrix", "return the",
        "sort", "search", "palindrome", "fibonacci",
        "two sum", "sliding window", "hash map",
        "minimum", "maximum", "longest", "shortest",
        "count", "frequency", "permutation", "combination"
    ]):
        return "DSA"

    if any(word in p for word in [
        "write a function", "implement",
        "create a program", "generate code",
        "build a program"
    ]):
        return "DEV"

    return "CHAT"


def get_rag_topics(prompt: str) -> list[str]:
    """
    Run a lightweight RAG retrieval just to get topic names for the UI.
    Returns a list of topic strings e.g. ["Top K Elements", "Heaps"]
    """
    try:
        from backend.app.rag.embedder import get_embedding
        from backend.app.rag.vectorstore import search, collection_count
        from backend.app.config import RAG_ENABLED, RAG_MIN_SCORE, RAG_TOP_K

        if not RAG_ENABLED or collection_count() == 0:
            return []

        query_embedding = get_embedding(prompt)
        hits = search(query_embedding, n_results=RAG_TOP_K)
        topics = [
            h["metadata"].get("topic", "Reference")
            for h in hits
            if h["score"] >= RAG_MIN_SCORE
        ]
        return topics
    except Exception:
        return []


# -------- Main Endpoint --------
@app.post("/solve")
def solve_problem(request: PromptRequest):
    global conversation_history

    prompt = request.prompt.strip()
    mode = detect_mode(prompt)

    # Add user message
    conversation_history.append({"role": "user", "content": prompt})
    conversation_history = conversation_history[-MAX_HISTORY:]

    # Build formatted history
    formatted_history = ""
    for msg in conversation_history:
        role = "User" if msg["role"] == "user" else "BonBon"
        formatted_history += f"{role}: {msg['content']}\n"

    # -------- DSA AGENT MODE --------
    if mode == "DSA":
        result = solve(prompt)
        print("RAG USED:", result.get("rag_used"))
        print("RAG TOPICS:", get_rag_topics(prompt))

        response_content = f"```python\n{result['code']}\n```"

        conversation_history.append({
            "role": "assistant",
            "content": response_content
        })

        conversation_history = conversation_history[-MAX_HISTORY:]

        # Get RAG topic names for UI display
        rag_topics = get_rag_topics(prompt) if result.get("rag_used") else []

        return {
            "type": "code",
            "content": response_content,
            "mode": result.get("mode"),
            "time": result.get("total_time"),
            "repairs": result.get("repair_attempts"),
            "rag_used": result.get("rag_used", False),
            "rag_topics": rag_topics
        }

    # -------- DEVELOPER EXPERT MODE --------
    elif mode == "DEV":
        response = ask_model(
            f"""
You are BonBon, a senior software engineer.

Rules:
- Diagnose errors precisely.
- Analyze provided code carefully.
- Explain WHY the issue happens.
- Provide corrected code when appropriate.
- Be concise but clear.
- Support C++, C#, Java, Python, JS, HTML, CSS, SQL, and frameworks.

Conversation so far:
{formatted_history}

BonBon:
"""
        )

    # -------- CHATGPT-VIBE MODE --------
    else:
        response = ask_model(
            f"""
You are BonBon, a highly intelligent, natural, human-like AI assistant.

Personality rules:
- Speak naturally (not robotic).
- Avoid generic filler phrases.
- Be structured and clear.
- Ask clarifying questions when useful.
- Adapt depth based on user tone.
- Feel like ChatGPT.
- Switch into precise developer mode if technical topics appear.

Conversation so far:
{formatted_history}

BonBon:
"""
        )

    conversation_history.append({
        "role": "assistant",
        "content": response
    })

    conversation_history = conversation_history[-MAX_HISTORY:]

    return {
        "type": "chat",
        "content": response
    }


# Mount frontend AFTER routes
# Absolute path for frontend (works in packaged + dev)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FRONTEND_DIR = os.path.join(BASE_DIR, "frontend")

app.mount("/", StaticFiles(directory=FRONTEND_DIR, html=True), name="frontend")