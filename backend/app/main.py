
from fastapi import FastAPI

# Create the FastAPI application
app = FastAPI(
    title="MindVault API",
    description="Personal AI Second Brain - Backend",
    version="1.0.0"
)

# Root endpoint
@app.get("/")
def home():
    return {
        "message": "Welcome to MindVault!",
        "status": "Backend is running successfully"
    }


# Health check endpoint
@app.get("/health")
def health_check():
    return {
        "status": "healthy"
    }
