from fastapi import APIRouter, Depends

from src.apps.load.schemas import ResponseLoadSchema, LoadSchema
from src.apps.load.service import LoadService
from src.apps.redis import METHODS, save_cache

load = APIRouter()


@load.get('/', response_model=ResponseLoadSchema)
@save_cache(METHODS.GET)
async def all_load():
    return await LoadService().get_all_usage()


@load.post('/', response_model=ResponseLoadSchema)
@save_cache(METHODS.POST)
async def any_load(data: LoadSchema):
    return await LoadService().get_any_load(data)

