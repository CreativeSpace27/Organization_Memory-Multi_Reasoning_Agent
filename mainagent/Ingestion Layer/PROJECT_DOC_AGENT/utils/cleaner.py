import re

def clean_document_text(text):
    """
    Removes boilerplate, excessive whitespace, and non-informative text.
    """
    # 1. Remove common footer/header patterns (e.g., "Page 1 of 10")
    text = re.sub(r"(?i)Page \d+ of \d+", "", text)
    
    # 2. Remove multiple newlines and tabs to save tokens
    text = re.sub(r'\n\s*\n', '\n', text)
    text = re.sub(r'\t+', ' ', text)
    
    # 3. Remove non-ASCII characters (often weird symbols from PDFs)
    text = text.encode("ascii", "ignore").decode()
    
    # 4. Remove generic boilerplate (Customizable)
    # Example: If every doc has "Confidential - Internal Use Only"
    text = text.replace("Confidential - Internal Use Only", "")

    return text.strip()