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
        "dynamic programming"
    ]):
        return "DSA"

    if any(word in p for word in [
        "write a function", "implement",
        "create a program", "generate code",
        "build a program"
    ]):
        return "DEV"

    return "CHAT"


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

        response_content = result["code"]

        conversation_history.append({
            "role": "assistant",
            "content": response_content
        })

        conversation_history = conversation_history[-MAX_HISTORY:]

        return {
            "type": "code",
            "content": response_content,
            "mode": result.get("mode"),
            "time": result.get("total_time"),
            "repairs": result.get("repair_attempts")
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