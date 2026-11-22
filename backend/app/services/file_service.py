
from pathlib import Path
from uuid import uuid4

import pymupdf

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
    """Validate and safely save an uploaded PDF."""

    try:
        # 1. Validate the filename
        if not file.filename or not file.filename.lower().endswith(".pdf"):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Only PDF files are allowed."
            )

        # 2. Validate the declared content type
        if file.content_type != "application/pdf":
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid file content type."
            )

        # 3. Read at most 10 MB + 1 byte
        content = await file.read(MAX_FILE_SIZE + 1)

        # 4. Check the file size
        if len(content) > MAX_FILE_SIZE:
            raise HTTPException(
                status_code=status.HTTP_413_CONTENT_TOO_LARGE,
                detail="File size exceeds the 10 MB limit."
            )

        # 5. Check the PDF signature
        if not content.startswith(b"%PDF-"):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="The uploaded file is not a valid PDF."
            )

        # 6. Validate the actual PDF structure
        try:
            with pymupdf.open(stream=content, filetype="pdf") as pdf:

                if pdf.needs_pass:
                    raise HTTPException(
                        status_code=status.HTTP_400_BAD_REQUEST,
                        detail="Password-protected PDFs are not supported."
                    )

                if pdf.page_count == 0:
                    raise HTTPException(
                        status_code=status.HTTP_400_BAD_REQUEST,
                        detail="PDF must contain at least one page."
                    )

        except pymupdf.FileDataError:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="The uploaded PDF is corrupted or unreadable."
            ) from None

        # 7. Generate a unique server-controlled filename
        stored_filename = f"{uuid4().hex}.pdf"
        file_path = UPLOAD_DIR / stored_filename

        ensure_upload_directory()

        # 8. Save the validated PDF
        try:
            file_path.write_bytes(content)

        except OSError:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Unable to save the uploaded file."
            ) from None

        return {
            "filename": file.filename,
            "stored_filename": stored_filename,
            "size": len(content),
            "status": "uploaded"
        }

    finally:
        # Always close the uploaded file
        await file.close()

