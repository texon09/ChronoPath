# ChronoPath AI

ChronoPath AI is a production-oriented multimodal historical storytelling system.
The target architecture uses Google ADK agents, Gemini, Google Maps, Wikipedia,
Wikidata, OpenStreetMap, PostgreSQL with pgvector, Redis, Google Cloud Storage,
FastAPI, Docker, Cloud Run, and OpenTelemetry.

## Milestone 2: Executable Agent Pipeline

The backend now exposes an executable `/generate` flow. FastAPI validates the
request, hands it to the supervisor, and the supervisor coordinates the agents.

Included now:

- FastAPI application shell
- Typed request and response contracts
- Environment-driven configuration
- Async base agent interface
- Session state
- Async supervisor orchestration
- `/generate` endpoint wired to the agent pipeline
- Dockerfile and docker-compose services
- CI workflow
- Contract tests

## API Contract

`POST /generate`

Request:

```json
{
  "user_id": "1",
  "latitude": 18.5196,
  "longitude": 73.8553
}
```

Response:

```json
{
  "request_id": "",
  "place": "Shaniwar Wada",
  "text": {
    "title": "Shaniwar Wada - Peshwa Era",
    "story": "..."
  },
  "safe": true
}
```

## Local Commands

```bash
python -m unittest discover -s tests
uvicorn api.main:app --reload
docker compose up --build
```

Example:

```bash
curl -X POST http://localhost:8000/generate \
  -H "Content-Type: application/json" \
  -d "{\"user_id\":\"1\",\"latitude\":18.5196,\"longitude\":73.8553}"
```

## Configuration

Copy `.env.example` to `.env` and provide real credentials before enabling
production integrations.
