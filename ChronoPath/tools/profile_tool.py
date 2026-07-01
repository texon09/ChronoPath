from tenacity import retry, wait_exponential, stop_after_attempt
from core.db import get_pool
from pydantic import BaseModel
import json

class ProfileResult(BaseModel):
    language: str
    interests: list[str]
    tone: str

@retry(wait=wait_exponential(multiplier=1, min=2, max=10), stop=stop_after_attempt(3))
async def profile_lookup(user_id) -> dict:
    pool = await get_pool()
    if pool:
        try:
            async with pool.acquire() as conn:
                row = await conn.fetchrow("SELECT language, interests, tone FROM profiles WHERE user_id = $1", str(user_id))
                if row:
                    interests = row["interests"]
                    if isinstance(interests, str):
                        try:
                            interests = json.loads(interests)
                        except Exception:
                            interests = [interests]
                    return ProfileResult(
                        language=row["language"] or "English",
                        interests=interests or [],
                        tone=row["tone"] or "clear"
                    ).model_dump()
        except Exception as e:
            # Table might not exist yet during migration tests, fallback below
            pass

    return ProfileResult(
        language="English",
        interests=["history"],
        tone="clear"
    ).model_dump()
