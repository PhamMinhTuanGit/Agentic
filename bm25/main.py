import os
import faiss
import numpy as np
from pathlib import Path
from bm25.parse import pipeline_html_extraction_and_normalization
from bm25.embedding import (
    embed_text, embed_batch, 
    chunk_by_paragraphs, chunk_by_sentences, chunk_by_size
)
from bm25.bm25 import BM25Okapi, tokenize_en
import pickle

# filepath: /home/tuanpm/work/Agentic/bm25/main.py


def process_documents(directory_path):
    """
    Process all HTML files in a directory and extract text content.
    
    Args:
        directory_path (str): Path to directory containing HTML files
        
    Returns:
        list: List of document dictionaries
    """
    documents = []
    html_files = Path(directory_path).rglob("*.html")
    
    for html_file in html_files:
        doc = pipeline_html_extraction_and_normalization(str(html_file))
        if doc:
            documents.append(doc)
    
    return documents


def _split_long_chunk(chunk: str, max_words: int = 300, overlap: int = 30) -> list:
    """
    Split a chunk that's too long into smaller pieces.
    
    Args:
        chunk (str): Text chunk to split
        max_words (int): Maximum words per piece
        overlap (int): Words to overlap between pieces
        
    Returns:
        list: List of smaller chunks
    """
    words = chunk.split()
    if len(words) <= max_words:
        return [chunk]
    
    pieces = []
    for i in range(0, len(words), max_words - overlap):
        piece = words[i:i + max_words]
        if piece:
            pieces.append(' '.join(piece))
    
    return pieces


def create_faiss_index(documents, dimension=768, chunking_method='paragraphs', 
                       max_chunk_size=512, overlap=50, max_embedding_words=300, 
                       verbose=True):
    """
    Create FAISS index from documents with chunking.
    
    Args:
        documents (list): List of document dictionaries with 'content' key
        dimension (int): Embedding dimension (default 768 for nomic-embed-text)
        chunking_method (str): Method to chunk documents ('paragraphs', 'sentences', 'size')
        max_chunk_size (int): Maximum chunk size in words for chunking
        overlap (int): Number of overlapping words between chunks
        max_embedding_words (int): Maximum words for embedding model (default 300)
        verbose (bool): Print progress information
        
    Returns:
        tuple: (faiss_index, chunks_data, embeddings_array)
            - faiss_index: FAISS index object
            - chunks_data: List of chunk dictionaries with metadata
            - embeddings_array: Numpy array of embeddings
    """
    if verbose:
        print(f"Creating FAISS index with {chunking_method} chunking...")
        print(f"  - Max chunk size: {max_chunk_size} words")
        print(f"  - Max embedding size: {max_embedding_words} words")
    
    chunks_data = []
    embeddings_array = []
    failed_chunks = 0
    
    # Process each document
    for doc_idx, doc in enumerate(documents):
        if 'content' not in doc:
            raise ValueError("Each document must have a 'content' key")
        
        text = doc['content']
        doc_name = doc.get('name', f'doc_{doc_idx}')
        
        # Chunk the document based on selected method
        if chunking_method == 'paragraphs':
            chunks = chunk_by_paragraphs(text, max_chunk_size, overlap)
        elif chunking_method == 'sentences':
            chunks = chunk_by_sentences(text, max_chunk_size, overlap)
        elif chunking_method == 'size':
            chunks = chunk_by_size(text, max_chunk_size, overlap)
        else:
            raise ValueError(f"Unknown chunking method: {chunking_method}")
        
        # Generate embeddings for each chunk
        successful_chunks = 0
        for chunk_idx, chunk in enumerate(chunks):
            # Check if chunk is too long for embedding model
            chunk_words = len(chunk.split())
            
            if chunk_words > max_embedding_words:
                # Split into smaller pieces for embedding
                sub_chunks = _split_long_chunk(chunk, max_embedding_words, overlap//2)
                
                for sub_idx, sub_chunk in enumerate(sub_chunks):
                    try:
                        embedding = embed_text(sub_chunk)
                        embeddings_array.append(embedding)
                        
                        chunks_data.append({
                            'chunk_id': f"{doc_name}_{chunk_idx}_{sub_idx}",
                            'doc_name': doc_name,
                            'doc_index': doc_idx,
                            'chunk_index': chunk_idx,
                            'sub_chunk_index': sub_idx,
                            'text': sub_chunk,
                            'word_count': len(sub_chunk.split()),
                            'method': chunking_method,
                            'is_sub_chunk': True
                        })
                        successful_chunks += 1
                    except Exception as e:
                        if verbose:
                            print(f"Warning: Failed to embed sub-chunk {sub_idx} of chunk {chunk_idx} from {doc_name}: {str(e)[:60]}")
                        failed_chunks += 1
                        continue
            else:
                # Chunk is small enough, embed directly
                try:
                    embedding = embed_text(chunk)
                    embeddings_array.append(embedding)
                    
                    chunks_data.append({
                        'chunk_id': f"{doc_name}_{chunk_idx}",
                        'doc_name': doc_name,
                        'doc_index': doc_idx,
                        'chunk_index': chunk_idx,
                        'text': chunk,
                        'word_count': len(chunk.split()),
                        'method': chunking_method,
                        'is_sub_chunk': False
                    })
                    successful_chunks += 1
                except Exception as e:
                    if verbose:
                        print(f"Warning: Failed to embed chunk {chunk_idx} from {doc_name}: {str(e)[:60]}")
                    failed_chunks += 1
                    continue
        
        if verbose and successful_chunks > 0:
            print(f"  {doc_name}: Created {successful_chunks} chunks (from {len(chunks)} chunks)")
    
    if verbose:
        print(f"\nTotal: {len(chunks_data)} chunks embedded successfully")
        if failed_chunks > 0:
            print(f"Failed: {failed_chunks} chunks")
    
    # Check if we have embeddings
    if len(embeddings_array) == 0:
        raise RuntimeError("No embeddings were created. Check your documents and settings.")
    
    # Convert to numpy array
    embeddings_array = np.array(embeddings_array, dtype='float32')
    
    # Create FAISS index (L2 distance)
    index = faiss.IndexFlatL2(dimension)
    
    # Normalize embeddings for cosine similarity
    faiss.normalize_L2(embeddings_array)
    
    # Add embeddings to index
    index.add(embeddings_array)
    
    if verbose:
        print(f"✓ FAISS index created with {index.ntotal} vectors")
    
    return index, chunks_data, embeddings_array


def create_bm25_index(chunks_data, verbose=True):
    """
    Create BM25 index from chunks.
    
    Args:
        chunks_data (list): List of chunk dictionaries with 'text' key
        verbose (bool): Print progress information
        
    Returns:
        BM25Okapi: BM25 index object
    """
    corpus = [chunk['text'] for chunk in chunks_data]
    tokenized_corpus = [tokenize_en(text) for text in corpus]
    
    bm25 = BM25Okapi(tokenized_corpus)
    
    if verbose:
        print(f"✓ BM25 index created with {len(tokenized_corpus)} chunks")
    
    return bm25


def save_index(faiss_index, bm25_index, chunks_data, documents=None, output_dir="indexes", verbose=True):
    """
    Save FAISS and BM25 indexes to disk.
    
    Args:
        faiss_index: FAISS index object
        bm25_index: BM25 index object
        chunks_data (list): List of chunk dictionaries
        documents (list): List of original documents (optional)
        output_dir (str): Directory to save indexes
        verbose (bool): Print progress information
    """
    os.makedirs(output_dir, exist_ok=True)
    
    # Save FAISS index
    faiss.write_index(faiss_index, os.path.join(output_dir, "faiss.index"))
    
    # Save BM25 index
    with open(os.path.join(output_dir, "bm25.pkl"), "wb") as f:
        pickle.dump(bm25_index, f)
    
    # Save chunks data
    with open(os.path.join(output_dir, "chunks.pkl"), "wb") as f:
        pickle.dump(chunks_data, f)
    
    # Save documents if provided
    if documents is not None:
        with open(os.path.join(output_dir, "documents.pkl"), "wb") as f:
            pickle.dump(documents, f)
    
    if verbose:
        print(f"✓ Indexes saved to {output_dir}/")
        print(f"  - FAISS index: faiss.index")
        print(f"  - BM25 index: bm25.pkl")
        print(f"  - Chunks data: chunks.pkl ({len(chunks_data)} chunks)")
        if documents:
            print(f"  - Documents: documents.pkl ({len(documents)} documents)")


def load_index(index_dir="indexes", verbose=True):
    """
    Load FAISS and BM25 indexes from disk.
    
    Args:
        index_dir (str): Directory containing saved indexes
        verbose (bool): Print progress information
        
    Returns:
        tuple: (faiss_index, bm25_index, chunks_data, documents)
            - documents is None if not saved
    """
    # Load FAISS index
    faiss_index = faiss.read_index(os.path.join(index_dir, "faiss.index"))
    
    # Load BM25 index
    with open(os.path.join(index_dir, "bm25.pkl"), "rb") as f:
        bm25_index = pickle.load(f)
    
    # Load chunks data
    with open(os.path.join(index_dir, "chunks.pkl"), "rb") as f:
        chunks_data = pickle.load(f)
    
    # Load documents if they exist
    documents = None
    doc_path = os.path.join(index_dir, "documents.pkl")
    if os.path.exists(doc_path):
        with open(doc_path, "rb") as f:
            documents = pickle.load(f)
    
    if verbose:
        print(f"✓ Indexes loaded from {index_dir}/")
        print(f"  - FAISS vectors: {faiss_index.ntotal}")
        print(f"  - Chunks: {len(chunks_data)}")
        if documents:
            print(f"  - Documents: {len(documents)}")
    
    return faiss_index, bm25_index, chunks_data, documents


if __name__ == "__main__":
    # Configuration
    HTML_DIR = "ZebOS-XP_1.4_HTML/ZebOS-XP 1.4"
    OUTPUT_DIR = "indexes"
    CHUNKING_METHOD = "paragraphs"  # or "sentences", "size"
    MAX_CHUNK_SIZE = 512
    OVERLAP = 50
    MAX_EMBEDDING_WORDS = 300  # Max words for embedding model to handle
    
    print("=" * 70)
    print("BUILDING HYBRID SEARCH INDEX WITH CHUNKING")
    print("=" * 70)
    
    # Process documents
    print(f"\n1. Processing documents from {HTML_DIR}...")
    documents = process_documents(HTML_DIR)
    print(f"   ✓ Processed {len(documents)} documents")
    
    # Create FAISS index with chunking
    print(f"\n2. Creating FAISS index with {CHUNKING_METHOD} chunking...")
    print(f"   - Max chunk size: {MAX_CHUNK_SIZE} words")
    print(f"   - Overlap: {OVERLAP} words")
    print(f"   - Max embedding words: {MAX_EMBEDDING_WORDS} words")
    faiss_index, chunks_data, embeddings = create_faiss_index(
        documents,
        chunking_method=CHUNKING_METHOD,
        max_chunk_size=MAX_CHUNK_SIZE,
        overlap=OVERLAP,
        max_embedding_words=MAX_EMBEDDING_WORDS,
        verbose=True
    )
    
    # Create BM25 index on chunks
    print(f"\n3. Creating BM25 index...")
    bm25_index = create_bm25_index(chunks_data, verbose=True)
    
    # Save indexes
    print(f"\n4. Saving indexes to {OUTPUT_DIR}...")
    save_index(
        faiss_index, bm25_index, chunks_data, 
        documents=documents,
        output_dir=OUTPUT_DIR,
        verbose=True
    )
    
    # Print summary statistics
    print("\n" + "=" * 70)
    print("INDEX CREATION SUMMARY")
    print("=" * 70)
    print(f"Original documents: {len(documents)}")
    print(f"Total chunks: {len(chunks_data)}")
    print(f"FAISS vectors: {faiss_index.ntotal}")
    print(f"BM25 documents: {bm25_index.corpus_size}")
    if chunks_data:
        print(f"Average chunk size: {sum(c['word_count'] for c in chunks_data) / len(chunks_data):.1f} words")
    print(f"Chunking method: {CHUNKING_METHOD}")
    print("\n✓ Indexing complete!")
    print("=" * 70)