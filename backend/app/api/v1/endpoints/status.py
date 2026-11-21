from fastapi import APIRouter


router = APIRouter()


@router.get("/status")
def api_status():
    return {
        "message": "MindVault API is working",
        "version": "v1"
    }