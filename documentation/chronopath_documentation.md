# ChronoPath AI: Complete System Documentation

ChronoPath AI is a highly advanced, agentic orchestration platform designed to generate hyper-personalized, historically accurate, and contextually rich narratives based on a user's geographical location. It moves beyond standard prompt-engineering by utilizing a custom Agent Development Kit (ADK), Agentic RAG routing, Vector-based semantic memory, and autonomous self-critique loops.

---

## 1. Summary of Product
When a user arrives at a specific coordinate on earth (e.g., the Eiffel Tower or an obscure Roman ruin), ChronoPath identifies their exact historical and geographical context. By analyzing their personal interests, age, demographic, and past travel history (Semantic Vector Memory), it autonomously writes, critiques, and delivers a highly engaging, bespoke audio-ready narrative about the location.

---

## 2. Technology Stack

### Application & Orchestration
- **Framework:** Custom Google-ADK (Agent Development Kit) for multi-agent graph routing.
- **Backend:** FastAPI (Python 3.13) for high-performance, asynchronous endpoints.
- **LLM Engine:** Google Gemini (via `google-genai` and `google.generativeai`), specifically `gemini-3.5-flash` for high-speed reasoning and generation.

### Database & Memory
- **Primary Database:** PostgreSQL 16
- **Vector Search:** `pgvector` (L2 distance semantic search for user travel memories)
- **Database Driver:** `asyncpg` / `sqlalchemy[asyncio]`
- **Caching & State:** Redis

### External Integrations & APIs
- **Geocoding & Places:** Google Maps API (`googlemaps`)
- **Historical Data:** Wikipedia / Wikidata REST APIs (via `httpx`)
- **Text-to-Speech:** Google Cloud Text-to-Speech API (`google-cloud-texttospeech`)

### CI/CD & Observability
- **Testing:** Pytest with Asyncio support (`pytest`, `pytest-asyncio`)
- **Metrics/Tracing:** OpenTelemetry, Prometheus (`prometheus-client`), Structlog.
- **Deployment:** GitHub Actions (Automated testing and dependency resolution).

---

## 3. Core Functionalities

1. **Hyper-Personalization:** Tailors narratives based on user demographics (e.g., explaining history differently to a 10-year-old vs. a PhD historian).
2. **Agentic RAG Routing:** Dynamically evaluates whether it needs to fetch external data (Wikipedia) or if it can rely on internal LLM knowledge, drastically reducing latency for famous landmarks.
3. **Semantic Memory (Vector RAG):** Translates past user journeys into vector embeddings. When visiting a new location, it semantically searches past trips to draw poetic analogies (e.g., comparing Roman ruins in France to ones they saw in Italy).
4. **Autonomous Self-Critique:** Features a "Reviewer Agent" that critiques generated stories against strict JSON schemas and tone guidelines, forcing rewrites before the user ever sees the text.
5. **Multi-Hop Fallbacks:** Gracefully degrades to "Unknown Location" or regional histories if coordinates are in the middle of nowhere or APIs fail.

---

## 4. The Working Pipeline (Top-to-Bottom)

When a POST request hits the `/generate` endpoint, the `SupervisorAgent` coordinates the following graph of execution:

### Step 1: Parallel Data Gathering (`ParallelRunner`)
Three agents spin up simultaneously to gather context without blocking each other:
*   **Location Agent:** 
    *   Reverse geocodes coordinates via Google Maps.
    *   Uses **Agentic RAG** to ask Gemini: *"Do you have deep knowledge of this place?"*
    *   If **Yes**, it generates facts instantly. If **No**, it hits Wikipedia/Wikidata via `history_tool.py`.
*   **Profile Agent:**
    *   Fetches the user's age, origin, language, and interests.
*   **Memory Agent:**
    *   Fetches the user's raw list of visited places.

### Step 2: Context Aggregation & Semantic Search
*   **Context Aggregator:** Merges the data from Step 1.
*   **Vector Search:** It triggers `semantic_search_journeys` to generate an embedding of the current location and queries `pgvector` to find the most relevant past story from the user's database. This semantic analogy is injected directly into the prompt directives.

### Step 3: The Generation & Critique Loop (`while` loop)
*   **Narrative Agent (Generator):** Writes the first draft of the story using the aggregated context, adhering to strict narrative constraints.
*   **Reviewer Agent (Critic):** Receives the draft and evaluates it for tone, historical accuracy, and engagement. It outputs a JSON critique.
*   **The Loop:** If the critique returns `status: FAILED`, the critique notes are fed *back* into the Narrative Agent, which rewrites the story. This loop continues until `status: PASSED` (or a max retry limit is hit).

### Step 4: Final Delivery
*   **Delivery Agent:** Takes the finalized, critiqued text and packages it for the frontend, ensuring metadata like IDs and timestamps are intact.
*   **Text-to-Speech:** (Optional capability via Google Cloud) Generates a natural-sounding audio file of the story.

---

## 5. Directory Structure & Architecture

```text
ChronoPath/
├── api/
│   └── main.py                 # FastAPI endpoints and telemetry
├── core/
│   ├── db.py                   # Asyncpg connection pooling
│   └── config.py               # Pydantic environment configurations
├── adk/
│   ├── loop.py                 # The Feedback Loop orchestrator logic
│   └── parallel.py             # Parallel processing nodes
├── agents/
│   ├── supervisor.py           # The root coordinator graph
│   ├── location_agent.py       # Agentic RAG & geolocation
│   ├── context_agent.py        # Semantic memory injection
│   ├── narrative_agent.py      # Draft generation
│   ├── reviewer_agent.py       # JSON-based critique
│   └── delivery_agent.py       # Final packaging
├── tools/
│   ├── geo_tool.py             # Google Maps integrations
│   ├── history_tool.py         # Wikipedia scraping
│   └── journey_tool.py         # pgvector embeddings & SQL logic
└── docker-compose.yml          # PostgreSQL + pgvector & Redis setup
```
