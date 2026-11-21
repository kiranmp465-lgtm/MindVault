
import pytest
from fastapi.testclient import TestClient

from app.main import app
from app.services import document_service


@pytest.fixture
def client():
    # Reset temporary document storage before each test
    document_service._documents.clear()
    document_service._next_document_id = 1

    with TestClient(app) as test_client:
        yield test_client

    # Clean up after each test
    document_service._documents.clear()
    document_service._next_document_id = 1


def test_create_document(client):
    response = client.post(
        "/api/v1/documents/",
        json={
            "title": "AI Notes",
            "filename": "ai_notes.pdf"
        }
    )

    assert response.status_code == 201
    assert response.json()["title"] == "AI Notes"
    assert response.json()["id"] == 1


def test_get_all_documents(client):
    client.post(
        "/api/v1/documents/",
        json={
            "title": "AI Notes",
            "filename": "ai_notes.pdf"
        }
    )

    response = client.get("/api/v1/documents/")

    assert response.status_code == 200
    assert len(response.json()) == 1


def test_get_document_by_id(client):
    client.post(
        "/api/v1/documents/",
        json={
            "title": "AI Notes",
            "filename": "ai_notes.pdf"
        }
    )

    response = client.get("/api/v1/documents/1")

    assert response.status_code == 200
    assert response.json()["id"] == 1


def test_get_missing_document(client):
    response = client.get("/api/v1/documents/999")

    assert response.status_code == 404


def test_delete_document(client):
    client.post(
        "/api/v1/documents/",
        json={
            "title": "AI Notes",
            "filename": "ai_notes.pdf"
        }
    )

    response = client.delete("/api/v1/documents/1")

    assert response.status_code == 204


def test_delete_missing_document(client):
    response = client.delete("/api/v1/documents/999")

    assert response.status_code == 404


def test_create_document_with_invalid_data(client):
    response = client.post(
        "/api/v1/documents/",
        json={
            "title": "",
            "filename": "ai_notes.pdf"
        }
    )

    assert response.status_code == 422
