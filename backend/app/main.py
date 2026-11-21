
import logging

from fastapi import FastAPI

from app.api.v1.router import api_router
from app.core.config import settings
from app.core.exceptions import global_exception_handler
from app.core.logging_config import setup_logging


# Configure application logging
setup_logging()
logger = logging.getLogger(__name__)


app = FastAPI(
    title=settings.APP_NAME,
    description="Personal AI Second Brain - Backend",
    version=settings.APP_VERSION,
)


# Register global exception handler
app.add_exception_handler(
    Exception,
    global_exception_handler
)


# Register API version 1 routes
app.include_router(
    api_router,
    prefix=settings.API_V1_PREFIX
)


@app.get("/")
def home():
    logger.info("Home endpoint accessed")

    return {
        "message": "Welcome to MindVault!",
        "status": "Backend is running successfully"
    }


@app.get("/health")
def health_check():
    return {
        "status": "healthy"
    }
