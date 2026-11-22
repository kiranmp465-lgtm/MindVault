
from pathlib import Path
from uuid import uuid4

from fastapi import HTTPException, UploadFile, status


# Locate the backend directory
BASE_DIR = Path(__file__).resolve().parents[2]

# Directory where uploaded PDFs will be stored
UPLOAD_DIR = BASE_DIR / "storage" / "uploads"

# Maximum upload size: 10 MB
MAX_FILE_SIZE = 10 * 1024 * 1024


def ensure_upload_directory() -> None:
    """Create the upload directory if it does not exist."""
    UPLOAD_DIR.mkdir(parents=True, exist_ok=True)


async def save_pdf(file: UploadFile) -> dict:
    """Validate and save an uploaded PDF."""

    # Check the original filename
    if not file.filename or not file.filename.lower().endswith(".pdf"):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Only PDF files are allowed."
        )

    # Check the declared content type
    if file.content_type != "application/pdf":
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid file content type."
        )

    # Read at most 10 MB + 1 byte to detect oversized files
    content = await file.read(MAX_FILE_SIZE + 1)

    if len(content) > MAX_FILE_SIZE:
        raise HTTPException(
            status_code=status.HTTP_413_REQUEST_ENTITY_TOO_LARGE,
            detail="File size exceeds the 10 MB limit."
        )

    # Check the PDF file signature
    if not content.startswith(b"%PDF-"):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="The uploaded file is not a valid PDF."
        )

    # Generate a unique server-controlled filename
    stored_filename = f"{uuid4().hex}.pdf"
    file_path = UPLOAD_DIR / stored_filename

    ensure_upload_directory()

    try:
        file_path.write_bytes(content)
    except OSError:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Unable to save the uploaded file."
        ) from None
    finally:
        await file.close()

    return {
        "filename": file.filename,
        "stored_filename": stored_filename,
        "size": len(content),
        "status": "uploaded"
    }
