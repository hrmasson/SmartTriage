
# SmartTriage

SmartTriage is an automated triage and routing system designed to analyze incoming user messages, identify the underlying problem, suggest relevant knowledge base solutions, and assign the issue to the appropriate department for resolution.

[FAQ — Frequently Asked Questions](FAQ.md)
---

## 🚀 Purpose

This project is built to:

- Process free-form **incoming messages** (from users, employees, or clients),
- Use a **Large Language Model (LLM)** to extract a structured **problem and category**,
- Retrieve **related solutions** from a local **semantic knowledge base**,
- Determine the correct **department** to handle the issue via a decision tree,
- **Send the final enriched message** to an output queue (e.g., for human review or automation).

---

## 🧠 How It Works

1. **LLM Extraction**
    - The input message is passed to an LLM API.
    - The model returns:
        - `problem`: a short, reworded summary.
        - `category`: a single-word tag (e.g., `network`, `hardware`).

2. **Knowledge Base Search**
    - The extracted problem is passed into a vector search engine.
    - **FAISS + HuggingFace embeddings + LangChain** are used to find the most relevant entries in a JSON-based knowledge base.

3. **Routing**
    - A **decision tree classifier** receives the `problem + category` and predicts the target department.

4. **Message Dispatch**
    - The message, extracted data, suggested solution, and destination are packed into a result and **sent to RabbitMQ** for downstream processing.

---


## ⚙️ Setup

### 1. Install dependencies

```bash
pip install -r requirements.txt
```

### 2. Set up environment

Create a `.env` file based on the following:

```dotenv
LOCALAI_BASE_URL=http://localhost
LOCALAI_PORT=8083
LOCALAI_MODEL_NAME=mistral

KNOWLEDGE_BASE_DATASET_PATH=data/knowledge_base_dataset.json
KNOWLEDGE_BASE_INDEX_PATH=models/indices/faq_index
KNOWLEDGE_BASE_MODEL_NAME=sentence-transformers/all-MiniLM-L6-v2

DISPATCHER_MODEL_PATH=models/dispatcher/model.pkl
DISPATCHER_LABELS_PATH=models/dispatcher/labels.pkl

RABBITMQ_HOST=localhost
RABBITMQ_USER=rabbitmq
RABBITMQ_PASS=rabbitmq
RABBIT_INPUT_QUEUE=input_queue
RABBIT_OUTPUT_QUEUE=output_queue
```
### 3. Train the dispatcher model

```bash
python dispatcher/train.py
```
---

## ▶️ Run the service

### 1. Start docker containers
```bash
 ./start_docker.sh
```
This script performs the following steps:
1. Loads environment variables from .env (if present).
2. Defines model info: name, file, download URL, and local path.
3. Downloads the model from Hugging Face if it’s not already present locally. 
4. .Starts Docker containers via docker-compose up -d. 
5. Waits for LocalAI API to become available at the configured port. 
6. Waits for the model (mistral) to fully load and appear in the LocalAI model list. 
7. Prints confirmation once the model is ready for use.

### 2. Start the triage engine
```bash
python run.py
```

This starts:
- The main triage engine (`MainService`)
- The RabbitMQ `Consumer`, which listens to input messages
- Automatic dispatch of results to the output queue

Logs are saved to `smarttriage.log` and printed to console.

---

## 🧪 Example Input

```json
{
  "text": "VPN keeps disconnecting while I upload large files"
}
```

→ Output (internally):

```json
{
  "problem": "unstable vpn during file uploads",
  "category": "network",
  "solutions": {
    "title": "How to fix VPN drops on large uploads",
    "url": "https://kb.example.com/vpn-fix"
  },
  "destination": "IT"
}
```

---

## 📁 Project Structure

```
├── orchestrator/         # Core logic (MainService)
├── llm/                  # LLM wrapper (LocalAIClient, LlmService)
├── knowledge_base/       # Semantic KB search (FAISS, LangChain)
├── dispatcher/           # Decision Tree classifier
├── rabbit/               # RabbitMQ Producer & Consumer
├── config/               # Settings (via pydantic)
├── run.py                # Entry point
├── .env                  # Environment configuration
├── smarttriage.log       # Log file
```

---
