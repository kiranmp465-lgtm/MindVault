
import pytest
import pymupdf

from io import BytesIO
from fastapi import HTTPException, UploadFile

from app.services.file_service import save_pdf, UPLOAD_DIR


def create_pdf():
    """Create a valid one-page PDF in memory."""

    pdf = pymupdf.open()
    page = pdf.new_page()
    page.insert_text((72, 72), "MindVault security test")

    content = pdf.tobytes()
    pdf.close()

    return content


@pytest.mark.anyio
async def test_upload_valid_pdf():
    """A valid PDF should upload successfully."""

    upload = UploadFile(
        filename="valid.pdf",
        file=BytesIO(create_pdf()),
        headers={"content-type": "application/pdf"}
    )

    result = await save_pdf(upload)

    saved_path = UPLOAD_DIR / result["stored_filename"]

    assert result["status"] == "uploaded"
    assert saved_path.exists()

    saved_path.unlink()


@pytest.mark.anyio
async def test_reject_corrupted_pdf():
    """A corrupted PDF should be rejected."""

    upload = UploadFile(
        filename="corrupted.pdf",
        file=BytesIO(b"%PDF-1.4 invalid content"),
        headers={"content-type": "application/pdf"}
    )

    with pytest.raises(HTTPException) as error:
        await save_pdf(upload)

    assert error.value.status_code == 400


@pytest.mark.anyio
async def test_reject_text_file_renamed_as_pdf():
    """A text file renamed to PDF should be rejected."""

    upload = UploadFile(
        filename="fake.pdf",
        file=BytesIO(b"%PDF-1.4 this is not a real PDF"),
        headers={"content-type": "application/pdf"}
    )

    with pytest.raises(HTTPException) as error:
        await save_pdf(upload)

    assert error.value.status_code == 400


@pytest.mark.anyio
async def test_reject_oversized_pdf():
    """A file exceeding 10 MB should be rejected."""

    oversized_content = b"%PDF-" + b"A" * (10 * 1024 * 1024)

    upload = UploadFile(
        filename="large.pdf",
        file=BytesIO(oversized_content),
        headers={"content-type": "application/pdf"}
    )

    with pytest.raises(HTTPException) as error:
        await save_pdf(upload)

    assert error.value.status_code == 413
