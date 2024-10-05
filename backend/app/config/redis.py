from redis.asyncio import Redis

from app.config.config import REDIS_HOST, REDIS_PASSWORD, REDIS_PORT


redis_url = f"redis://:{REDIS_PASSWORD}@{REDIS_HOST}:{REDIS_PORT}/0"

redis_client = Redis.from_url(redis_url)
