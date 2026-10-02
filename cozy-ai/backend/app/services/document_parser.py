import os
import re
from typing import Tuple
from pypdf import PdfReader
import docx

class DocumentParser:
    @staticmethod
    def parse_pdf(file_path: str) -> str:
        """Extract text from PDF using pypdf."""
        reader = PdfReader(file_path)
        extracted_pages = []
        for i, page in enumerate(reader.pages):
            text = page.extract_text() or ""
            if text.strip():
                extracted_pages.append(f"--- PAGE {i + 1} ---\n" + text)
        return "\n\n".join(extracted_pages)

    @staticmethod
    def parse_docx(file_path: str) -> str:
        """Extract text from DOCX file."""
        doc = docx.Document(file_path)
        paragraphs = [p.text for p in doc.paragraphs if p.text.strip()]
        return "\n".join(paragraphs)

    @staticmethod
    def parse_txt(file_path: str) -> str:
        """Read plain text or markdown file."""
        with open(file_path, "r", encoding="utf-8", errors="replace") as f:
            return f.read()

    @classmethod
    def extract_text(cls, file_path: str) -> Tuple[str, str]:
        """
        Extract raw text based on file extension.
        Returns: (raw_text, file_type)
        """
        ext = os.path.splitext(file_path)[1].lower()
        if ext == ".pdf":
            raw = cls.parse_pdf(file_path)
            file_type = "pdf"
        elif ext in [".docx", ".doc"]:
            raw = cls.parse_docx(file_path)
            file_type = "docx"
        elif ext in [".txt", ".md", ".csv"]:
            raw = cls.parse_txt(file_path)
            file_type = "txt"
        else:
            # Fallback to text reading
            raw = cls.parse_txt(file_path)
            file_type = "unknown"

        cleaned = cls.clean_text(raw)
        return cleaned, file_type

    @staticmethod
    def clean_text(text: str) -> str:
        """Normalize line breaks and clean whitespace."""
        # Replace multiple spaces with a single space, but keep newlines
        lines = [line.strip() for line in text.splitlines()]
        cleaned_lines = []
        for line in lines:
            # Skip empty lines or pure page number markers
            if not line:
                cleaned_lines.append("")
                continue
            # Remove isolated page headers / footers like "Page 1 of 5"
            if re.match(r"^(?:Page\s+\d+(?:\s+of\s+\d+)?|\d+\s*/\s*\d+)$", line, re.IGNORECASE):
                continue
            cleaned_lines.append(line)
        return "\n".join(cleaned_lines)
