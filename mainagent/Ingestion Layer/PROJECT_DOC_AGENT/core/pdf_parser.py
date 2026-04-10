import fitz # PyMuPDF

def extract_text(file_path):
    text = ""
    with fitz.open(file_path) as doc:
        for page in doc:
            # We add page markers so the Reasoning Engine knows context
            text += f"\n[Page {page.number}]\n" + page.get_text()
    return text