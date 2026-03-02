from pathlib import Path

from app.services.document.pdf_validation import (
    PDFValidationFailureReason,
    validate_pdf_stage1,
)

try:
    from pypdf import PdfWriter
except ImportError:  # pragma: no cover
    from PyPDF2 import PdfWriter  # type: ignore


def test_validate_pdf_stage1_success(tmp_path: Path) -> None:
    pdf_path = tmp_path / "ok.pdf"
    writer = PdfWriter()
    writer.add_blank_page(width=612, height=792)
    writer.add_blank_page(width=612, height=792)
    if hasattr(writer, "add_outline_item"):
        writer.add_outline_item("Start", 0)
    else:  # PyPDF2 compatibility
        writer.add_bookmark("Start", 0)
    with pdf_path.open("wb") as handle:
        writer.write(handle)

    result = validate_pdf_stage1(pdf_path)

    assert result.status == "COMPLETED"
    assert result.page_count == 2
    assert len(result.per_page_metadata) == 2
    assert result.per_page_metadata[0].fingerprint
    assert len(result.outline_tree) >= 1
    assert result.failure_reason is None


def test_validate_pdf_stage1_encrypted_pdf(tmp_path: Path) -> None:
    pdf_path = tmp_path / "locked.pdf"
    writer = PdfWriter()
    writer.add_blank_page(width=612, height=792)
    writer.encrypt(user_password="secret")
    with pdf_path.open("wb") as handle:
        writer.write(handle)

    result = validate_pdf_stage1(pdf_path)

    assert result.status == "FAILED"
    assert result.failure_reason == PDFValidationFailureReason.ENCRYPTED_OR_LOCKED


def test_validate_pdf_stage1_malformed_pdf(tmp_path: Path) -> None:
    bad_pdf_path = tmp_path / "broken.pdf"
    bad_pdf_path.write_bytes(b"not-a-real-pdf")

    result = validate_pdf_stage1(bad_pdf_path)

    assert result.status == "FAILED"
    assert result.failure_reason == PDFValidationFailureReason.MALFORMED_PDF
