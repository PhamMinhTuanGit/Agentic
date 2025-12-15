import re
import os
import glob
from bs4 import BeautifulSoup
from typing import List, Dict
import json

def extract_html(raw_text: str) -> str:
    """
    Extract clean text from ZebOS-XP HTML documentation.
    
    Args:
        raw_text: Raw HTML content as string
        
    Returns:
        str: Clean extracted text content
    """
    soup = BeautifulSoup(raw_text, 'html.parser')
    
    # Remove script and style elements
    for script in soup(['script', 'style', 'meta', 'link', 'noscript']):
        script.decompose()
    
    # Get text content
    text = soup.get_text(separator='\n', strip=True)
    
    # Clean up whitespace
    # Remove excessive newlines (more than 2)
    text = re.sub(r'\n{3,}', '\n\n', text)
    
    # Remove excessive spaces
    text = re.sub(r' {2,}', ' ', text)
    
    # Remove tabs
    text = re.sub(r'\t+', ' ', text)
    
    # Remove non-printable characters except newlines and basic punctuation
    text = re.sub(r'[^\x20-\x7E\n]', '', text)
    
    # Remove lines with only whitespace
    lines = [line.strip() for line in text.split('\n') if line.strip()]
    text = '\n'.join(lines)
    
    return text


def semantic_chunking(text: str, max_chunk_size: int = 512, overlap: int = 50) -> List[str]:
    """
    Chia văn bản thành các chunks dựa trên ngữ nghĩa.
    
    Args:
        text: Văn bản đầu vào
        max_chunk_size: Kích thước tối đa của mỗi chunk (theo số từ)
        overlap: Số từ overlap giữa các chunks
        
    Returns:
        List[str]: Danh sách các chunks
    """
    # Tách theo đoạn văn trước
    paragraphs = text.split('\n\n')
    
    chunks = []
    current_chunk = []
    current_size = 0
    
    for para in paragraphs:
        para = para.strip()
        if not para:
            continue
            
        words = para.split()
        para_size = len(words)
        
        # Nếu đoạn văn quá dài, chia nhỏ hơn
        if para_size > max_chunk_size:
            # Lưu chunk hiện tại nếu có
            if current_chunk:
                chunks.append(' '.join(current_chunk))
                current_chunk = []
                current_size = 0
            
            # Chia đoạn văn lớn thành các chunks nhỏ
            for i in range(0, para_size, max_chunk_size - overlap):
                chunk_words = words[i:i + max_chunk_size]
                chunks.append(' '.join(chunk_words))
        
        # Nếu thêm đoạn này vào chunk hiện tại vượt quá max_chunk_size
        elif current_size + para_size > max_chunk_size:
            if current_chunk:
                chunks.append(' '.join(current_chunk))
            
            # Bắt đầu chunk mới với overlap
            if overlap > 0 and current_chunk:
                overlap_words = ' '.join(current_chunk).split()[-overlap:]
                current_chunk = overlap_words + words
                current_size = len(overlap_words) + para_size
            else:
                current_chunk = words
                current_size = para_size
        else:
            # Thêm đoạn văn vào chunk hiện tại
            current_chunk.extend(words)
            current_size += para_size
    
    # Thêm chunk cuối cùng
    if current_chunk:
        chunks.append(' '.join(current_chunk))
    
    return chunks


def process_html_files(html_dir: str, output_file: str, max_chunk_size: int = 512, overlap: int = 50):
    """
    Xử lý tất cả các file HTML trong thư mục và tạo chunks với metadata.
    
    Args:
        html_dir: Đường dẫn đến thư mục chứa file HTML
        output_file: Đường dẫn file output JSON
        max_chunk_size: Kích thước tối đa của chunk
        overlap: Overlap giữa các chunks
    """
    html_files = glob.glob(os.path.join(html_dir, "*.html"))
    
    all_chunks = []
    
    for idx, html_file in enumerate(html_files):
        print(f"Processing {idx + 1}/{len(html_files)}: {os.path.basename(html_file)}")
        
        try:
            with open(html_file, 'r', encoding='utf-8', errors='ignore') as f:
                raw_html = f.read()
            
            # Extract clean text
            clean_text = extract_html(raw_html)
            
            if not clean_text.strip():
                print(f"  ⚠ Skipped (empty content)")
                continue
            
            # Tạo chunks
            chunks = semantic_chunking(clean_text, max_chunk_size, overlap)
            
            # Thêm metadata cho mỗi chunk
            for chunk_idx, chunk in enumerate(chunks):
                all_chunks.append({
                    'chunk_id': f"{os.path.basename(html_file)}_{chunk_idx}",
                    'source_file': os.path.basename(html_file),
                    'chunk_index': chunk_idx,
                    'total_chunks': len(chunks),
                    'text': chunk,
                    'word_count': len(chunk.split())
                })
            
            print(f"  ✓ Created {len(chunks)} chunks")
            
        except Exception as e:
            print(f"  ✗ Error: {str(e)}")
            continue
    
    # Lưu kết quả ra file JSON
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(all_chunks, f, ensure_ascii=False, indent=2)
    
    print(f"\n✓ Total: {len(all_chunks)} chunks from {len(html_files)} files")
    print(f"✓ Saved to: {output_file}")
    
    # Thống kê
    total_words = sum(chunk['word_count'] for chunk in all_chunks)
    avg_words = total_words / len(all_chunks) if all_chunks else 0
    print(f"\nStatistics:")
    print(f"  - Total chunks: {len(all_chunks)}")
    print(f"  - Total words: {total_words}")
    print(f"  - Average words per chunk: {avg_words:.1f}")


if __name__ == "__main__":
    # Đường dẫn thư mục chứa HTML files
    HTML_DIR = "ZebOS-XP_1.4_HTML/ZebOS-XP 1.4"
    
    # File output
    OUTPUT_FILE = "zebos_chunks.json"
    
    # Cấu hình chunking
    MAX_CHUNK_SIZE = 512  # số từ
    OVERLAP = 50  # số từ overlap
    
    print("=" * 60)
    print("SEMANTIC CHUNKING FOR ZebOS-XP DOCUMENTATION")
    print("=" * 60)
    print(f"Input directory: {HTML_DIR}")
    print(f"Output file: {OUTPUT_FILE}")
    print(f"Max chunk size: {MAX_CHUNK_SIZE} words")
    print(f"Overlap: {OVERLAP} words")
    print("=" * 60)
    print()
    
    process_html_files(HTML_DIR, OUTPUT_FILE, MAX_CHUNK_SIZE, OVERLAP)
