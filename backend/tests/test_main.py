
from fastapi.testclient import TestClient

from app.main import app


# Create a test client
client = TestClient(app, raise_server_exceptions=False)


def test_home_endpoint():
    response = client.get("/")

    assert response.status_code == 200
    assert response.json()["message"] == "Welcome to MindVault!"


def test_health_endpoint():
    response = client.get("/health")

    assert response.status_code == 200
    assert response.json()["status"] == "healthy"


def test_api_status_endpoint():
    response = client.get("/api/v1/status")

    assert response.status_code == 200
    assert response.json()["message"] == "MindVault API is working"
    assert response.json()["version"] == "v1"
