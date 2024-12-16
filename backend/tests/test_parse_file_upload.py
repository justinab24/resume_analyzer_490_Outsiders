import pytest
from unittest.mock import MagicMock, patch
import io
from io import BytesIO
import pdfplumber
import docx
from utils.parse_file_upload import extract_text_from_pdf_in_memory, extract_text_from_docx_in_memory  # adjust the import as per your module

@pytest.fixture
def mock_pdf_content():
    """Fixture to return a mocked PDF file content as bytes"""
    return b"Mocked PDF file content"

@pytest.fixture
def mock_docx_content():
    """Fixture to return a mocked DOCX file content as bytes"""
    return b"Mocked DOCX file content"

def test_extract_text_from_pdf_in_memory(mock_pdf_content):
    """Test for the extract_text_from_pdf_in_memory function."""
    # Create a mocked pdfplumber.open that returns a mocked page with text
    with patch('utils.parse_file_upload.pdfplumber.open') as mock_pdf:
        mock_page = MagicMock()
        mock_page.extract_text.return_value = "Page 1 text."
        mock_pdf.return_value.__enter__.return_value.pages = [mock_page]

        # Call the function to test with the raw bytes content
        result = extract_text_from_pdf_in_memory(mock_pdf_content)

        # Assert the text extracted matches the expected
        assert result == "Page 1 text.\n"
        
        # Ensure pdfplumber.open was called with the correct object
        args, _ = mock_pdf.call_args
        assert args[0].getvalue() == mock_pdf_content

def test_extract_text_from_docx_in_memory(mock_docx_content):
    """Test for the extract_text_from_docx_in_memory function."""
    # Create a mocked docx.Document that returns mocked paragraphs
    with patch('utils.parse_file_upload.docx.Document') as mock_docx:
        mock_paragraph = MagicMock()
        mock_paragraph.text = "This is a paragraph."
        mock_docx.return_value.paragraphs = [mock_paragraph]

        # Call the function to test with the raw bytes content
        result = extract_text_from_docx_in_memory(mock_docx_content)

        # Assert the text extracted matches the expected
        assert result == "This is a paragraph.\n"
        
        # Ensure docx.Document was called with the correct object
        args, _ = mock_docx.call_args
        assert args[0].getvalue() == mock_docx_content