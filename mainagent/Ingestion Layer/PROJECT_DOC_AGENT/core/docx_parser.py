import fitz  # PyMuPDF
import docx
import os

def extract_text(file_path):
    """
    Identifies the file type and routes it to the correct extraction logic.
    """
    ext = os.path.splitext(file_path)[-1].lower()
    
    if ext == ".pdf":
        return _parse_pdf(file_path)
    elif ext == ".docx":
        return _parse_docx(file_path)
    else:
        raise ValueError(f"Unsupported file format: {ext}")

def _parse_pdf(file_path):
    text = ""
    with fitz.open(file_path) as doc:
        for page in doc:
            # We add a small marker so the LLM knows the document structure
            text += f"\n[DOC_PAGE_{page.number + 1}]\n"
            text += page.get_text("text")
    return text

def _parse_docx(file_path):
    doc = docx.Document(file_path)
    # Joining paragraphs with newlines
    return "\n".join([para.text for para in doc.paragraphs])