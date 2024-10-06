from contextlib import asynccontextmanager
import json
from typing import Any

from redis.asyncio import Redis, RedisError

from app.config.cache import redis_client


async def append_to_list(key: str, value: dict[str, Any] | str, client: Redis = redis_client) -> None:
    """Serializes and appends the given value to the list."""

    if isinstance(value, dict):
        serialized_value = json.dumps(value)
    else:
        serialized_value = value

    try:
        await client.lpush(key, serialized_value)  # type: ignore
    except RedisError as exc:
        print(f"error appending to cached list: {exc}")
        raise


async def set_expiry(key: str, expiry_seconds: int, client: Redis = redis_client) -> None:
    """Sets expiry time for the given key."""

    try:
        await client.expire(key, expiry_seconds)
    except RedisError as exc:
        print(f"error setting key expiry: {exc}")
        raise


async def get_value(key: str, client: Redis = redis_client) -> Any:
    """Gets cached value given apt key."""

    try:
        value = await client.get(key)
    except RedisError as exc:
        print(f"error getting cached value: {exc}")
        raise

    return value


async def get_list_values(key: str, client: Redis = redis_client) -> list:
    """Gets list values given apt key."""

    try:
        values = await client.lrange(key, 0, -1)  # type: ignore
    except RedisError as exc:
        print(f"error getting cached value: {exc}")
        raise

    return values


async def get_latest_list_value(key: str, client: Redis = redis_client) -> Any:
    """Gets latest list value given apt key."""

    try:
        value = await client.blpop([key], 0)  # type: ignore
    except RedisError as exc:
        print(f"error getting latest cached list value for list '{key}': {exc}")
        raise

    return value


@asynccontextmanager
async def subscribe_to_channel(namespace: str, pattern: bool = True, client: Redis = redis_client):
    """Initializes a new pub-sub connection on the given channel namespace, using pattern-based or literal string-matching
    subscription."""

    pubsub = client.pubsub()
    try:
        if pattern:
            await pubsub.psubscribe(namespace)
        else:
            await pubsub.subscribe(namespace)

        yield pubsub
    except RedisError as exc:
        print(f"error subscribing to pubsub namespace '{namespace}': {exc}")
        raise
    finally:
        await pubsub.unsubscribe()
