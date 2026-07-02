import logging
import json
from typing import Any
from core.cache import get_redis

logger = logging.getLogger("chronopath.memory.redis_client")

class RedisClient:
    def __init__(self):
        self._client = None

    async def get_client(self):
        if self._client is None:
            self._client = await get_redis()
        return self._client

    async def get(self, key: str) -> str | None:
        try:
            client = await self.get_client()
            return await client.get(key)
        except Exception as e:
            logger.error("Redis get failed for key %s: %s", key, e)
            return None

    async def setex(self, key: str, ttl: int, value: str) -> bool:
        try:
            client = await self.get_client()
            await client.set(key, value, ex=ttl)
            return True
        except Exception as e:
            logger.error("Redis setex failed for key %s: %s", key, e)
            return False

    async def delete(self, key: str) -> bool:
        try:
            client = await self.get_client()
            await client.delete(key)
            return True
        except Exception as e:
            logger.error("Redis delete failed for key %s: %s", key, e)
            return False

    async def lpush(self, key: str, value: str) -> int | None:
        try:
            client = await self.get_client()
            return await client.lpush(key, value)
        except Exception as e:
            logger.error("Redis lpush failed for key %s: %s", key, e)
            return None

    async def ltrim(self, key: str, start: int, stop: int) -> bool:
        try:
            client = await self.get_client()
            await client.ltrim(key, start, stop)
            return True
        except Exception as e:
            logger.error("Redis ltrim failed for key %s: %s", key, e)
            return False

    async def expire(self, key: str, ttl: int) -> bool:
        try:
            client = await self.get_client()
            await client.expire(key, ttl)
            return True
        except Exception as e:
            logger.error("Redis expire failed for key %s: %s", key, e)
            return False
