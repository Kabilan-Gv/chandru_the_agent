import PyPDF2
import docx
from typing import Dict, Any
import io

class DocumentProcessor:
    """Process and extract text from various document formats"""

    @staticmethod
    def extract_text_from_pdf(file_bytes: bytes) -> str:
        """Extract text from PDF file"""
        try:
            pdf_file = io.BytesIO(file_bytes)
            pdf_reader = PyPDF2.PdfReader(pdf_file)

            text = ""
            for page in pdf_reader.pages:
                text += page.extract_text() + "\n"

            return text.strip()
        except Exception as e:
            raise Exception(f"Error extracting text from PDF: {str(e)}")

    @staticmethod
    def extract_text_from_docx(file_bytes: bytes) -> str:
        """Extract text from DOCX file"""
        try:
            docx_file = io.BytesIO(file_bytes)
            doc = docx.Document(docx_file)

            text = ""
            for paragraph in doc.paragraphs:
                text += paragraph.text + "\n"

            return text.strip()
        except Exception as e:
            raise Exception(f"Error extracting text from DOCX: {str(e)}")

    @staticmethod
    def extract_text_from_txt(file_bytes: bytes) -> str:
        """Extract text from TXT file"""
        try:
            return file_bytes.decode('utf-8').strip()
        except Exception as e:
            raise Exception(f"Error extracting text from TXT: {str(e)}")

    @staticmethod
    def process_document(file_bytes: bytes, file_type: str) -> Dict[str, Any]:
        """Process document based on file type"""
        file_type = file_type.lower()

        if file_type in ['pdf', 'application/pdf']:
            text = DocumentProcessor.extract_text_from_pdf(file_bytes)
        elif file_type in ['docx', 'application/vnd.openxmlformats-officedocument.wordprocessingml.document']:
            text = DocumentProcessor.extract_text_from_docx(file_bytes)
        elif file_type in ['txt', 'text/plain']:
            text = DocumentProcessor.extract_text_from_txt(file_bytes)
        else:
            raise Exception(f"Unsupported file type: {file_type}")

        return {
            "text": text,
            "word_count": len(text.split()),
            "char_count": len(text)
        }
