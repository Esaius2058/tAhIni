import logging
import tempfile
from docx import Document
from uuid import UUID
from pdfminer.high_level import extract_text
from backend.src.db.models import ExamContent
from sqlalchemy.orm import Session
from fastapi import UploadFile

class FileExtractor:
    def __init__(self):
        self.logger = logging.getLogger("Parser:File Extractor")

    def extract(self, file: UploadFile):
        if file.filename.endswith(".pdf"):
            return self._extract_pdf(file)
        elif file.filename.endswith(".docx"):
            return self._extract_docx(file)
        else:
            raise ValueError("Unsupported file type")

    def _extract_pdf(self, file: UploadFile):
        try:
            text = extract_text(file.file)
            return text
        except Exception as e:
            self.logger.error(f"Error extracting text from file '{file.filename}': {e}")
            return ""

    def _extract_docx(self, file: UploadFile):
        try:
            doc = Document(file.file)
            text = "\n".join([p.text for p in doc.paragraphs])
            return text
        except Exception as e:
            self.logger.error(f"Error extracting text from file '{file.filename}': {e}")
            return ""


class TextCleaner:
    def __init__(self):
        self.logger = logging.getLogger("Parser:Text Cleaner")

    def clean(self, text: str) -> str:
        text = self._remove_headers_and_footers(text)
        text = _normalize_whitespace(text)
        return text

    def _remove_headers_and_footers(self, text: str) -> str:
        try:
            pages = text.split("\f") if "\f" in text else text.split("\n\n")
            cleaned_pages = []

            first_lines, last_lines = [], []
            for page in pages:
                lines = page.strip().splitlines()
                if lines:
                    first_lines.append(lines[0].strip())
                    last_lines.append(lines[-1].strip())

            header_candidates = {line for line in first_lines if first_lines.count(line) > 1}
            footer_candidates = {line for line in last_lines if last_lines.count(line) > 1}

            # Regex patterns for page numbers, etc.
            regex_patterns = [
                r"^Page \d+ of \d+$",
                r"^Page \d+$",
                r"^\d+$"
                r"^\s*-+\s*$"
            ]

            for page in pages:
                lines = page.strip().splitlines()
                filtered = []
                for l in lines:
                    # skip header/footer candidates
                    if l.strip() in header_candidates or l.strip() in footer_candidates:
                        continue
                    # skip lines matching regex patterns
                    if any(re.match(p, l.strip(), flags=re.IGNORECASE) for p in regex_patterns):
                        continue
                    filtered.append(l)
                cleaned_pages.append("\n".join(filtered))

            return "\n\n".join(cleaned_pages)
        except Exception as e:
            if self.logger:
                self.logger.error(f"Error cleaning headers/footers: {e}")
            return text

    def _normalize_whitespace(self, text: str) -> str:
        return " ".join(text.split())


class ExamContentRepository:
    def __init__(self, db: Session):
        self.db = db
        self.logger = logging.getLogger("Parser:Exam Repo")

    def store(self, upload_id: UUID, text: str):
        try:
            self.db.query(ExamContent).filter(upload_id=upload_id).update({"text": text})
            self.db.commit()
            return True
        except Exception as e:
            self.logger.error(f"Error storing text in database: {e}")
            return False

class ExamPipeLine:
    def __init__(self, db: Session):
        self.extractor = FileExtractor()
        self.cleaner = TextCleaner()
        self.repo = ExamContentRepository(db)
        self.logger = logging.getLogger("Parser:Exam Pipeline")

    def process_upload(self, upload_id: UUID, file: UploadFile):
        try:
            raw_text = self.extractor.extract(file)
            clean_text = self.cleaner.clean(raw_text)
            self.repo.store(upload_id, clean_text)
            if not clean_text:
                raise ValueError("Failed to clean text")
            return clean_text
        except Exception as e:
            self.logger.error(f"Error extracting file {file.filename} contents: {e}")
            return None
