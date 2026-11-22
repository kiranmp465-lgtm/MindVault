
import pymupdf

from pathlib import Path


def extract_text_from_pdf(file_path: Path) -> dict:
    """Extract text from every page of a PDF."""

    extracted_pages = []

    with pymupdf.open(file_path) as pdf:
        for page_number, page in enumerate(pdf, start=1):
            page_text = page.get_text("text")

            extracted_pages.append({
                "page": page_number,
                "text": page_text.strip()
            })

    full_text = "\n\n".join(
        page["text"] for page in extracted_pages
    )

    return {
        "total_pages": len(extracted_pages),
        "total_characters": len(full_text),
        "text": full_text,
        "pages": extracted_pages
    }
