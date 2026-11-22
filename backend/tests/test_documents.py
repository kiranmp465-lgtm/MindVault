import pymupdf
import pytest
from fastapi.testclient import TestClient

from app.main import app
from app.services import document_service

from unittest.mock import patch

from app.services.file_service import UPLOAD_DIR



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

def test_uploaded_file_deleted_when_extraction_fails(client):
    """Uploaded PDF should be deleted if text extraction fails."""

    # Generate a structurally valid PDF
    pdf = pymupdf.open()
    page = pdf.new_page()
    page.insert_text((72, 72), "MindVault cleanup test")

    fake_pdf = pdf.tobytes()
    pdf.close()

    with patch(
        "app.api.v1.endpoints.documents.extract_text_from_pdf",
        side_effect=ValueError("Simulated extraction failure")
    ):
        response = client.post(
            "/api/v1/documents/upload",
            files={
                "file": (
                    "cleanup_test.pdf",
                    fake_pdf,
                    "application/pdf"
                )
            }
        )

    assert response.status_code == 422

    # Find any remaining file with the test filename's generated storage ID.
    # The API uses UUID filenames, so inspect the upload directory.
    assert not any(
        path.is_file()
        and path.stat().st_size == len(fake_pdf)
        and path.read_bytes() == fake_pdf
        for path in UPLOAD_DIR.iterdir()
    )
