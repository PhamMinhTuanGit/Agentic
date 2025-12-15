# BM25 Hybrid Search System Documentation

## Overview

This system implements a hybrid search framework combining BM25 (keyword-based) and embedding-based (semantic) search for the ZebOS-XP documentation. The system processes HTML documents, chunks them into manageable pieces, and indexes them using both BM25 and FAISS vector search.

## System Architecture

The system consists of three main components:

1. Document Processing: Extract and normalize text from HTML files
2. Chunking: Split documents into semantically meaningful chunks
3. Indexing: Create both BM25 and FAISS indexes for hybrid search

## Components

### 1. Parse Module (bm25/parse.py)

Purpose: Extract and normalize text from HTML documents

Main Class: CorpusParser

Description:
- Reads HTML files and extracts clean text content
- Normalizes whitespace and removes HTML artifacts
- Handles encoding issues

Main Methods:
- parse(): Processes HTML content
- get_corpus(): Returns extracted corpus

### 2. Embedding Module (bm25/embedding.py)

Purpose: Generate embeddings and perform chunking

Main Functions:

chunk_by_paragraphs(text, max_chunk_size, overlap):
- Chunks text by natural paragraph boundaries
- Maintains semantic meaning
- Parameters:
  - text: Input text
  - max_chunk_size: Maximum words per chunk (default 512)
  - overlap: Words to repeat between chunks (default 50)
- Returns: List of text chunks

chunk_by_sentences(text, max_chunk_size, overlap):
- Chunks text by sentence boundaries
- Useful for technical documentation
- Same parameters as chunk_by_paragraphs
- Returns: List of text chunks

chunk_by_size(text, max_chunk_size, overlap):
- Simple fixed-size chunking
- Parameters:
  - text: Input text
  - max_chunk_size: Maximum words per chunk
  - overlap: Words to repeat between chunks
- Returns: List of text chunks

embed_text(text):
- Generates single embedding using nomic-embed-text model
- Uses Ollama for local embedding
- Parameters:
  - text: Text to embed
- Returns: Embedding vector (768 dimensions)

embed_batch(texts):
- Generates embeddings for multiple texts
- Parameters:
  - texts: List of texts
- Returns: List of embedding vectors

chunk_and_embed(text, chunking_method, max_chunk_size, overlap):
- Combines chunking and embedding in one step
- Parameters:
  - text: Input text
  - chunking_method: 'paragraphs', 'sentences', or 'size'
  - max_chunk_size: Maximum words per chunk
  - overlap: Words to repeat between chunks
- Returns: List of dictionaries with chunk_id, text, embedding, word_count, method

### 3. BM25 Module (bm25/bm25.py)

Purpose: Implement BM25 keyword-based search

Main Class: BM25Okapi

Description: 
- Implementation of BM25 ranking algorithm
- Calculates relevance scores for keyword queries
- Used for sparse, keyword-based search

Main Methods:
- get_scores(query_tokens): Returns BM25 scores for query
- corpus_size: Property for number of documents

Helper Function:
- tokenize_en(text): Tokenizes English text for BM25

### 4. Main Module (bm25/main.py)

Purpose: Orchestrate document processing, indexing, and search

Main Functions:

process_documents(directory_path):
- Processes all HTML files in a directory
- Parameters:
  - directory_path: Path to directory with HTML files
- Returns: List of document dictionaries with 'content' and 'name' keys

_split_long_chunk(chunk, max_words, overlap):
- Splits chunks that exceed embedding model limits
- Parameters:
  - chunk: Text chunk to split
  - max_words: Maximum words per piece (default 300)
  - overlap: Words to repeat between pieces (default 30)
- Returns: List of smaller chunks

create_faiss_index(documents, dimension, chunking_method, max_chunk_size, overlap, max_embedding_words, verbose):
- Creates FAISS index from documents
- Handles long chunks by splitting them
- Parameters:
  - documents: List of document dictionaries
  - dimension: Embedding dimension (default 768)
  - chunking_method: 'paragraphs', 'sentences', or 'size'
  - max_chunk_size: Maximum chunk size in words (default 512)
  - overlap: Words between chunks (default 50)
  - max_embedding_words: Maximum words for embedding model (default 300)
  - verbose: Print progress information
- Returns: Tuple of (faiss_index, chunks_data, embeddings_array)

create_bm25_index(chunks_data, verbose):
- Creates BM25 index from chunk data
- Parameters:
  - chunks_data: List of chunk dictionaries
  - verbose: Print progress information
- Returns: BM25Okapi index object

save_index(faiss_index, bm25_index, chunks_data, documents, output_dir, verbose):
- Saves indexes to disk
- Parameters:
  - faiss_index: FAISS index object
  - bm25_index: BM25 index object
  - chunks_data: List of chunk dictionaries
  - documents: Original documents (optional)
  - output_dir: Directory to save indexes
  - verbose: Print progress information
- Saves files:
  - faiss.index: FAISS vector index
  - bm25.pkl: BM25 index
  - chunks.pkl: Chunk metadata and text
  - documents.pkl: Original documents (if provided)

load_index(index_dir, verbose):
- Loads previously saved indexes from disk
- Parameters:
  - index_dir: Directory containing saved indexes
  - verbose: Print progress information
- Returns: Tuple of (faiss_index, bm25_index, chunks_data, documents)

## Data Flow

1. Input: HTML documents in ZebOS-XP_1.4_HTML/ZebOS-XP 1.4/ directory

2. Process Documents:
   - Parse HTML files
   - Extract clean text
   - Create document list with 'content' and 'name' keys

3. Create FAISS Index:
   - Chunk documents using selected method
   - For each chunk:
     - If chunk > 300 words: split into sub-chunks
     - Generate embedding using nomic-embed-text model
     - Store in FAISS index
   - Return index, chunks_data, embeddings

4. Create BM25 Index:
   - Tokenize each chunk text
   - Build BM25 index from tokenized corpus

5. Save Indexes:
   - FAISS index to faiss.index
   - BM25 index to bm25.pkl (pickled)
   - Chunk metadata to chunks.pkl (pickled)
   - Original documents to documents.pkl (optional)

## Chunk Metadata Structure

Each chunk stores the following metadata:

chunk_id: Unique identifier (format: doc_name_chunk_idx or doc_name_chunk_idx_sub_idx)
doc_name: Original document name
doc_index: Index in document list
chunk_index: Index of chunk within document
sub_chunk_index: Index of sub-chunk (if split for embedding)
text: Actual chunk text
word_count: Number of words in chunk
method: Chunking method used ('paragraphs', 'sentences', or 'size')
is_sub_chunk: Boolean indicating if this is a sub-chunk

## Chunking Methods Comparison

Paragraphs Method:
- Splits at double newlines
- Preserves semantic boundaries
- Best for: Mixed content, technical docs
- Advantages: Maintains context and meaning
- Disadvantages: Uneven chunk sizes

Sentences Method:
- Splits at sentence boundaries
- More uniform chunks
- Best for: Highly structured text, API documentation
- Advantages: Complete sentences preserve grammar
- Disadvantages: May break logical groupings

Size Method:
- Fixed word count per chunk
- Most uniform chunks
- Best for: Large-scale processing
- Advantages: Predictable sizes
- Disadvantages: May split sentences or paragraphs

## Configuration Parameters

HTML_DIR: Path to HTML documents (default: ZebOS-XP_1.4_HTML/ZebOS-XP 1.4)
OUTPUT_DIR: Directory to save indexes (default: indexes)
CHUNKING_METHOD: Method for chunking (default: paragraphs)
MAX_CHUNK_SIZE: Maximum words per chunk (default: 512)
OVERLAP: Words to repeat between chunks (default: 50)
MAX_EMBEDDING_WORDS: Maximum words for embedding model (default: 300)
EMBEDDING_DIMENSION: Dimension of embeddings (default: 768)

## Performance Characteristics

Document Processing:
- Speed: Depends on number and size of HTML files
- Memory: Proportional to total document size

Chunking:
- Speed: Fast (linear in text size)
- Method overhead: Paragraphs < Sentences < Size
- Typical: ~1000 chunks per MB of text

Embedding:
- Speed: Depends on model and hardware
- Model: nomic-embed-text via Ollama
- Dimension: 768
- Typical: ~50-200 chunks per second (varies with system)

FAISS Indexing:
- Speed: Fast (linear in number of vectors)
- Memory: ~768 floats * 4 bytes * num_chunks = ~3KB per chunk
- Search: Milliseconds per query

BM25 Indexing:
- Speed: Fast (linear in vocabulary size)
- Memory: Small (vocabulary and IDF values)
- Search: Fast (milliseconds per query)

## Error Handling

The system implements graceful error handling:

Long Chunks:
- Chunks exceeding MAX_EMBEDDING_WORDS are automatically split
- Sub-chunks are embedded individually
- Failed chunks are skipped with warning

Embedding Errors:
- Network/model errors are caught and reported
- Problematic chunks are skipped
- Processing continues with remaining chunks

File I/O:
- Missing directories are created automatically
- Existing index files are overwritten
- Load errors are reported with guidance

## Usage Example

Basic Usage:

```python
from bm25.main import (
    process_documents, 
    create_faiss_index, 
    create_bm25_index,
    save_index,
    load_index
)

# Configuration
HTML_DIR = "ZebOS-XP_1.4_HTML/ZebOS-XP 1.4"
OUTPUT_DIR = "indexes"

# Step 1: Process documents
documents = process_documents(HTML_DIR)

# Step 2: Create FAISS index
faiss_index, chunks_data, embeddings = create_faiss_index(
    documents,
    chunking_method='paragraphs',
    max_chunk_size=512,
    overlap=50,
    max_embedding_words=300,
    verbose=True
)

# Step 3: Create BM25 index
bm25_index = create_bm25_index(chunks_data, verbose=True)

# Step 4: Save indexes
save_index(
    faiss_index, 
    bm25_index, 
    chunks_data,
    documents=documents,
    output_dir=OUTPUT_DIR,
    verbose=True
)

# Later: Load indexes
faiss_index, bm25_index, chunks_data, documents = load_index(OUTPUT_DIR)
```

Running Full Pipeline:

```bash
python3 -m bm25.main
```

This will:
1. Process all HTML files from HTML_DIR
2. Create FAISS and BM25 indexes
3. Save indexes to OUTPUT_DIR
4. Print summary statistics

## File Structure

Working Directory:
/home/tuanpm/work/Agentic/

Key Files:
- bm25/parse.py: Document parsing
- bm25/embedding.py: Chunking and embedding
- bm25/bm25.py: BM25 implementation
- bm25/main.py: Main orchestration logic
- ZebOS-XP_1.4_HTML/: Source HTML documentation
- indexes/: Saved indexes directory (created on first run)

Output Files (in indexes/):
- faiss.index: FAISS vector index
- bm25.pkl: BM25 index (pickled)
- chunks.pkl: Chunk data (pickled)
- documents.pkl: Original documents (pickled)

## Dependencies

Core Libraries:
- faiss: Vector search library
- ollama: Local embedding model interface
- numpy: Numerical operations
- beautifulsoup4: HTML parsing

Python Standard Library:
- os: File operations
- re: Regular expressions
- pathlib: Path operations
- pickle: Serialization

## Future Enhancements

Possible improvements:
- Support for additional chunking strategies
- Multiple embedding models
- Distributed indexing for large datasets
- Real-time index updates
- Advanced search features (filtering, ranking)
- Query expansion and refinement
- Caching and performance optimization

## Troubleshooting

Issue: "input length exceeds the context length" error
Solution: MAX_EMBEDDING_WORDS parameter limits chunk size. Default is 300 words. The system automatically splits longer chunks.

Issue: Out of memory during indexing
Solution: Reduce MAX_CHUNK_SIZE or process documents in batches

Issue: Slow embedding generation
Solution: Check Ollama service is running. Consider hardware acceleration (GPU).

Issue: No embeddings created
Solution: Verify HTML_DIR path exists and contains HTML files. Check HTML files contain text content.

## Contact and Support

For issues or questions, refer to the inline documentation in each module.
