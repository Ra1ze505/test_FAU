from fastapi import FastAPI

from src.apps import routers
from src.config import settings


app = FastAPI()


app.include_router(routers.api_router, prefix=settings.API_V1_STR)