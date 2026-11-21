
from fastapi import APIRouter, HTTPException, status

from app.schemas.document import DocumentCreate, DocumentResponse
from app.services import document_service


router = APIRouter(
    prefix="/documents",
    tags=["Documents"]
)


@router.post(
    "/",
    response_model=DocumentResponse,
    status_code=status.HTTP_201_CREATED
)
def create_document(document: DocumentCreate):
    return document_service.create_document(document)


@router.get(
    "/",
    response_model=list[DocumentResponse]
)
def get_documents():
    return document_service.get_all_documents()


@router.get(
    "/{document_id}",
    response_model=DocumentResponse
)
def get_document(document_id: int):
    document = document_service.get_document_by_id(document_id)

    if document is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Document not found"
        )

    return document


@router.delete(
    "/{document_id}",
    status_code=status.HTTP_204_NO_CONTENT
)
def delete_document(document_id: int):
    deleted = document_service.delete_document(document_id)

    if not deleted:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Document not found"
        )
