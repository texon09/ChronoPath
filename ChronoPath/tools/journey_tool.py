from tenacity import retry, wait_exponential, stop_after_attempt
from core.db import get_pool
from pydantic import BaseModel
import json
import logging

logger = logging.getLogger("chronopath.tools.journey_tool")

class JourneyResult(BaseModel):
    visited_places: list[str]
    recent_story_topics: list[str]

def _get_fallback_journey() -> dict:
    return JourneyResult(
        visited_places=[],
        recent_story_topics=[]
    ).model_dump()

@retry(wait=wait_exponential(multiplier=1, min=2, max=10), stop=stop_after_attempt(3))
async def journey_lookup(user_id) -> dict:
    # Input Validation
    if not user_id or not isinstance(user_id, (str, int)) or str(user_id).strip() == "":
        logger.warning("Invalid user_id provided: %s. Returning empty journey fallback.", user_id)
        return _get_fallback_journey()

    user_id_str = str(user_id).strip()
    pool = await get_pool()

    if pool:
        try:
            async with pool.acquire() as conn:
                row = await conn.fetchrow(
                    "SELECT visited_places, recent_story_topics FROM journeys WHERE user_id = $1", 
                    user_id_str
                )
                if row:
                    visited = row["visited_places"]
                    topics = row["recent_story_topics"]
                    
                    if isinstance(visited, str):
                        try:
                            visited = json.loads(visited)
                        except Exception as e:
                            logger.error("Failed to parse visited_places JSON for user %s: %s", user_id_str, e)
                            visited = []
                    if isinstance(topics, str):
                        try:
                            topics = json.loads(topics)
                        except Exception as e:
                            logger.error("Failed to parse recent_story_topics JSON for user %s: %s", user_id_str, e)
                            topics = []
                        
                    return JourneyResult(
                        visited_places=visited or [],
                        recent_story_topics=topics or []
                    ).model_dump()
                else:
                    logger.info("No journey history record found for user %s.", user_id_str)
        except Exception as e:
            logger.error("Database query exception in journey_lookup for user %s: %s", user_id_str, e)
    else:
        logger.warning("Database connection pool is offline. Journey lookup fallback active for user %s.", user_id_str)

    return _get_fallback_journey()

@retry(wait=wait_exponential(multiplier=1, min=2, max=10), stop=stop_after_attempt(3))
async def save_journey(user_id, place: str, topic: str = None) -> bool:
    if not user_id or not place:
        logger.warning("Invalid user_id or place provided to save_journey. Aborting save.")
        return False

    user_id_str = str(user_id).strip()
    pool = await get_pool()
    if not pool:
        logger.warning("Database connection pool is offline. save_journey failed for user %s.", user_id_str)
        return False

    try:
        async with pool.acquire() as conn:
            async with conn.transaction():
                # 1. Fetch current journeys
                row = await conn.fetchrow(
                    "SELECT visited_places, recent_story_topics FROM journeys WHERE user_id = $1", 
                    user_id_str
                )
                
                visited = []
                topics = []
                
                if row:
                    visited_raw = row["visited_places"]
                    topics_raw = row["recent_story_topics"]
                    
                    if isinstance(visited_raw, str):
                        try: visited = json.loads(visited_raw)
                        except Exception: visited = []
                    elif isinstance(visited_raw, list):
                        visited = visited_raw

                    if isinstance(topics_raw, str):
                        try: topics = json.loads(topics_raw)
                        except Exception: topics = []
                    elif isinstance(topics_raw, list):
                        topics = topics_raw

                # 2. Append new values safely
                if place not in visited:
                    visited.append(place)
                if topic and topic not in topics:
                    topics.append(topic)

                # 3. Upsert
                visited_json = json.dumps(visited)
                topics_json = json.dumps(topics)
                
                await conn.execute(
                    """
                    INSERT INTO journeys (user_id, visited_places, recent_story_topics)
                    VALUES ($1, $2, $3)
                    ON CONFLICT (user_id) DO UPDATE
                    SET visited_places = EXCLUDED.visited_places,
                        recent_story_topics = EXCLUDED.recent_story_topics
                    """,
                    user_id_str, visited_json, topics_json
                )
                logger.info("Successfully updated journey record for user %s.", user_id_str)
                return True
    except Exception as e:
        logger.error("Database transaction error in save_journey for user %s: %s", user_id_str, e)
        return False

@retry(wait=wait_exponential(multiplier=1, min=2, max=10), stop=stop_after_attempt(3))
async def get_last_story(user_id) -> str | None:
    if not user_id:
        return None

    user_id_str = str(user_id).strip()
    pool = await get_pool()
    if not pool:
        return None

    try:
        async with pool.acquire() as conn:
            # Get the last story matching user_id
            row = await conn.fetchrow(
                "SELECT story_text FROM story_history WHERE user_id = $1 ORDER BY id DESC LIMIT 1",
                user_id_str
            )
            if row:
                return row["story_text"]
    except Exception as e:
        logger.error("Database query error in get_last_story for user %s: %s", user_id_str, e)
        # If order by id fails because id doesn't exist, try fallback select
        try:
            async with pool.acquire() as conn:
                row = await conn.fetchrow(
                    "SELECT story_text FROM story_history WHERE user_id = $1 LIMIT 1",
                    user_id_str
                )
                if row:
                    return row["story_text"]
        except Exception:
            pass
    return None
