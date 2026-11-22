from app.services.pdf_service import extract_text_from_pdf
from app.services.file_service import UPLOAD_DIR
from fastapi import APIRouter, HTTPException, UploadFile, File, status

from app.services.file_service import save_pdf
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



@router.post(
    "/upload",
    status_code=status.HTTP_201_CREATED
)
async def upload_document(file: UploadFile = File(...)):
    """Upload a PDF, extract its text, and clean up on failure."""

    result = await save_pdf(file)

    file_path = UPLOAD_DIR / result["stored_filename"]

    try:
        extracted_data = extract_text_from_pdf(file_path)

    except Exception:
        # Remove the uploaded PDF if extraction fails
        file_path.unlink(missing_ok=True)

        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_CONTENT,
            detail="Unable to extract text from the uploaded PDF."
        ) from None

    return {
        "message": "PDF uploaded and processed successfully",
        "document": result,
        "extraction": {
            "total_pages": extracted_data["total_pages"],
            "total_characters": extracted_data["total_characters"],
            "text": extracted_data["text"]
        }
    }
