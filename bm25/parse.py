import trafilatura
import re
import unicodedata


def extract_text_from_html_file(file_path):
    with open(file_path, encoding="utf-8", errors="ignore") as f:
        html = f.read()

    text = trafilatura.extract(
        html,
        include_links=False,
        include_tables=True
    )
    
    if not text:
        return ""

    return text
def normalize_text(text):
    text = unicodedata.normalize("NFKC", text)
    text = re.sub(r"\s+", " ", text)
    return text.strip()

def pipeline_html_extraction_and_normalization(file_path):
    extracted_text = extract_text_from_html_file(file_path)

    if not extracted_text:
        return None

    normalized_text = normalize_text(extracted_text)

    doc = {
        "source": file_path,
        "content": normalized_text,
        "length": len(normalized_text),
        "type": "html"
    }

    return doc

if __name__ == "__main__":
	
	html_file_path = "ZebOS-XP_1.4_HTML/ZebOS-XP 1.4/AAA Commands.603.04.html"
	extracted_text = extract_text_from_html_file(html_file_path)
	normalized_text = normalize_text(extracted_text)
	print(normalized_text)