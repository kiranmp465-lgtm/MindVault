
from datetime import datetime, timezone

from app.schemas.document import DocumentCreate, DocumentResponse


# Temporary in-memory document storage
_documents: dict[int, DocumentResponse] = {}

# Automatically generated document IDs
_next_document_id = 1


def create_document(document: DocumentCreate) -> DocumentResponse:
    global _next_document_id

    new_document = DocumentResponse(
        id=_next_document_id,
        title=document.title,
        filename=document.filename,
        status="created",
        created_at=datetime.now(timezone.utc),
    )

    _documents[_next_document_id] = new_document
    _next_document_id += 1

    return new_document


def get_all_documents() -> list[DocumentResponse]:
    return list(_documents.values())


def get_document_by_id(document_id: int) -> DocumentResponse | None:
    return _documents.get(document_id)


def delete_document(document_id: int) -> bool:
    if document_id not in _documents:
        return False

    del _documents[document_id]
    return True
