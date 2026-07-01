import redis.asyncio as redis
from core.config import settings

_redis_pool = None

async def get_redis():
    global _redis_pool
    if _redis_pool is None:
        _redis_pool = redis.from_url(settings.redis_url, decode_responses=True)
    return _redis_pool

async def close_redis():
    global _redis_pool
    if _redis_pool:
        await _redis_pool.aclose()
        _redis_pool = None
