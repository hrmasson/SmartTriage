# ❓ FAQ — SmartTriage

This document answers common questions about SmartTriage, its design, components, and usage.

---

### 🤔 Why use LocalAI instead of OpenAI?

**LocalAI** runs models locally with no internet dependency or API costs.  
This is especially useful when:
- Running in secure environments (e.g. healthcare, enterprise IT),
- Needing full control over model behavior and data,
- Avoiding OpenAI rate limits, outages, or cost scaling.

You can still use OpenAI-compatible APIs if needed — just update `base_url` and `model_name` in `.env`.

---

### 🧠 What models are supported?

Any model that is:
- Compatible with **GGUF format**,
- Loadable by **LocalAI** or similar frameworks (e.g., Ollama),
- Used for **chat/completion** tasks (e.g., Mistral, LLaMA2, Gemma).

Default: `mistral-7b-instruct`.

---

### 🔁 Can I replace the routing model (Decision Tree)?

Yes. The dispatcher is model-agnostic.  
You can retrain using scikit-learn (e.g. Random Forest, SVM) or integrate a remote service.

Just update:
- `models/dispatcher/model.pkl`
- `models/dispatcher/labels.pkl`

---

### 📚 How is the knowledge base indexed?

Using:
- LangChain document wrappers,
- HuggingFace embeddings (`sentence-transformers/all-MiniLM-L6-v2`),
- FAISS for fast similarity search.

You can rebuild the index from a JSON file via `KnowledgeBaseIndexer`.

---

### 🐇 What does RabbitMQ do in this project?

RabbitMQ connects SmartTriage with external systems.

- Input queue = raw messages (to be triaged),
- Output queue = structured triage result (problem + category + solution + destination).

You can integrate this with a ticketing system, EMR, chatbot, etc.

---

### 🔐 Is the LLM request secure?

All processing stays **local** when using LocalAI + Docker.  
No data is sent to external APIs — ideal for sensitive environments.

To enforce HTTPS or add auth, configure LocalAI behind a reverse proxy (e.g. Nginx + TLS).

---

### 🧪 How can I test it?

You can test the system end-to-end by:

1. Starting the service: `python run.py`
2. Publishing a test message to the input queue (e.g. with `pika` or Postman).
3. Watching logs or reading from the output queue.

---

### 🛠 Something broke — where are logs?

- All logs go to both **console** and **`smarttriage.log`**.
- Look there first if something hangs or crashes.
- You can increase verbosity by changing `level=logging.DEBUG` in `run.py`.

---

### 📦 Can I use it as a microservice?

Yes. SmartTriage is modular and Docker-friendly.  
You can wrap it in an API gateway, deploy as part of a larger triage flow, or expose endpoints via FastAPI.

---
