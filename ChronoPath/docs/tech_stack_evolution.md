# Tech Stack & Tools Evolution

ChronoPath AI has undergone significant architectural shifts to reach its current industry-standard state. This document traces the evolution of our tech stack, the tools we used, and the rationale behind each migration.

## 1. Database & Persistence

### Initial State: SQLite3
- **Rationale**: Chosen for its simplicity, zero-configuration setup, and ease of local development.
- **The Challenge**: As the agentic framework grew, multiple asynchronous agents (Location, Narrative, Safety) began attempting to write to the `journeys` table simultaneously. This led to severe database lock contention and concurrency bottlenecks.

### Current State: PostgreSQL & asyncpg
- **Rationale**: PostgreSQL was adopted to handle high-concurrency transactional loads without locking. We paired it with the `asyncpg` driver in Python to take full advantage of native async/await connection pooling.
- **Additional Tooling**: We integrated the `pgvector` extension to allow for high-dimensional vector embeddings, enabling the Context Agent to perform semantic search across a user's past stories.

## 2. Authentication & Security

### Initial State: Custom JWT & Local JSON
- **Rationale**: A fast way to prototype user sessions without relying on external cloud providers. Implemented via a static `users_db.json` file.
- **The Challenge**: Managing secure token refresh lifecycles, password hashing, and scalable identity management locally became a significant security liability and development overhead.

### Current State: Google Firebase Authentication
- **Rationale**: We ripped out the custom JWT system in favor of Firebase. Firebase provides hardened, industry-standard identity management, completely decoupling user passwords from our backend. It also allowed us to easily integrate a seamless Google Sign-In OAuth flow on the frontend.

## 3. Generative AI & SDK Integration

### Initial State: `google.generativeai` SDK
- **Rationale**: The standard library for interacting with Google's early Gemini and PaLM models.
- **The Challenge**: As Google rapidly evolved their AI offerings, this SDK faced deprecation warnings. Furthermore, we experienced prompt formatting incompatibilities when attempting to use newer, highly-efficient models.

### Current State: `google.genai` SDK & `gemini-3.5-flash`
- **Rationale**: We migrated to the modern SDK to ensure future-proofing. We standardized on the `gemini-3.5-flash` model for its exceptional balance of low-latency generation and high reasoning capability, which is critical for real-time narrative generation.

## 4. Backend Orchestration

### Initial State: Linear Scripting
- **Rationale**: The backend originally processed location data and generated stories in a strict, linear pipeline.
- **The Challenge**: The narratives lacked depth, safety checks were hardcoded, and the system could not easily scale to include multi-modal (image) generation.

### Current State: FastAPI & The Supervisor Agent Pattern
- **Rationale**: We transitioned to **FastAPI** to handle highly concurrent API requests using Python's async features. 
- **Agentic Framework**: We implemented a Supervisor Pattern. The backend now spins up autonomous sub-agents (Context, Location, Narrative, Media, Reviewer, Safety). This decoupled architecture allows agents to run in parallel (e.g., generating the narrative while fetching semantic memory) and critique each other before responding to the user.

## 5. Frontend & UI Design

### Initial State: Basic React UI
- **Rationale**: A functional interface for testing API endpoints.
- **The Challenge**: Lacked the immersive, cinematic feel required for an AI storytelling application.

### Current State: Next.js 14+ & Tailwind CSS
- **Rationale**: We upgraded to Next.js for its robust routing and server-side rendering capabilities. We utilized Tailwind CSS to build a highly polished, responsive **Glassmorphism** design system. This modern aesthetic ensures the user feels immediately immersed in the experience the moment they log in.

## 6. Observability

### Initial State: Print Statements
- **Rationale**: Standard debugging during early prototyping.
- **The Challenge**: Impossible to track performance bottlenecks or agent latency in a production environment.

### Current State: OpenTelemetry & Prometheus
- **Rationale**: We integrated `FastAPIInstrumentor` and `prometheus_client`. The backend now exposes `/metrics` to track latency histograms and request counts, while `structlog` provides machine-readable JSON logs for tracking the exact execution path of every agent.
