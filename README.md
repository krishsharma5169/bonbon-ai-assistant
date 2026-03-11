# BonBon AI Coding Assistant

BonBon is a **fully local AI-powered coding assistant** built as an Electron desktop application. It solves programming problems, assists with Data Structures & Algorithms, and helps debug code — all using locally hosted large language models with no cloud dependency, no API keys, and no data leaving your machine.

---

## Features

- **Intelligent Mode Detection** — automatically routes prompts to DSA, DEV, or CHAT pipelines
- **Agentic DSA Pipeline** — multi-stage pipeline with repair loop, critic agent, and auto-escalation
- **RAG (Retrieval-Augmented Generation)** — retrieves relevant algorithm patterns from a local knowledge base before generating solutions
- **FAST vs VOTING Mode** — single generation for speed, dual-generation with comparison for hard problems
- **Critic Agent** — second LLM pass reviews every solution for optimality and rewrites if needed
- **Auto-Escalation** — automatically escalates to VOTING mode when FAST mode struggles
- **Solution Explanations** — every DSA response includes approach, time complexity, and space complexity
- **Syntax Highlighted Code** — clean code output with highlight.js
- **RAG Badge** — UI shows which knowledge base patterns were retrieved and used
- **Fully Local** — Qwen2.5-Coder 7B via Ollama, ChromaDB, nomic-embed-text — zero cloud dependency

---

## Tech Stack

### Backend
- Python, FastAPI, Uvicorn
- Ollama + Qwen2.5-Coder 7B (LLM)
- ChromaDB (vector database)
- nomic-embed-text (embeddings)

### Frontend
- Electron (desktop app)
- Vanilla JavaScript, HTML, CSS
- marked.js (markdown rendering)
- highlight.js (syntax highlighting)

---

## System Architecture

```
User Input (Electron UI)
        ↓
  Mode Detection
  (DSA / DEV / CHAT)
        ↓
   ┌────────────────────────────┐
   │      DSA Pipeline          │
   │  1. RAG Retrieval          │
   │  2. Code Generation        │
   │  3. Execution & Repair     │
   │  4. Critic Agent           │
   │  5. Auto-Escalation        │
   │  6. Explanation Generation │
   └────────────────────────────┘
        ↓
  FastAPI Backend
        ↓
  Ollama → Qwen2.5-Coder 7B (local)
        ↓
  Response → Electron UI
```

---

## Project Structure

```
bonbon-ai-assistant/
│
├── backend/
│   ├── app/
│   │   ├── config.py         # Model settings, RAG config, pipeline flags
│   │   ├── pipeline.py       # Agentic DSA pipeline
│   │   ├── prompts.py        # Structured, repair, critic prompts
│   │   ├── executor.py       # Python code execution sandbox
│   │   ├── llm.py            # Ollama LLM interface
│   │   └── rag/
│   │       ├── ingestor.py   # Embed and store knowledge base
│   │       ├── retriever.py  # Retrieve relevant context
│   │       ├── embedder.py   # Generate embeddings
│   │       └── vectorstore.py # ChromaDB interface
│   └── main.py               # FastAPI app, mode detection, routing
│
├── frontend/
│   ├── index.html            # Main UI
│   ├── script.js             # Frontend logic
│   ├── style.css             # Styling
│   └── main.js               # Electron entry point
│
├── start_bonbon.bat          # Launch script (Windows)
├── package.json              # Node.js dependencies
├── requirements.txt          # Python dependencies
└── .gitignore
```

---

## Prerequisites

Before setting up BonBon, make sure you have the following installed:

- **Python 3.11** (required — ChromaDB is not compatible with 3.12+)
- **Node.js** (v18 or higher)
- **Ollama** — download from [https://ollama.com](https://ollama.com)

### Pull required Ollama models

```bash
ollama pull qwen2.5-coder:7b
ollama pull nomic-embed-text
```

---

## Installation

### 1. Clone the repository

```bash
git clone https://github.com/krishsharma5169/bonbon-ai-assistant.git
cd bonbon-ai-assistant
```

### 2. Create a Python 3.11 virtual environment

```bash
py -3.11 -m venv .venv
```

### 3. Activate the virtual environment

```bash
.venv\Scripts\activate
```

### 4. Install Python dependencies

```bash
pip install -r requirements.txt
```

### 5. Install Node.js dependencies

```bash
npm install
```

### 6. Build the RAG knowledge base

Run this once to embed and store the algorithm patterns into ChromaDB:

```bash
py -m backend.app.rag.ingestor
```

---

## Running BonBon

### Windows (Recommended) — use the bat file

Double-click `start_bonbon.bat` or run it from the terminal:

```bash
start_bonbon.bat
```

This will:
1. Kill any leftover Python processes on port 8000
2. Launch the Electron app
3. Electron automatically starts the FastAPI backend using your `.venv` Python
4. Kill the backend process when you close the app

> **Note:** You can create a desktop shortcut to `start_bonbon.bat` for quick access. Right-click the file → Send to → Desktop (create shortcut).

### Manual launch (alternative)

If you prefer to run manually, start the backend first:

```bash
.venv\Scripts\activate
py -m uvicorn backend.main:app --host 127.0.0.1 --port 8000
```

Then in a separate terminal launch the frontend:

```bash
npx electron .
```

---

## Configuration

All settings are in `backend/app/config.py`:

```python
MODEL_NAME = "qwen2.5-coder:7b"   # LLM model
MAX_ATTEMPTS = 4                    # Max repair loop attempts
FAST_MODE = True                    # Use FAST mode by default
AUTO_ESCALATE = True                # Auto-escalate to VOTING on failures
RAG_ENABLED = True                  # Toggle RAG on/off
RAG_TOP_K = 3                       # Number of chunks to retrieve
RAG_MIN_SCORE = 0.2                 # Minimum cosine similarity threshold
```

---

## Adding to the Knowledge Base

To add your own algorithm notes or LeetCode patterns, open `backend/app/rag/ingestor.py` and add entries to the `LEETCODE_PATTERNS` list:

```python
{
    "topic": "Your Pattern Name",
    "text": """Pattern: Description
Approach: ...
Time: O(n). Space: O(1)."""
},
```

Then re-run the ingestor:

```bash
py -m backend.app.rag.ingestor
```

---

## RAG Performance Results

After adding a Stack using Queues pattern to the knowledge base:

| Metric | Before RAG | After RAG |
|--------|-----------|-----------|
| Solution quality | Buggy | Correct |
| Solve time | 117s | 28s |
| Repair attempts | 1 | 0 |

---

## Troubleshooting

### Wrong Python version being used

BonBon requires **Python 3.11**. ChromaDB and some dependencies are not compatible with Python 3.12 or higher.

If you have multiple Python versions installed, make sure you create the venv explicitly with 3.11:

```bash
py -3.11 -m venv .venv
```

To verify the venv is using the right version:

```bash
.venv\Scripts\python.exe --version
# Should output: Python 3.11.x
```

---

### Blank terminal when opening PyCharm

If PyCharm's terminal opens blank after setting a custom shell path, go to:

**Settings → Tools → Terminal** and set Shell path back to:

```
cmd.exe
```

Then activate manually each time:

```bash
.venv\Scripts\activate
```

---

### Port 8000 already in use

If you see this error:

```
[Errno 10048] error while attempting to bind on address ('127.0.0.1', 8000)
```

It means a previous backend process is still running. Kill it with:

```bash
taskkill /f /im python.exe
```

The `start_bonbon.bat` file handles this automatically — it kills existing Python processes before launching.

---

### Connection Error: Failed to fetch

This means the frontend loaded but the backend isn't running. Either:

- The backend crashed on startup — check the terminal window for Python errors
- The backend took too long to start — the bat file waits 4 seconds by default

Check `backend.log` in the project root for backend startup errors.

---

### Electron using wrong Python (system Python instead of venv)

If you see errors about missing modules like `chromadb` or `fastapi`, Electron is spawning the wrong Python. This is configured in `frontend/main.js`:

```javascript
const pythonPath = app.isPackaged
    ? path.join(process.resourcesPath, "app.asar.unpacked", ".venv", "Scripts", "python.exe")
    : path.join(app.getAppPath(), ".venv", "Scripts", "python.exe");
```

Make sure your `.venv` folder is in the project root (`bonbon-ai-assistant/.venv`). If you created it somewhere else, update this path accordingly.

---

### electron-builder fails with symbolic link error

If `npx electron-builder` fails with:

```
A required privilege is not held by the client
```

Either run your terminal as Administrator, or enable Developer Mode in Windows:

**Settings → Privacy & Security → For Developers → Developer Mode → On**

---

### RAG badge not showing

If the backend logs show `RAG Used: True` but the badge isn't appearing in the UI:

1. Hard refresh the Electron window with **Ctrl+Shift+R**
2. In `frontend/index.html`, bump the cache-busting version on the script tag:
   ```html
   <script src="script.js?v=2"></script>
   ```
3. Close and relaunch via `start_bonbon.bat`

---

### RAG retrieving but scores below threshold

Run this diagnostic to see actual similarity scores:

```bash
py -c "from backend.app.rag.embedder import get_embedding; from backend.app.rag.vectorstore import search; q = get_embedding('your problem here'); hits = search(q, n_results=3); [print(h['score'], h['metadata']['topic']) for h in hits]"
```

If scores are consistently below `RAG_MIN_SCORE`, lower the threshold in `config.py`:

```python
RAG_MIN_SCORE = 0.2
```

Or add more relevant patterns to the knowledge base via `ingestor.py`.

---

## Author

**Krish Sharma**
BSc Computer Science (Artificial Intelligence)
Asia Pacific University of Technology & Innovation

- GitHub: [github.com/krishsharma5169](https://github.com/krishsharma5169)
- LinkedIn: [linkedin.com/in/krish-sharma-2457a322a](https://www.linkedin.com/in/krish-sharma-2457a322a/)

---

## License

This project is intended for educational and research purposes.