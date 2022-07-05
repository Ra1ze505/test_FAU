from fastapi import APIRouter
from src.apps.load.api import load
from src.apps.cache.api import cache


api_router = APIRouter()

api_router.include_router(load, prefix="/load", tags=["load"])
api_router.include_router(cache, prefix="/cache", tags=["cache"])
