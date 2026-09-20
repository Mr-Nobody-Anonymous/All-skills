# 🥈 Intermediate Engineering Projects

Production-oriented projects emphasizing distributed components, authentication, testing, and cloud infrastructure.

---

## 1. Fullstack SaaS Task & Project Hub (`team-sync-saas`)
- **Objective**: Multi-tenant task manager with team workspaces, real-time updates, and subscription billing.
- **Architecture**: Next.js App Router, Tailwind CSS, PostgreSQL via Drizzle ORM, WebSockets, Supabase Auth.
- **Key Features**: RBAC (Admin, Member, Viewer), optimistic UI updates, automated GitHub Actions CI/CD.

## 2. High-Throughput REST & GraphQL API Gateway (`gateway-service`)
- **Objective**: Reverse proxy and API gateway providing unified auth, rate limiting, and request caching.
- **Architecture**: Go or Rust backend, Redis token-bucket rate limiter, JWT validation middleware.
- **Key Features**: Prometheus metrics exporter, structured JSON logging, distributed tracing headers.

## 3. Local Document Retrieval Augmented Generation (RAG) System (`rag-docs`)
- **Objective**: Search and chat with local PDF and markdown knowledge bases.
- **Architecture**: Python FastAPI backend, Qdrant vector database, Hugging Face BGE embeddings, Ollama / vLLM.
- **Key Features**: Semantic hybrid search, chunking optimization, source citation verification.
