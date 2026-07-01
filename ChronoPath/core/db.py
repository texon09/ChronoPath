import asyncpg
from core.config import settings

_pool = None

async def get_pool():
    global _pool
    if _pool is None:
        url = settings.database_url.replace("+asyncpg", "")
        try:
            _pool = await asyncpg.create_pool(url)
        except Exception:
            return None
    return _pool

async def close_pool():
    global _pool
    if _pool:
        await _pool.close()
        _pool = None
