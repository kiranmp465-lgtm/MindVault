
from pathlib import Path

from app.services.pdf_service import extract_text_from_pdf
from app.services.file_service import UPLOAD_DIR


# Use the PDF you uploaded through Swagger
pdf_path = UPLOAD_DIR / "f6ce01b490c24392b2ea8e6c4c7afdd8.pdf"

# Extract PDF text
result = extract_text_from_pdf(pdf_path)

print("\n========== PDF EXTRACTION RESULTS ==========")

print("Total pages:", result["total_pages"])
print("Total characters:", result["total_characters"])

print("\n========== EXTRACTED TEXT (FIRST 1500 CHARACTERS) ==========")

print(result["text"][:1500])
