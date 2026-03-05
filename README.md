# BonBon AI Assistant

BonBon is a **local AI-powered coding assistant** designed to help developers solve programming problems, debug code, and understand algorithms using locally hosted large language models.

The system integrates **FastAPI, Ollama, and DeepSeekCoder** to provide AI-assisted programming capabilities while running entirely on a local machine. The goal of BonBon is to provide a lightweight developer assistant without relying on external APIs or cloud-based AI services.

---

## Features

- AI-powered coding assistance
- Solve programming and Data Structures & Algorithms (DSA) problems
- Local LLM inference using Ollama
- REST API backend built with FastAPI
- Desktop interface powered by Electron
- Local-first architecture (no external API dependency)

---

## Technologies Used

### Backend
- Python
- FastAPI
- Ollama
- DeepSeekCoder (LLM)

### Frontend
- JavaScript
- Electron

### AI & Data
- Large Language Models (LLMs)
- Local AI inference
- Prompt-based code generation

---

## System Architecture

The BonBon architecture is designed to separate the user interface, backend API, and AI model integration.

User Interface (Electron)
↓
FastAPI Backend
↓
Ollama
↓
DeepSeekCoder LLM

1. The **Electron frontend** provides the user interface.
2. Requests are sent to the **FastAPI backend**.
3. The backend communicates with **Ollama**.
4. Ollama runs the **DeepSeekCoder LLM** locally.
5. AI-generated responses are returned to the user.

---

## Project Structure
bonbon-ai-assistant
│
├── backend/ # FastAPI backend and AI integration
├── frontend/ # Electron desktop interface
├── benchmark/ # Performance testing scripts
├── main.py # Python entry point
├── main.js # Electron application entry point
├── package.json # Node.js dependencies
├── .gitignore # Ignored files and build artifacts



---

## Installation

### 1. Clone the repository
git clone https://github.com/krishsharma5169/bonbon-ai-assistant.git
Navigate to the project folder:
cd bonbon-ai-assistant


---

### 2. Install Python dependencies
pip install -r requirements.txt


---

### 3. Install Node.js dependencies
npm install


---

### 4. Start the backend
python main.py


---

### 5. Start the frontend
npm start


---

## Example Use Cases

BonBon can assist developers with:

- Solving algorithm and DSA problems
- Generating code snippets
- Explaining programming concepts
- Debugging logic errors
- Learning new programming techniques

---

## Future Improvements

Planned improvements for the project include:

- Multi-agent AI architecture
- Codebase-aware AI assistance
- Retrieval-Augmented Generation (RAG)
- Improved developer tooling
- Performance optimization

---

## Author

Krish Sharma  
BSc Computer Science (Artificial Intelligence)  
Asia Pacific University of Technology & Innovation  

GitHub:  
https://github.com/krishsharma5169

LinkedIn:  
https://www.linkedin.com/in/krish-sharma-2457a322a/

---

## License

This project is intended for educational and research purposes.





