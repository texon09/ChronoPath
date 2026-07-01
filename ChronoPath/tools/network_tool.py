import httpx
import time
from tenacity import retry, wait_exponential, stop_after_attempt
from pydantic import BaseModel

class NetworkResult(BaseModel):
    quality: str
    latency_ms: float

@retry(wait=wait_exponential(multiplier=1, min=2, max=10), stop=stop_after_attempt(3))
async def network_quality_check(network_quality=None) -> dict:
    if network_quality and network_quality.lower() in {"good", "medium", "low"}:
        return NetworkResult(quality=network_quality.lower(), latency_ms=0.0).model_dump()
        
    start = time.perf_counter()
    async with httpx.AsyncClient(timeout=3.0) as client:
        try:
            await client.head("https://www.google.com")
            latency_ms = (time.perf_counter() - start) * 1000
            
            if latency_ms < 200:
                quality = "good"
            elif latency_ms < 600:
                quality = "medium"
            else:
                quality = "low"
                
            return NetworkResult(quality=quality, latency_ms=latency_ms).model_dump()
        except Exception:
            pass

    return NetworkResult(quality="low", latency_ms=9999.0).model_dump()
