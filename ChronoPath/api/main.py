import os
import time
import structlog
from fastapi import FastAPI, HTTPException, Response, Depends
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from fastapi.security import OAuth2PasswordRequestForm
from prometheus_client import generate_latest, CONTENT_TYPE_LATEST, Counter, Histogram
from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor

from config import get_settings
from agents.supervisor import SupervisorAgent
from schemas import GenerateRequest, GenerateResponse
from core.auth import get_current_user, verify_password, create_access_token, load_users, save_users, get_password_hash

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

import os
os.makedirs("media", exist_ok=True)
app.mount("/media", StaticFiles(directory="media"), name="media")

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

from pydantic import BaseModel

class RegisterRequest(BaseModel):
    username: str
    password: str

@app.post("/api/auth/register")
async def register(req: RegisterRequest):
    username = req.username.strip()
    password = req.password.strip()
    if len(username) < 3 or len(password) < 4:
        raise HTTPException(
            status_code=400,
            detail="Explorer name must be >= 3 chars, Keyphrase must be >= 4 chars"
        )
    users = load_users()
    if username in users:
        raise HTTPException(
            status_code=400,
            detail="Explorer name is already registered"
        )
    
    users[username] = {
        "username": username,
        "hashed_password": get_password_hash(password),
        "role": "explorer"
    }
    save_users(users)
    
    access_token = create_access_token(data={"sub": username})
    return {"access_token": access_token, "token_type": "bearer", "username": username}

@app.post("/api/auth/login")
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    username = form_data.username
    password = form_data.password
    users = load_users()
    user = users.get(username)
    if not user or not verify_password(password, user["hashed_password"]):
        raise HTTPException(
            status_code=401,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token = create_access_token(data={"sub": username})
    return {"access_token": access_token, "token_type": "bearer", "username": username}

@app.post("/generate", response_model=GenerateResponse)
async def generate(request: GenerateRequest, current_user: str = Depends(get_current_user)):
    logger.info("generate_request_started", request_id=request.request_id if hasattr(request, 'request_id') else "unknown")
    try:
        payload = request.to_agent_payload()
        # Enforce authenticated user context
        payload["user_id"] = current_user
        
        res = await supervisor.execute(payload)
        logger.info("generate_request_completed", place=res.place.name)
        return res
    except ValueError as exc:
        logger.error("generate_request_failed", error=str(exc))
        raise HTTPException(status_code=502, detail=str(exc)) from exc

@app.get("/")
async def get_index():
    index_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "static", "index.html")
    if os.path.exists(index_path):
        return FileResponse(index_path)
    if os.path.exists("static/index.html"):
        return FileResponse("static/index.html")
    raise HTTPException(status_code=404, detail="Frontend index.html not found.")

@app.get("/static/{path:path}")
async def get_static(path: str):
    base_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), "static")
    file_path = os.path.join(base_dir, path)
    if os.path.exists(file_path):
        return FileResponse(file_path)
    
    fallback_path = os.path.join("static", path)
    if os.path.exists(fallback_path):
        return FileResponse(fallback_path)
        
    raise HTTPException(status_code=404, detail="File not found.")
