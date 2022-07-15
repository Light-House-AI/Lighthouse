from fastapi.routing import APIRouter
from lighthouse.config import config

from . import auth
from . import users
from . import projects
from . import health
from . import deployments
from . import models
from . import cleaned_datasets
from . import raw_datasets

api_router = APIRouter(prefix=config.API_PREFIX)

api_router.include_router(health.router, tags=["Health"])
api_router.include_router(auth.router, tags=["Auth"])
api_router.include_router(users.router, tags=["Users"])
api_router.include_router(projects.router, tags=["Projects"])
api_router.include_router(raw_datasets.router, tags=["Raw Datasets"])
api_router.include_router(cleaned_datasets.router, tags=["Cleaned Datasets"])
api_router.include_router(models.router, tags=["Models"])
api_router.include_router(deployments.router, tags=["Deployments"])
