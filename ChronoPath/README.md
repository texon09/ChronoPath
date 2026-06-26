# ChronoPath AI

ChronoPath AI is a production-oriented multimodal historical storytelling system.
The target architecture uses Google ADK agents, Gemini, Google Maps, Wikipedia,
Wikidata, OpenStreetMap, PostgreSQL with pgvector, Redis, Google Cloud Storage,
FastAPI, Docker, Cloud Run, and OpenTelemetry.

## Milestone 1: Production Foundation

This milestone establishes the backend foundation without pretending that real
external integrations are already wired.

Included now:

- FastAPI application shell
- Typed request and response contracts
- Environment-driven configuration
- Async base agent interface
- Dockerfile and docker-compose services
- CI workflow
- Contract tests

## API Contract

`POST /generate`

Request:

```json
{
  "user_id": "user-1",
  "lat": 18.5196,
  "lng": 73.8553
}
```

Response:

```json
{
  "request_id": "",
  "place": {
    "id": "",
    "name": ""
  },
  "text": {
    "title": "",
    "story": "",
    "facts": []
  },
  "audio": {
    "url": "",
    "duration": 0
  },
  "visual": {
    "url": ""
  },
  "metadata": {
    "latency_ms": 0,
    "cached": false
  }
}
```

## Local Commands

```bash
python -m unittest discover -s tests
uvicorn app:app --reload
docker compose up --build
```

## Configuration

Copy `.env.example` to `.env` and provide real credentials before enabling
production integrations.
