import pdfplumber
import docx
import io
import re

def extract_text_from_pdf_in_memory(file_content: bytes) -> str:
    with pdfplumber.open(io.BytesIO(file_content)) as pdf:
        text = ""
        for page in pdf.pages:
            text += page.extract_text() + "\n"
    return text

def extract_text_from_docx_in_memory(file_content: bytes) -> str:
    doc = docx.Document(io.BytesIO(file_content))
    text = ""
    for paragraph in doc.paragraphs:
        text += paragraph.text + "\n"
    return text


def split_description_by_headers(description):
    # Define flexible header patterns for required, preferred, and other common headers
    header_patterns = {
        "required": re.compile(r"(?i)\b(required skills|must-have|essential|mandatory|minimum qualifications)\b"),
        "preferred": re.compile(r"(?i)\b(preferred qualifications|nice to have|bonus|desired skills)\b"),
    }

    # Define a pattern for bulleted lists (e.g., *, -, or •)
    bullet_pattern = re.compile(r"^(\*|-|•|\d+\.)\s+.*")

    lines = description.split("\n")
    current_header = None
    sections = {"required": "", "preferred": ""}
    blankNum = 0
    section_text = ""

    for i, line in enumerate(lines):
        line = line.strip()
        
        if current_header == None:
            for header, pattern in header_patterns.items():
                print(f"Checking line against pattern: {line} -> {pattern}")
                if pattern.search(line):
                    current_header = header
                    break;
        else:
            print("Current header: ", current_header, "Line: ", line)
            print(blankNum)
            if not line:
                blankNum += 1
            else:
                section_text += line + " "
            if blankNum > 1:
                print("Blank number: ", blankNum, "Section text: ", section_text)
                sections[current_header] = section_text
                section_text = ""
                blankNum = 0
                current_header = None

    return sections