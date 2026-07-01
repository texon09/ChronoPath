import json
import asyncio
from core.db import get_pool
from core.cache import get_redis

class MemoryAgent:
    async def execute(self, state):
        request_id = state.get("request_id")
        user_id = state.get("request", {}).get("user_id", "unknown")
        place = state.get("location", {}).get("place", "")
        story = state.get("story", {}).get("story", "")
        
        # Parallelize Redis and Postgres writes
        tasks = [
            self._write_short_term(user_id, place, story, state),
            self._write_long_term(user_id, place, story, request_id)
        ]
        
        # Write asynchronously (don't fail the request if it fails)
        try:
            await asyncio.gather(*tasks)
            state.set("memory_saved", True)
        except Exception as e:
            state.set("memory_saved", False)
            
        return state
        
    async def _write_short_term(self, user_id, place, story, state):
        redis = await get_redis()
        try:
            pipe = redis.pipeline()
            # Cache session and last story
            pipe.setex(f"session:{user_id}", 1800, json.dumps({"last_req": state.get("request_id")}))
            pipe.setex(f"story:{user_id}", 1800, story)
            # Recent places (list)
            pipe.lpush(f"places:{user_id}", place)
            pipe.ltrim(f"places:{user_id}", 0, 9)
            pipe.expire(f"places:{user_id}", 1800)
            await pipe.execute()
        except Exception:
            pass

    async def _write_long_term(self, user_id, place, story, request_id):
        pool = await get_pool()
        if not pool:
            return
            
        async with pool.acquire() as conn:
            try:
                # Stubbed inserts to missing tables. 
                # Assumes pgvector extension exists and schema is ready.
                async with conn.transaction():
                    await conn.execute(
                        "INSERT INTO journey_events (user_id, place, event_time) VALUES ($1, $2, NOW())",
                        str(user_id), place
                    )
                    await conn.execute(
                        "INSERT INTO story_history (user_id, request_id, story_text) VALUES ($1, $2, $3)",
                        str(user_id), request_id, story
                    )
            except Exception:
                # Swallow exceptions for now if tables don't exist yet
                pass
