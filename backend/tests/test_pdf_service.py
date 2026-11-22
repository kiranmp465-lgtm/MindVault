
import pymupdf
import pytest

from app.services.pdf_service import extract_text_from_pdf


def create_test_pdf(file_path, pages):
    """Create a temporary PDF containing the supplied page text."""

    pdf = pymupdf.open()

    for page_text in pages:
        page = pdf.new_page()
        page.insert_text((72, 72), page_text)

    pdf.save(file_path)
    pdf.close()


def test_extract_text_from_single_page_pdf(tmp_path):
    """Test text extraction from a one-page PDF."""

    pdf_path = tmp_path / "single_page.pdf"

    create_test_pdf(pdf_path, ["Welcome to MindVault"])

    result = extract_text_from_pdf(pdf_path)

    assert result["total_pages"] == 1
    assert result["total_characters"] > 0
    assert "Welcome to MindVault" in result["text"]
    assert result["pages"][0]["page"] == 1


def test_extract_text_from_multiple_page_pdf(tmp_path):
    """Test text extraction from a PDF with multiple pages."""

    pdf_path = tmp_path / "multiple_pages.pdf"

    create_test_pdf(
        pdf_path,
        [
            "This is page one",
            "This is page two",
            "This is page three",
        ]
    )

    result = extract_text_from_pdf(pdf_path)

    assert result["total_pages"] == 3
    assert "This is page one" in result["text"]
    assert "This is page two" in result["text"]
    assert "This is page three" in result["text"]


def test_extract_text_from_pdf_with_blank_page(tmp_path):
    """Test extraction from a PDF containing a blank page."""

    pdf_path = tmp_path / "blank_page.pdf"

    create_test_pdf(pdf_path, [""])

    result = extract_text_from_pdf(pdf_path)

    assert result["total_pages"] == 1
    assert result["total_characters"] == 0
    assert result["text"] == ""


def test_extract_text_from_corrupted_pdf(tmp_path):
    """Test that corrupted PDFs raise an appropriate error."""

    pdf_path = tmp_path / "corrupted.pdf"

    pdf_path.write_bytes(b"This is not a valid PDF file")

    with pytest.raises(pymupdf.FileDataError):
        extract_text_from_pdf(pdf_path)
