
from fastapi import APIRouter

# Main API router for version 1
api_router = APIRouter()


@api_router.get("/status")
def api_status():
    return {
        "message": "MindVault API is working",
        "version": "v1"
    }
