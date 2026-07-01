import structlog
from fastapi import FastAPI, HTTPException, Response
from prometheus_client import generate_latest, CONTENT_TYPE_LATEST, Counter, Histogram
from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor
import time

from config import get_settings
from agents.supervisor import SupervisorAgent
from schemas import GenerateRequest, GenerateResponse

# Configure structlog
structlog.configure(
    processors=[
        structlog.stdlib.add_log_level,
        structlog.processors.TimeStamper(fmt="iso"),
        structlog.processors.JSONRenderer()
    ]
)
logger = structlog.get_logger()

# Metrics
REQUEST_COUNT = Counter('request_count', 'App Request Count', ['method', 'endpoint', 'http_status'])
REQUEST_LATENCY = Histogram('request_latency_seconds', 'Request latency', ['endpoint'])

settings = get_settings()
app = FastAPI(title=settings.app_name)
supervisor = SupervisorAgent()

FastAPIInstrumentor.instrument_app(app)

@app.middleware("http")
async def metrics_middleware(request, call_next):
    start_time = time.perf_counter()
    response = await call_next(request)
    latency = time.perf_counter() - start_time
    
    REQUEST_COUNT.labels(request.method, request.url.path, response.status_code).inc()
    REQUEST_LATENCY.labels(request.url.path).observe(latency)
    
    return response

@app.get("/health")
async def health():
    return {
        "status": "ok",
        "app": settings.app_name,
        "environment": settings.environment,
    }

@app.get("/metrics")
async def metrics():
    return Response(generate_latest(), media_type=CONTENT_TYPE_LATEST)

@app.post("/generate", response_model=GenerateResponse)
async def generate(request: GenerateRequest):
    logger.info("generate_request_started", request_id=request.request_id if hasattr(request, 'request_id') else "unknown")
    try:
        res = await supervisor.execute(request.to_agent_payload())
        logger.info("generate_request_completed", place=res.place.name)
        return res
    except ValueError as exc:
        logger.error("generate_request_failed", error=str(exc))
        raise HTTPException(status_code=502, detail=str(exc)) from exc
