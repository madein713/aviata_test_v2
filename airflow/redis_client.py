from dataclasses import dataclass
from typing import Optional
import redis


@dataclass
class RedisClient:
    port: Optional[int] = 6379
    host: str = 'redis'
    _redis: redis.Redis = redis.Redis(host)

    def set(self, key, value):
        self._redis.set(key, value)

    def get(self, key):
        return self._redis.get(key)


redis_client = RedisClient()
