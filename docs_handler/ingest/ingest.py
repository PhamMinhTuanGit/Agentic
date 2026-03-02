import fitz  # PyMuPDF

def read_pdf(file_path: str) -> str:
    """
    Read text content from a PDF file using PyMuPDF.
    
    Args:
        file_path: Path to the PDF file
        
    Returns:
        Extracted text content from the PDF
    """
    text = ""
    try:
        pdf_document = fitz.open(file_path)
        for page_num in range(len(pdf_document)):
            page = pdf_document[page_num]
            text += page.get_text()
        pdf_document.close()
    except Exception as e:
        print(f"Error reading PDF: {e}")
    
    return text