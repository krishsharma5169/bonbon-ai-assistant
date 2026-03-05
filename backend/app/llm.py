import requests

OLLAMA_URL = "http://localhost:11434/api/generate"

SYSTEM_PROMPT = """
You are BonBon, an intelligent AI programming assistant.

Primary expertise:
- Data Structures and Algorithms (DSA)
- Python, Java, C++, C#, JavaScript, HTML, CSS
- Debugging code
- Explaining programming concepts clearly

If a term is ambiguous (e.g., DSA), prefer programming-related meanings
unless the user clearly refers to marketing or advertising.

Be clear, technical when needed, but friendly and conversational.
"""

# In-memory conversation history
conversation_history = []

def ask_model(user_prompt, temperature=0.7):

    global conversation_history

    coding_keywords = [
        "code", "error", "exception", "debug",
        "python", "java", "c++", "javascript",
        "algorithm", "binary", "array", "function",
        "dsa", "data structure"
    ]

    if any(word in user_prompt.lower() for word in coding_keywords):
        model = "deepseek-coder:6.7b"
    else:
        model = "llama3:8b"

    # Add user message to history
    conversation_history.append(f"User: {user_prompt}")

    # Keep only last 10 messages to prevent context explosion
    if len(conversation_history) > 10:
        conversation_history = conversation_history[-10:]

    full_prompt = (
        SYSTEM_PROMPT
        + "\n\n"
        + "\n".join(conversation_history)
        + "\nBonBon:"
    )

    try:
        response = requests.post(
            OLLAMA_URL,
            json={
                "model": model,
                "prompt": full_prompt,
                "temperature": temperature,
                "stream": False
            },
            timeout=60
        )

        response.raise_for_status()

        data = response.json()
        model_reply = data.get("response", "Model returned no response.")

        # Add model reply to history
        conversation_history.append(f"BonBon: {model_reply}")

        return model_reply

    except requests.exceptions.RequestException as e:
        return f"Error connecting to local model: {str(e)}"


def clear_memory():
    global conversation_history
    conversation_history = []