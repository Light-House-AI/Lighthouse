from fastapi.routing import APIRouter
from . import monitoring

api_router = APIRouter()
api_router.include_router(monitoring.router, tags=["monitoring"])
