
from fastapi import APIRouter

from app.api.v1.endpoints import documents, status


# Main API router for version 1
api_router = APIRouter()

# Register individual endpoint routers
api_router.include_router(status.router)
api_router.include_router(documents.router)
