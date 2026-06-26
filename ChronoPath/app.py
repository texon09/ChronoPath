from fastapi import FastAPI, HTTPException

from config import get_settings
from schemas import GenerateRequest, GenerateResponse


settings = get_settings()
app = FastAPI(title=settings.app_name)


@app.get("/health")
async def health():
    return {
        "status": "ok",
        "app": settings.app_name,
        "environment": settings.environment,
    }


@app.post("/generate", response_model=GenerateResponse)
async def generate(request: GenerateRequest):
    raise HTTPException(
        status_code=503,
        detail=(
            "Production agent pipeline is not wired yet. Milestone 1 exposes "
            "validated contracts only."
        ),
    )
