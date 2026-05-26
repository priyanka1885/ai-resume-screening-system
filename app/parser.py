"""
parser.py - Resume text extraction from PDF, DOCX, and TXT files.

Handles reading uploaded files and converting them to plain text
for downstream processing.
"""

import io
from typing import Optional

import pdfplumber
from docx import Document


def extract_text_from_pdf(file_bytes: bytes) -> str:
    """
    Extract text content from a PDF file.

    Args:
        file_bytes: Raw bytes of the PDF file.

    Returns:
        Extracted text as a single string.

    Raises:
        ValueError: If the PDF cannot be read or contains no text.
    """
    try:
        text_parts: list[str] = []
        with pdfplumber.open(io.BytesIO(file_bytes)) as pdf:
            for page in pdf.pages:
                page_text: Optional[str] = page.extract_text()
                if page_text:
                    text_parts.append(page_text)

        full_text = "\n".join(text_parts).strip()
        if not full_text:
            raise ValueError("PDF file contains no extractable text.")
        return full_text

    except Exception as e:
        raise ValueError(f"Failed to extract text from PDF: {str(e)}")


def extract_text_from_docx(file_bytes: bytes) -> str:
    """
    Extract text content from a DOCX file.

    Args:
        file_bytes: Raw bytes of the DOCX file.

    Returns:
        Extracted text as a single string.

    Raises:
        ValueError: If the DOCX cannot be read or contains no text.
    """
    try:
        doc = Document(io.BytesIO(file_bytes))
        text_parts: list[str] = []
        for paragraph in doc.paragraphs:
            if paragraph.text.strip():
                text_parts.append(paragraph.text.strip())

        full_text = "\n".join(text_parts).strip()
        if not full_text:
            raise ValueError("DOCX file contains no extractable text.")
        return full_text

    except Exception as e:
        raise ValueError(f"Failed to extract text from DOCX: {str(e)}")


def extract_text_from_txt(file_bytes: bytes) -> str:
    """
    Extract text content from a plain text file.

    Args:
        file_bytes: Raw bytes of the TXT file.

    Returns:
        Extracted text as a single string.

    Raises:
        ValueError: If the file cannot be decoded or is empty.
    """
    try:
        # Try UTF-8 first, fall back to latin-1
        try:
            text = file_bytes.decode("utf-8")
        except UnicodeDecodeError:
            text = file_bytes.decode("latin-1")

        text = text.strip()
        if not text:
            raise ValueError("TXT file is empty.")
        return text

    except Exception as e:
        raise ValueError(f"Failed to extract text from TXT: {str(e)}")


def extract_text(file_bytes: bytes, filename: str) -> str:
    """
    Route file to the appropriate text extractor based on file extension.

    Args:
        file_bytes: Raw bytes of the uploaded file.
        filename: Original filename (used to determine file type).

    Returns:
        Extracted text content.

    Raises:
        ValueError: If the file type is unsupported or extraction fails.
    """
    filename_lower = filename.lower()

    if filename_lower.endswith(".pdf"):
        return extract_text_from_pdf(file_bytes)
    elif filename_lower.endswith(".docx"):
        return extract_text_from_docx(file_bytes)
    elif filename_lower.endswith(".txt"):
        return extract_text_from_txt(file_bytes)
    else:
        raise ValueError(
            f"Unsupported file type: '{filename}'. "
            "Accepted formats: .pdf, .docx, .txt"
        )
