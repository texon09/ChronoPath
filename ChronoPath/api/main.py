from fastapi import FastAPI, HTTPException

from config import get_settings
from agents.supervisor import SupervisorAgent
from schemas import GenerateRequest, GenerateResponse


settings = get_settings()
app = FastAPI(title=settings.app_name)
supervisor = SupervisorAgent()


@app.get("/health")
async def health():
    return {
        "status": "ok",
        "app": settings.app_name,
        "environment": settings.environment,
    }


@app.post("/generate", response_model=GenerateResponse)
async def generate(request: GenerateRequest):
    try:
        return await supervisor.execute(request.to_agent_payload())
    except ValueError as exc:
        raise HTTPException(status_code=502, detail=str(exc)) from exc
