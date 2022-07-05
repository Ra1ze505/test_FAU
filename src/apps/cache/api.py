from fastapi import APIRouter

from src.apps.cache.schemas import ResponseCacheSchema, DeleteCacheSchema
from src.apps.redis import get_cache, clear_cache_from_redis


cache = APIRouter()


@cache.get('/cache', response_model=ResponseCacheSchema)
async def view_cache():
    result = await get_cache()
    return {'cache': result}


@cache.post('/cache')
async def delete_cache(data: DeleteCacheSchema):
    await clear_cache_from_redis(data)
    return {'success': True}
