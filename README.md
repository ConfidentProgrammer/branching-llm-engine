# chat-tree-ai 🌲⚡

`chat-tree-ai` is an advanced, non-linear LLM conversation engine and interactive infinite canvas. Moving away from traditional linear chat windows, this project maps dialogue histories into a **branching tree architecture** where users can fork, branch, and inspect chat history at any depth.

## 🛠️ Tech Stack & Architecture

* **Frontend:** React, Vite, Tailwind CSS, `@xyflow/react` (React Flow) with a custom Neobrutalist design system.
* **Backend:** FastAPI (Python) implementing a clean Strategy Pattern for embedding providers.
* **Storage & RAG:** PostgreSQL with `pgvector` for combined relational tree storage and semantic vector search.
* **Context Isolation:** Uses ancestry-path metadata filtering on a single vector index to prevent cross-contamination between conversation branches.

## 🚀 Key Features

* **Visual Node Canvas:** Drag, zoom, and navigate conversation turns like a system diagram.
* **Pointer-Based Tree Structure:** Clean server-side relational mapping of parent-child node pointers.
* **Stateful RAG Payload Assembly:** Dynamically queries ancestor chunks at runtime to feed precise context back into the LLM API.
* **Neobrutalist UI:** High-contrast retro-modern aesthetics featuring solid borders, hard shadows, and monospaced typography.