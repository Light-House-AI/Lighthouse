from sys import prefix
from fastapi.routing import APIRouter
from lighthouse.config import config

from . import auth
from . import projects
from . import monitoring
from . import deployments
from . import models

api_router = APIRouter(prefix=config.API_PREFIX)

api_router.include_router(monitoring.router, tags=["Monitoring"])
api_router.include_router(projects.router, tags=["Projects"])
api_router.include_router(auth.router, tags=["Auth"])
api_router.include_router(deployments.router, tags=["Deployments"])
api_router.include_router(models.router, tags=["Models"])
