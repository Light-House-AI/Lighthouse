from fastapi import FastAPI
from fastapi.responses import UJSONResponse
from fastapi.middleware.cors import CORSMiddleware
import uvicorn

from .routers import api_router
from .lifetime import shutdown, startup
from .metadata import METADATA

from lighthouse.config import config


def get_app() -> FastAPI:
    """
    Get FastAPI application.
    This is the main constructor of an application.
    """
    app = FastAPI(
        **METADATA,
        docs_url=config.API_PREFIX + "/docs",
        redoc_url=config.API_PREFIX + "/redoc",
        openapi_url=config.API_PREFIX + "/openapi.json",
        default_response_class=UJSONResponse,
    )

    # setup lifecycle hooks
    app.on_event("startup")(startup(app))
    app.on_event("shutdown")(shutdown(app))

    # add CORS middleware
    add_cors_middleware(app)

    # add routers
    app.include_router(router=api_router)
    return app


def add_cors_middleware(app):
    """
    Add CORS middleware to the application.
    """
    app.add_middleware(
        CORSMiddleware,
        allow_origins=config.CORS_ORIGIN,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )


def get_uvicorn_log_config():
    log_config = uvicorn.config.LOGGING_CONFIG.copy()

    log_config["formatters"]["access"][
        "fmt"] = "%(asctime)s - %(levelname)s - %(message)s"

    log_config["formatters"]["default"][
        "fmt"] = "%(asctime)s - %(levelname)s - %(message)s"

    return log_config


def run_app():
    """
    Entrypoint of the application.
    """

    uvicorn.run(
        "lighthouse.ml_projects.api.application:get_app",
        workers=config.WORKERS_COUNT,
        host=config.HOST,
        port=config.PORT,
        reload=config.RELOAD,
        factory=True,
    )
