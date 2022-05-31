from sys import prefix
from fastapi.routing import APIRouter
from lighthouse.config import config

from . import monitoring
from . import projects
from . import auth

api_router = APIRouter(prefix=config.API_PREFIX)

api_router.include_router(monitoring.router, tags=["monitoring"])
api_router.include_router(projects.router, tags=["projects"])
api_router.include_router(auth.router, tags=["auth"])