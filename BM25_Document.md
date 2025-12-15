# Tài Liệu Hệ Thống Tìm Kiếm Lai BM25

## Tổng Quan

Hệ thống này triển khai một framework tìm kiếm lai kết hợp BM25 (tìm kiếm dựa trên từ khóa) và tìm kiếm dựa trên embedding (tìm kiếm ngữ nghĩa) cho tài liệu ZebOS-XP. Hệ thống xử lý các tài liệu HTML, chia chúng thành các phần có thể quản lý được, và lập chỉ mục chúng bằng cả BM25 và tìm kiếm vector FAISS.

## Kiến Trúc Hệ Thống

Hệ thống bao gồm ba thành phần chính:

1. Xử Lý Tài Liệu: Trích xuất và chuẩn hóa văn bản từ các file HTML
2. Chia Nhỏ (Chunking): Chia tài liệu thành các phần có ý nghĩa ngữ nghĩa
3. Lập Chỉ Mục (Indexing): Tạo cả hai chỉ mục BM25 và FAISS cho tìm kiếm lai

## Các Thành Phần

### 1. Module Parse (bm25/parse.py)

Mục Đích: Trích xuất và chuẩn hóa văn bản từ các tài liệu HTML

Lớp Chính: CorpusParser

Mô Tả:
- Đọc các file HTML và trích xuất nội dung văn bản sạch
- Chuẩn hóa khoảng trắng và loại bỏ các thành phần HTML
- Xử lý các vấn đề liên quan đến mã hóa

Các Phương Thức Chính:
- parse(): Xử lý nội dung HTML
- get_corpus(): Trả về corpus đã trích xuất

### 2. Module Embedding (bm25/embedding.py)

Mục Đích: Tạo embedding và thực hiện chia nhỏ

Các Hàm Chính:

chunk_by_paragraphs(text, max_chunk_size, overlap):
- Chia văn bản theo ranh giới đoạn văn tự nhiên
- Duy trì ý nghĩa ngữ nghĩa
- Tham số:
  - text: Văn bản đầu vào
  - max_chunk_size: Số từ tối đa trên mỗi chunk (mặc định 512)
  - overlap: Số từ lặp lại giữa các chunks (mặc định 50)
- Trả về: Danh sách các phần văn bản

chunk_by_sentences(text, max_chunk_size, overlap):
- Chia văn bản theo ranh giới câu
- Hữu ích cho tài liệu kỹ thuật
- Cùng tham số với chunk_by_paragraphs
- Trả về: Danh sách các phần văn bản

chunk_by_size(text, max_chunk_size, overlap):
- Chia theo kích thước cố định
- Tham số:
  - text: Văn bản đầu vào
  - max_chunk_size: Số từ tối đa trên mỗi chunk
  - overlap: Số từ lặp lại giữa các chunks
- Trả về: Danh sách các phần văn bản

embed_text(text):
- Tạo embedding đơn lẻ bằng mô hình nomic-embed-text
- Sử dụng Ollama để tạo embedding cục bộ
- Tham số:
  - text: Văn bản cần embedding
- Trả về: Vector embedding (768 chiều)

embed_batch(texts):
- Tạo embedding cho nhiều văn bản
- Tham số:
  - texts: Danh sách các văn bản
- Trả về: Danh sách các vector embedding

chunk_and_embed(text, chunking_method, max_chunk_size, overlap):
- Kết hợp chia nhỏ và tạo embedding trong một bước
- Tham số:
  - text: Văn bản đầu vào
  - chunking_method: 'paragraphs', 'sentences', hoặc 'size'
  - max_chunk_size: Số từ tối đa trên mỗi chunk
  - overlap: Số từ lặp lại giữa các chunks
- Trả về: Danh sách các từ điển chứa chunk_id, text, embedding, word_count, method

### 3. Module BM25 (bm25/bm25.py)

Mục Đích: Triển khai tìm kiếm dựa trên từ khóa BM25

Lớp Chính: BM25Okapi

Mô Tả:
- Triển khai thuật toán xếp hạng BM25
- Tính điểm liên quan cho các truy vấn từ khóa
- Sử dụng cho tìm kiếm thưa thớt dựa trên từ khóa

Các Phương Thức Chính:
- get_scores(query_tokens): Trả về điểm BM25 cho truy vấn
- corpus_size: Thuộc tính cho số lượng tài liệu

Hàm Hỗ Trợ:
- tokenize_en(text): Tách từ cho văn bản tiếng Anh để dùng BM25

### 4. Module Chính (bm25/main.py)

Mục Đích: Điều phối xử lý tài liệu, lập chỉ mục và tìm kiếm

Các Hàm Chính:

process_documents(directory_path):
- Xử lý tất cả các file HTML trong một thư mục
- Tham số:
  - directory_path: Đường dẫn đến thư mục chứa file HTML
- Trả về: Danh sách các từ điển tài liệu với khóa 'content' và 'name'

_split_long_chunk(chunk, max_words, overlap):
- Chia các chunks vượt quá giới hạn của mô hình embedding
- Tham số:
  - chunk: Phần văn bản cần chia
  - max_words: Số từ tối đa trên mỗi phần (mặc định 300)
  - overlap: Số từ lặp lại giữa các phần (mặc định 30)
- Trả về: Danh sách các chunks nhỏ hơn

create_faiss_index(documents, dimension, chunking_method, max_chunk_size, overlap, max_embedding_words, verbose):
- Tạo chỉ mục FAISS từ các tài liệu
- Xử lý các chunks dài bằng cách chia chúng
- Tham số:
  - documents: Danh sách các từ điển tài liệu
  - dimension: Chiều của embedding (mặc định 768)
  - chunking_method: 'paragraphs', 'sentences', hoặc 'size'
  - max_chunk_size: Kích thước chunk tối đa theo từ (mặc định 512)
  - overlap: Số từ giữa các chunks (mặc định 50)
  - max_embedding_words: Số từ tối đa cho mô hình embedding (mặc định 300)
  - verbose: In thông tin tiến độ
- Trả về: Tuple của (faiss_index, chunks_data, embeddings_array)

create_bm25_index(chunks_data, verbose):
- Tạo chỉ mục BM25 từ dữ liệu chunks
- Tham số:
  - chunks_data: Danh sách các từ điển chunks
  - verbose: In thông tin tiến độ
- Trả về: Đối tượng chỉ mục BM25Okapi

save_index(faiss_index, bm25_index, chunks_data, documents, output_dir, verbose):
- Lưu các chỉ mục vào ổ đĩa
- Tham số:
  - faiss_index: Đối tượng chỉ mục FAISS
  - bm25_index: Đối tượng chỉ mục BM25
  - chunks_data: Danh sách các từ điển chunks
  - documents: Các tài liệu gốc (tùy chọn)
  - output_dir: Thư mục để lưu các chỉ mục
  - verbose: In thông tin tiến độ
- Lưu các file:
  - faiss.index: Chỉ mục vector FAISS
  - bm25.pkl: Chỉ mục BM25
  - chunks.pkl: Dữ liệu metadata và text của chunks
  - documents.pkl: Các tài liệu gốc (nếu được cung cấp)

load_index(index_dir, verbose):
- Tải các chỉ mục đã lưu từ ổ đĩa
- Tham số:
  - index_dir: Thư mục chứa các chỉ mục đã lưu
  - verbose: In thông tin tiến độ
- Trả về: Tuple của (faiss_index, bm25_index, chunks_data, documents)

## Luồng Dữ Liệu

1. Đầu Vào: Các tài liệu HTML trong thư mục ZebOS-XP_1.4_HTML/ZebOS-XP 1.4/

2. Xử Lý Tài Liệu:
   - Phân tích các file HTML
   - Trích xuất văn bản sạch
   - Tạo danh sách tài liệu với khóa 'content' và 'name'

3. Tạo Chỉ Mục FAISS:
   - Chia các tài liệu bằng phương pháp đã chọn
   - Với mỗi chunk:
     - Nếu chunk > 300 từ: chia thành các sub-chunks
     - Tạo embedding bằng mô hình nomic-embed-text
     - Lưu vào chỉ mục FAISS
   - Trả về chỉ mục, chunks_data, embeddings

4. Tạo Chỉ Mục BM25:
   - Tách từ cho mỗi text của chunk
   - Xây dựng chỉ mục BM25 từ corpus được tách từ

5. Lưu Chỉ Mục:
   - FAISS index vào faiss.index
   - BM25 index vào bm25.pkl (pickle hóa)
   - Dữ liệu chunk vào chunks.pkl (pickle hóa)
   - Các tài liệu gốc vào documents.pkl (tùy chọn)

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
