# API Reference

ChronoPath AI uses FastAPI to expose an asynchronous HTTP server. All endpoints (except health and metrics) require Firebase JWT authentication via the `Authorization: Bearer <token>` header.

## Primary Endpoints

### 1. `POST /generate`
This is the core agentic generation endpoint. It delegates to the Supervisor Agent.

**Headers**:
- `Authorization`: `Bearer <Firebase_JWT>`

**Request Body** (`GenerateRequest` Schema):
```json
{
  "request_id": "string (UUID)",
  "lat": "float (e.g., 40.7128)",
  "lng": "float (e.g., -74.0060)",
  "age": "int (e.g., 25)",
  "origin": "string (e.g., 'London, UK')",
  "background": "string (e.g., 'Architect')"
}
```

**Response Body** (`GenerateResponse` Schema):
```json
{
  "story": "string (The generated historical narrative)",
  "place": {
    "name": "string",
    "distance_km": "float",
    "themes": ["string"]
  },
  "media": [
    {
      "url": "string (URL to the generated image)",
      "caption": "string (Description of the image)"
    }
  ],
  "safety": {
    "approved": "boolean",
    "issues": ["string"]
  }
}
```

## Observability Endpoints

### 2. `GET /health`
Returns the status of the API server. No authentication required.
**Response**:
```json
{
  "status": "ok",
  "app": "ChronoPath AI",
  "environment": "production"
}
```

### 3. `GET /metrics`
Exposes Prometheus metrics for the application. No authentication required.
**Response Body**: `text/plain`
Contains standard Prometheus metrics such as:
- `request_count_total`
- `request_latency_seconds`
- Agent invocation metrics.
