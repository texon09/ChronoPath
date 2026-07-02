import json
import logging
from typing import Any, Dict, Optional
from memory.redis_client import RedisClient
from core.db import get_pool

logger = logging.getLogger("chronopath.memory.memory_manager")

class MemoryManager:
    def __init__(self):
        self.redis = RedisClient()

    async def save_session(self, user_id: str, session_data: Dict[str, Any], ttl: int = 1800) -> bool:
        key = f"session:{user_id}"
        try:
            val = json.dumps(session_data)
            return await self.redis.setex(key, ttl, val)
        except Exception as e:
            logger.error("Failed to save session for user %s: %s", user_id, e)
            return False

    async def load_session(self, user_id: str) -> Optional[Dict[str, Any]]:
        key = f"session:{user_id}"
        try:
            val = await self.redis.get(key)
            if val:
                return json.loads(val)
        except Exception as e:
            logger.error("Failed to load session for user %s: %s", user_id, e)
        return None

    async def save_story(self, user_id: str, story_data: Dict[str, Any] | str, ttl: int = 1800) -> bool:
        key = f"story:{user_id}"
        try:
            if isinstance(story_data, str):
                story_data = {"story": story_data}
            val = json.dumps(story_data)
            return await self.redis.setex(key, ttl, val)
        except Exception as e:
            logger.error("Failed to save story for user %s: %s", user_id, e)
            return False

    async def load_story(self, user_id: str) -> Optional[Dict[str, Any]]:
        key = f"story:{user_id}"
        try:
            val = await self.redis.get(key)
            if val:
                return json.loads(val)
        except Exception as e:
            logger.error("Failed to load story for user %s: %s", user_id, e)
        return None

    async def save_journey(self, user_id: str, place: str, request_id: Optional[str] = None, story_text: Optional[str] = None) -> bool:
        success = True
        
        # 1. Short-term Cache (Redis List)
        try:
            key = f"places:{user_id}"
            await self.redis.lpush(key, place)
            await self.redis.ltrim(key, 0, 9)
            await self.redis.expire(key, 1800)
        except Exception as e:
            logger.error("Failed to save journey to Redis cache for user %s: %s", user_id, e)
            success = False

        # 2. Long-term DB (PostgreSQL)
        pool = await get_pool()
        if pool:
            try:
                async with pool.acquire() as conn:
                    async with conn.transaction():
                        await conn.execute(
                            "INSERT INTO journey_events (user_id, place, event_time) VALUES ($1, $2, NOW())",
                            str(user_id), place
                        )
                        if request_id and story_text:
                            await conn.execute(
                                "INSERT INTO story_history (user_id, request_id, story_text) VALUES ($1, $2, $3)",
                                str(user_id), request_id, story_text
                            )
            except Exception as e:
                logger.error("Failed to save journey to database for user %s: %s", user_id, e)
                success = False
        else:
            logger.warning("Database connection pool is not available; long-term journey not stored.")
            success = False

        return success

    async def invalidate_session(self, user_id: str) -> bool:
        success = True
        try:
            r1 = await self.redis.delete(f"session:{user_id}")
            r2 = await self.redis.delete(f"story:{user_id}")
            success = r1 and r2
        except Exception as e:
            logger.error("Failed to invalidate session for user %s: %s", user_id, e)
            success = False
        return success
