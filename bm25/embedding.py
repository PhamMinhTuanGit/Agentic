import ollama
from bm25.bm25 import tokenize_en
import re
from typing import List, Dict
import numpy as np
import os

# filepath: /home/tuanpm/work/Agentic/bm25/embedding.py

# Configure Ollama client for Docker environment
OLLAMA_HOST = os.getenv('OLLAMA_HOST', 'http://localhost:11434')
if os.getenv('RUNNING_IN_DOCKER', 'false').lower() == 'true':
    OLLAMA_HOST = 'http://ollama:11434'

# Create client instance
ollama_client = ollama.Client(host=OLLAMA_HOST)


# ============ CHUNKING FUNCTIONS ============

def chunk_by_paragraphs(text: str, max_chunk_size: int = 512, overlap: int = 50) -> List[str]:
    """
    Chia văn bản thành chunks dựa trên đoạn văn.
    
    Args:
        text (str): Văn bản đầu vào
        max_chunk_size (int): Kích thước tối đa của chunk (theo số từ)
        overlap (int): Số từ overlap giữa các chunks
        
    Returns:
        List[str]: Danh sách các chunks
    """
    # Tách theo đoạn văn
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


def chunk_by_sentences(text: str, max_chunk_size: int = 512, overlap: int = 50) -> List[str]:
    """
    Chia văn bản thành chunks dựa trên câu.
    
    Args:
        text (str): Văn bản đầu vào
        max_chunk_size (int): Kích thước tối đa của chunk (theo số từ)
        overlap (int): Số từ overlap giữa các chunks
        
    Returns:
        List[str]: Danh sách các chunks
    """
    # Tách thành các câu
    sentences = re.split(r'(?<=[.!?])\s+', text)
    
    chunks = []
    current_chunk = []
    current_size = 0
    
    for sentence in sentences:
        sentence = sentence.strip()
        if not sentence:
            continue
            
        words = sentence.split()
        sentence_size = len(words)
        
        # Nếu câu quá dài
        if sentence_size > max_chunk_size:
            if current_chunk:
                chunks.append(' '.join(current_chunk))
                current_chunk = []
                current_size = 0
            
            # Chia câu thành các phần
            for i in range(0, sentence_size, max_chunk_size - overlap):
                chunk_words = words[i:i + max_chunk_size]
                chunks.append(' '.join(chunk_words))
        
        # Nếu thêm câu này vượt quá max_chunk_size
        elif current_size + sentence_size > max_chunk_size:
            if current_chunk:
                chunks.append(' '.join(current_chunk))
            
            # Bắt đầu chunk mới với overlap
            if overlap > 0 and current_chunk:
                overlap_words = ' '.join(current_chunk).split()[-overlap:]
                current_chunk = overlap_words + words
                current_size = len(overlap_words) + sentence_size
            else:
                current_chunk = words
                current_size = sentence_size
        else:
            # Thêm câu vào chunk hiện tại
            current_chunk.extend(words)
            current_size += sentence_size
    
    # Thêm chunk cuối cùng
    if current_chunk:
        chunks.append(' '.join(current_chunk))
    
    return chunks


def chunk_by_size(text: str, max_chunk_size: int = 512, overlap: int = 50) -> List[str]:
    """
    Chia văn bản thành chunks dựa trên kích thước.
    
    Args:
        text (str): Văn bản đầu vào
        max_chunk_size (int): Kích thước tối đa của chunk (theo số từ)
        overlap (int): Số từ overlap giữa các chunks
        
    Returns:
        List[str]: Danh sách các chunks
    """
    words = text.split()
    chunks = []
    
    for i in range(0, len(words), max_chunk_size - overlap):
        chunk = words[i:i + max_chunk_size]
        if chunk:
            chunks.append(' '.join(chunk))
    
    return chunks


# ============ EMBEDDING FUNCTIONS ============

def embed_text(text):
    """
    Generate embedding for a single text using nomic-embed-text model from Ollama.
    
    Args:
        text (str): Input text to embed
        
    Returns:
        list: Embedding vector
    """
    response = ollama_client.embeddings(
        model='nomic-embed-text:latest',
        prompt=text
    )
    return response['embedding']


def embed_batch(texts):
    """
    Generate embeddings for a batch of texts using nomic-embed-text model from Ollama.
    
    Args:
        texts (list): List of input texts to embed
        
    Returns:
        list: List of embedding vectors
    """
    embeddings = []
    for text in texts:
        embedding = embed_text(text)
        embeddings.append(embedding)
    return embeddings


def chunk_and_embed(
    text: str,
    chunking_method: str = 'paragraphs',
    max_chunk_size: int = 512,
    overlap: int = 50
) -> List[Dict]:
    """
    Chia văn bản thành chunks và tạo embeddings cho mỗi chunk.
    
    Args:
        text (str): Văn bản đầu vào
        chunking_method (str): Phương pháp chunking ('paragraphs', 'sentences', 'size')
        max_chunk_size (int): Kích thước tối đa của chunk
        overlap (int): Số từ overlap
        
    Returns:
        List[Dict]: Danh sách các dict chứa chunk và embedding
    """
    # Chọn phương pháp chunking
    if chunking_method == 'paragraphs':
        chunks = chunk_by_paragraphs(text, max_chunk_size, overlap)
    elif chunking_method == 'sentences':
        chunks = chunk_by_sentences(text, max_chunk_size, overlap)
    elif chunking_method == 'size':
        chunks = chunk_by_size(text, max_chunk_size, overlap)
    else:
        raise ValueError(f"Unknown chunking method: {chunking_method}")
    
    # Tạo embeddings
    embeddings = embed_batch(chunks)
    
    # Kết hợp chunks và embeddings
    result = []
    for idx, (chunk, embedding) in enumerate(zip(chunks, embeddings)):
        result.append({
            'chunk_id': idx,
            'text': chunk,
            'embedding': embedding,
            'word_count': len(chunk.split()),
            'method': chunking_method
        })
    
    return result





if __name__ == "__main__":
    # Test embedding
    sample_text = """This is a sample text for embedding. It contains multiple sentences and paragraphs.

Here is a second paragraph with more information. We are testing the chunking functionality with various methods.

The third paragraph demonstrates how the system can split text into meaningful chunks while preserving context through overlap."""
    
    print("=" * 60)
    print("Testing Chunking and Embedding")
    print("=" * 60)
    
    # Test chunking methods
    print("\n1. Chunking by paragraphs:")
    chunks_para = chunk_by_paragraphs(sample_text, max_chunk_size=20, overlap=5)
    for idx, chunk in enumerate(chunks_para):
        print(f"   Chunk {idx}: {len(chunk.split())} words - {chunk[:50]}...")
    
    print("\n2. Chunking by sentences:")
    chunks_sent = chunk_by_sentences(sample_text, max_chunk_size=20, overlap=5)
    for idx, chunk in enumerate(chunks_sent):
        print(f"   Chunk {idx}: {len(chunk.split())} words - {chunk[:50]}...")
    
    print("\n3. Chunking by size:")
    chunks_size = chunk_by_size(sample_text, max_chunk_size=20, overlap=5)
    for idx, chunk in enumerate(chunks_size):
        print(f"   Chunk {idx}: {len(chunk.split())} words - {chunk[:50]}...")
    
    # Test chunk and embed
    print("\n4. Combining chunking and embedding:")
    print("   Processing text with paragraph chunking...")
    result = chunk_and_embed(sample_text, chunking_method='paragraphs', max_chunk_size=30)
    
    print(f"   Created {len(result)} chunks")
    for item in result:
        print(f"   - Chunk {item['chunk_id']}: {item['word_count']} words, "
              f"embedding dim: {len(item['embedding'])}")
    
    print("\n✓ All tests completed successfully!")
    print("=" * 60)