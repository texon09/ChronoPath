from tenacity import retry, wait_exponential, stop_after_attempt
from core.db import get_pool
from pydantic import BaseModel
import json
import logging

logger = logging.getLogger("chronopath.tools.profile_tool")

class ProfileResult(BaseModel):
    language: str
    interests: list[str]
    tone: str

def _get_fallback_profile() -> dict:
    return ProfileResult(
        language="English",
        interests=["history"],
        tone="clear"
    ).model_dump()

@retry(wait=wait_exponential(multiplier=1, min=2, max=10), stop=stop_after_attempt(3))
async def profile_lookup(user_id) -> dict:
    # Input Validation
    if not user_id or not isinstance(user_id, (str, int)) or str(user_id).strip() == "":
        logger.warning("Invalid user_id provided: %s. Returning fallback profile.", user_id)
        return _get_fallback_profile()

    user_id_str = str(user_id).strip()
    pool = await get_pool()
    
    if pool:
        try:
            async with pool.acquire() as conn:
                row = await conn.fetchrow(
                    "SELECT language, interests, tone FROM profiles WHERE user_id = $1", 
                    user_id_str
                )
                if row:
                    interests = row["interests"]
                    if isinstance(interests, str):
                        try:
                            interests = json.loads(interests)
                        except Exception as e:
                            logger.error(
                                "Failed to parse interests JSON for user %s: %s", 
                                user_id_str, e
                            )
                            interests = [interests]
                    return ProfileResult(
                        language=row["language"] or "English",
                        interests=interests or [],
                        tone=row["tone"] or "clear"
                    ).model_dump()
                else:
                    logger.info("No profile record found for user %s. Using default profile.", user_id_str)
        except Exception as e:
            logger.error("Database query exception for user %s: %s", user_id_str, e)
    else:
        logger.warning("Database connection pool is offline. Fallback active for user %s.", user_id_str)

    return _get_fallback_profile()
