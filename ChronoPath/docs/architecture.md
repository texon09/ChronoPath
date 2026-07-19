# System Architecture

ChronoPath AI is built on a highly concurrent, agentic framework designed to provide immersive, historically accurate location-based narratives. The system is split into a Next.js frontend and a FastAPI backend orchestrating several autonomous agents.

## 1. High-Level Architecture
- **Frontend Layer**: Next.js 14+ (React), styled with Tailwind CSS, utilizing a modern Glassmorphism design system for maximum immersion.
- **Backend Layer**: FastAPI (Python 3.10+) handling asynchronous API requests and agent orchestration.
- **Data Layer**: PostgreSQL with `asyncpg` for high-performance concurrent writes (managing user journey history) and Vector Embeddings (`pgvector`) for semantic search of past stories.
- **Authentication**: Google Firebase Auth integration ensuring secure, decoupled identity management.

## 2. Agentic Framework (The Supervisor Pattern)
The core intelligence of ChronoPath AI is orchestrated by a **Supervisor Agent**, which delegates tasks to specialized sub-agents based on the user's location and request.

### The Supervisor (`agents/supervisor.py`)
Acts as the central router. When a user requests a narrative generation, the Supervisor:
1. Instantiates the Location Agent to determine coordinates and context.
2. In parallel, gathers contextual history and semantic memory.
3. Delegates narrative drafting to the Narrative Agent.
4. Passes the draft to the Safety and Reviewer Agents.
5. Aggregates media assets from the Media Agent.

### Sub-Agents
* **Location Agent**: Interfaces with Google Maps and OpenStreetMap APIs to resolve Latitude/Longitude into a precise point of interest. Utilizes *Contextual Scoping* (appending City, State, Country) to prevent geospatial hallucination.
* **Context Agent**: Retrieves the user's past journeys from PostgreSQL and semantically retrieves similar historical contexts using embeddings.
* **Narrative Agent**: The core storyteller. Uses Gemini 3.5 Flash to synthesize the location data and user context into an educational, immersive narrative.
* **Reviewer Agent**: Critiques the Narrative Agent's draft for historical accuracy and tone, forcing rewrites if necessary.
* **Media Agent**: Generates cinematic, historically accurate images of the location using `image.pollinations.ai`.
* **Safety Agent**: A strict gatekeeper ensuring the narrative contains no PII, prompt injections, or inappropriate content.

## 3. Observability & Telemetry
- **Prometheus Metrics**: The backend exposes `/metrics` to track Request Counts, Latency Histograms, and Agent Execution times.
- **OpenTelemetry**: Integrated via `FastAPIInstrumentor` for distributed tracing across agent boundaries.
- **Structured Logging**: `structlog` provides machine-readable JSON logs for production debugging.
