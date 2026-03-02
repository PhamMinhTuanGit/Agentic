"""Stage 1 PDF validation and metadata extraction for ingestion pipeline."""

from __future__ import annotations

import hashlib
from enum import Enum
from pathlib import Path
from typing import Any, List, Optional

from pydantic import BaseModel, Field

try:
    from pypdf import PdfReader
    from pypdf.errors import PdfReadError
except ImportError:  # pragma: no cover - compatibility fallback
    from PyPDF2 import PdfReader  # type: ignore
    from PyPDF2.errors import PdfReadError  # type: ignore

"""
Base Model 
"""
class PDFValidationFailureReason(str, Enum):
    """Known failure reasons for Stage 1 PDF validation."""

    FILE_NOT_FOUND = "FILE_NOT_FOUND"
    ENCRYPTED_OR_LOCKED = "ENCRYPTED_OR_LOCKED"
    MALFORMED_PDF = "MALFORMED_PDF"
    UNKNOWN_ERROR = "UNKNOWN_ERROR"


class OutlineNode(BaseModel):
    """Single outline/bookmark node."""

    title: str
    page_number: Optional[int] = None
    children: List["OutlineNode"] = Field(default_factory=list)


class PageMetadata(BaseModel):
    """Per-page metadata emitted by Stage 1."""

    page_number: int
    fingerprint: Optional[str] = None


class PDFValidationResult(BaseModel):
    """Structured output for Stage 1 PDF validation."""

    status: str
    page_count: Optional[int] = None
    outline_tree: List[OutlineNode] = Field(default_factory=list)
    per_page_metadata: List[PageMetadata] = Field(default_factory=list)
    failure_reason: Optional[PDFValidationFailureReason] = None
    failure_detail: Optional[str] = None


OutlineNode.model_rebuild()


def _extract_outline_tree(reader: PdfReader) -> List[OutlineNode]:
    """Extract outline/bookmarks while preserving hierarchy."""
    raw_outline = getattr(reader, "outline", None)
    if raw_outline is None:
        raw_outline = getattr(reader, "outlines", None)

    if not raw_outline:
        return []

    def walk(items: Any) -> List[OutlineNode]:
        """
        Recursively walks through a PDF outline/bookmark structure and converts it to a flat list of OutlineNode objects.

        This function processes PDF outline items which can be nested in lists (representing hierarchy).
        When a list is encountered, its contents are recursively processed and added as children to the
        last node in the current level.

        Args:
            items (Any): An iterable of outline items from a PDF. Items can be outline objects with
                         a 'title' attribute, dictionaries with a '/Title' key, or nested lists
                         representing child outline items.

        Returns:
            List[OutlineNode]: A flat list of OutlineNode objects, where each node contains:
                              - title: The bookmark title (defaults to "Untitled" if not found)
                              - page_number: The 1-based page number the bookmark points to (None if unavailable)
                              - children: Nested outline items processed recursively

        Note:
            - The function relies on a 'reader' object in the outer scope that has a
              'get_destination_page_number' method
            - Page numbers are converted from pypdf's zero-based indexing to one-based indexing
            - If page number extraction fails, it silently sets page_number to None
        """
        nodes: List[OutlineNode] = []
        for item in items:
            if isinstance(item, list):
                if nodes:
                    nodes[-1].children.extend(walk(item))
                continue

            title = getattr(item, "title", None)
            if title is None and isinstance(item, dict):
                title = item.get("/Title")
            if not title:
                title = "Untitled"

            page_number: Optional[int] = None
            try:
                # pypdf returns zero-based index; convert to one-based.
                page_number = reader.get_destination_page_number(item) + 1
            except Exception:
                page_number = None

            nodes.append(
                OutlineNode(
                    title=str(title),
                    page_number=page_number,
                )
            )
        return nodes

    return walk(raw_outline)


def _compute_page_fingerprint(page: Any) -> str:
    """
    Compute a stable page fingerprint from page geometry + content stream + text.
    """
    hasher = hashlib.sha256()
    hasher.update(str(page.mediabox).encode("utf-8", errors="ignore"))
    hasher.update(str(getattr(page, "rotation", 0) or 0).encode("utf-8", errors="ignore"))

    try:
        contents = page.get_contents()
        if contents is not None:
            if isinstance(contents, list):
                for content_obj in contents:
                    hasher.update(content_obj.get_data())
            else:
                hasher.update(contents.get_data())
    except Exception:
        pass

    try:
        text = page.extract_text() or ""
        hasher.update(text[:5000].encode("utf-8", errors="ignore"))
    except Exception:
        pass

    return hasher.hexdigest()


def _build_page_metadata(reader: PdfReader, compute_fingerprints: bool) -> List[PageMetadata]:
    """Build per-page metadata payload."""
    page_items: List[PageMetadata] = []
    for idx, page in enumerate(reader.pages, start=1):
        page_items.append(
            PageMetadata(
                page_number=idx,
                fingerprint=_compute_page_fingerprint(page) if compute_fingerprints else None,
            )
        )
    return page_items


def validate_pdf(
    pdf_path: str | Path,
    compute_fingerprints: bool = True,
) -> PDFValidationResult:
    """
    Stage 1 pipeline step:
    - open PDF
    - validate accessibility and format
    - count pages
    - optionally compute per-page fingerprint
    - extract outline/bookmarks
    """
    path = Path(pdf_path)

    if not path.exists():
        return PDFValidationResult(
            status="FAILED",
            failure_reason=PDFValidationFailureReason.FILE_NOT_FOUND,
            failure_detail=f"File does not exist: {path}",
        )

    try:
        reader = PdfReader(str(path))
    except PdfReadError as exc:
        return PDFValidationResult(
            status="FAILED",
            failure_reason=PDFValidationFailureReason.MALFORMED_PDF,
            failure_detail=str(exc),
        )
    except Exception as exc:
        return PDFValidationResult(
            status="FAILED",
            failure_reason=PDFValidationFailureReason.UNKNOWN_ERROR,
            failure_detail=str(exc),
        )

    if getattr(reader, "is_encrypted", False):
        return PDFValidationResult(
            status="FAILED",
            failure_reason=PDFValidationFailureReason.ENCRYPTED_OR_LOCKED,
            failure_detail="PDF is encrypted or locked.",
        )

    try:
        page_count = len(reader.pages)
        outline_tree = _extract_outline_tree(reader)
        per_page_metadata = _build_page_metadata(reader, compute_fingerprints=compute_fingerprints)
    except PdfReadError as exc:
        return PDFValidationResult(
            status="FAILED",
            failure_reason=PDFValidationFailureReason.MALFORMED_PDF,
            failure_detail=str(exc),
        )
    except Exception as exc:
        return PDFValidationResult(
            status="FAILED",
            failure_reason=PDFValidationFailureReason.UNKNOWN_ERROR,
            failure_detail=str(exc),
        )

    return PDFValidationResult(
        status="COMPLETED",
        page_count=page_count,
        outline_tree=outline_tree,
        per_page_metadata=per_page_metadata,
    )


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Validate a PDF and extract metadata.")
    parser.add_argument(
        "pdf_path",
        nargs="?",
        type=str,
        help="Path to the PDF file to validate.",
    )
    parser.add_argument(
        "--pdf_path",
        dest="pdf_path_flag",
        type=str,
        help="Path to the PDF file to validate (flag form).",
    )
    parser.add_argument(
        "--no-fingerprint",
        action="store_true",
        help="Skip per-page fingerprint generation.",
    )
    args = parser.parse_args()

    pdf_path = args.pdf_path_flag or args.pdf_path
    if not pdf_path:
        parser.error("Please provide a PDF path as positional arg or --pdf_path.")

    result = validate_pdf(pdf_path, compute_fingerprints=not args.no_fingerprint)
    print(result.model_dump_json(indent=2))
    
