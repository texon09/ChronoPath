from tenacity import retry, wait_exponential, stop_after_attempt
from core.db import get_pool
from pydantic import BaseModel
import json

class JourneyResult(BaseModel):
    visited_places: list[str]
    recent_story_topics: list[str]

@retry(wait=wait_exponential(multiplier=1, min=2, max=10), stop=stop_after_attempt(3))
async def journey_lookup(user_id) -> dict:
    pool = await get_pool()
    if pool:
        try:
            async with pool.acquire() as conn:
                row = await conn.fetchrow(
                    "SELECT visited_places, recent_story_topics FROM journeys WHERE user_id = $1", 
                    str(user_id)
                )
                if row:
                    visited = row["visited_places"]
                    topics = row["recent_story_topics"]
                    
                    # Handle potential stringified JSON
                    if isinstance(visited, str):
                        try: visited = json.loads(visited)
                        except Exception: visited = []
                    if isinstance(topics, str):
                        try: topics = json.loads(topics)
                        except Exception: topics = []
                        
                    return JourneyResult(
                        visited_places=visited or [],
                        recent_story_topics=topics or []
                    ).model_dump()
        except Exception:
            pass

    return JourneyResult(
        visited_places=[],
        recent_story_topics=[]
    ).model_dump()
