import datetime
import json
import aioredis
from aioredis import Redis
from pydantic import BaseModel
from functools import wraps
from enum import Enum

from src.config import settings
from src.apps.cache.schemas import DeleteCacheSchema


class METHODS(Enum):
    GET = 'get'
    POST = 'post'
    PATCH = 'patch'


async def init_redis_pool() -> Redis:
    pool = await aioredis.from_url(f"redis://{settings.REDIS_HOST}", decode_responses=True)
    return pool


def save_cache(method: METHODS):
    def wrap(func):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            pool = await init_redis_pool()
            result = await func(*args, **kwargs)

            if isinstance(result, BaseModel):
                result = result.dict()

            cached_data = {
                'method': method.value,
                'data': result
            }
            await pool.set(f'{datetime.datetime.now()}', json.dumps(cached_data))
            return result

        return wrapper

    return wrap


async def get_cache():
    result = {}
    pool = await init_redis_pool()
    keys = await pool.keys()
    for key in keys:
        value = await pool.get(key)
        result[key] = json.loads(value)
    return result


async def clear_cache_from_redis(data: DeleteCacheSchema):
    pool = await init_redis_pool()
    keys = await pool.keys()
    for key in keys:
        if check_data(datetime.datetime.fromisoformat(key), data):
            await pool.delete(key)


def check_data(current_time: datetime.datetime, times: DeleteCacheSchema) -> bool:
    if times.start_time is None and times.end_time is None:
        return True

    return times.start_time <= current_time <= times.end_time
