
from bm25.bm25 import BM25Okapi, tokenize_en
from bm25.embedding import embed_text
from bm25.main import load_index
import pickle
import faiss
import numpy as np
from typing import List, Dict, Tuple

def hybrid_search_en(
    query: str,
    bm25: BM25Okapi,
    faiss_index: faiss.IndexFlatL2,
    chunks_data: List[Dict],
    embeddings: np.ndarray,
    top_k: int = 10,
    alpha: float = 0.4
) -> List[Dict]:
    """
    Hybrid search combining BM25 and vector search.
    
    Args:
        query: Search query string
        bm25: BM25 index object
        faiss_index: FAISS index object
        chunks_data: List of chunk dictionaries with metadata
        embeddings: Numpy array of embeddings (for reference)
        top_k: Number of top results to return
        alpha: Weight for BM25 scores (1 - alpha for vector scores)
               alpha=0.4 means 40% BM25, 60% vector
    
    Returns:
        List of top_k chunks sorted by combined score
    """
    # BM25 search
    tokenized_query = tokenize_en(query)
    bm25_scores = bm25.get_scores(tokenized_query)
    
    # Vector search
    try:
        query_embedding = embed_text(query)
        query_embedding = np.array([query_embedding], dtype='float32')
        
        # Normalize for cosine similarity
        faiss.normalize_L2(query_embedding)
        
        # Search in FAISS
        vector_distances, vector_ids = faiss_index.search(
            query_embedding,
            min(top_k * 2, len(chunks_data))  # Get more candidates
        )
        
        # Convert distances to similarity scores
        # FAISS L2 distance: smaller is better, so we invert it
        # Both are 2D arrays with shape (1, k), so take first row
        vector_scores = 1.0 / (1.0 + vector_distances[0])
        vector_ids = vector_ids[0]
        
    except Exception as e:
        print(f"Warning: Vector search failed: {e}")
        # Fallback to BM25 only
        vector_ids = np.array([])
        vector_scores = np.array([])
    
    # Normalize BM25 scores
    if bm25_scores.max() > bm25_scores.min():
        bm25_norm = (bm25_scores - bm25_scores.min()) / (
            bm25_scores.max() - bm25_scores.min()
        )
    else:
        bm25_norm = bm25_scores
    
    # Combine scores
    score_map = {}
    if len(vector_ids) > 0:
        for idx, score in zip(vector_ids, vector_scores):
            score_map[int(idx)] = float(score)
    
    combined_scores = []
    for i, bm25_score in enumerate(bm25_norm):
        vector_score = score_map.get(i, 0.0)
        # Weighted combination
        combined_score = alpha * bm25_score + (1 - alpha) * vector_score
        combined_scores.append((i, combined_score, bm25_score, vector_score))
    
    # Sort by combined score
    combined_scores.sort(key=lambda x: x[1], reverse=True)
    
    # Return top_k results with scores
    results = []
    for rank, (idx, combined, bm25_s, vector_s) in enumerate(combined_scores[:top_k]):
        chunk = chunks_data[idx].copy()
        chunk['rank'] = rank + 1
        chunk['combined_score'] = round(combined, 4)
        chunk['bm25_score'] = round(bm25_s, 4)
        chunk['vector_score'] = round(vector_s, 4)
        results.append(chunk)
    
    return results


def search_with_indexes(
    query: str,
    index_dir: str = "indexes",
    top_k: int = 10,
    alpha: float = 0.4,
    verbose: bool = True
) -> List[Dict]:
    """
    Full search pipeline using saved indexes.
    
    Args:
        query: Search query string
        index_dir: Directory containing saved indexes
        top_k: Number of top results to return
        alpha: Weight for BM25 scores
        verbose: Print search information
    
    Returns:
        List of top_k search results
    """
    try:
        # Load indexes
        if verbose:
            print(f"Loading indexes from {index_dir}...")
        
        faiss_index, bm25_index, chunks_data, documents = load_index(
            index_dir, 
            verbose=verbose
        )
        
        if verbose:
            print(f"Performing hybrid search for query: '{query}'")
            print(f"Parameters: top_k={top_k}, alpha={alpha}")
        
        # Perform search
        results = hybrid_search_en(
            query,
            bm25_index,
            faiss_index,
            chunks_data,
            None,  # embeddings not needed for search
            top_k=top_k,
            alpha=alpha
        )
        
        return results
    
    except Exception as e:
        print(f"Error during search: {e}")
        import traceback
        traceback.print_exc()
        return []


def display_results(results: List[Dict], show_text_length: int = 200):
    """
    Display search results in a formatted way.
    
    Args:
        results: List of search results
        show_text_length: Number of characters to show from each result
    """
    if not results:
        print("No results found.")
        return
    
    print("\n" + "=" * 80)
    print(f"Search Results ({len(results)} matches)")
    print("=" * 80)
    
    for result in results:
        rank = result.get('rank', '?')
        doc_name = result.get('doc_name', 'unknown')
        chunk_id = result.get('chunk_id', 'unknown')
        combined_score = result.get('combined_score', 0)
        bm25_score = result.get('bm25_score', 0)
        vector_score = result.get('vector_score', 0)
        text = result.get('text', '')[:show_text_length]
        word_count = result.get('word_count', 0)
        
        print(f"\nResult {rank}: {doc_name} (Chunk: {chunk_id})")
        print(f"Scores - Combined: {combined_score}, BM25: {bm25_score}, Vector: {vector_score}")
        print(f"Length: {word_count} words")
        print(f"Text: {text}...")
    
    print("\n" + "=" * 80)


if __name__ == "__main__":
    # Example queries
    queries = [
        "AAA authentication",
        "BGP configuration",
        "VLAN settings"
    ]
    
    print("=" * 80)
    print("BM25 Hybrid Search Demo")
    print("=" * 80)
    
    for query in queries:
        print(f"\nSearching for: '{query}'")
        results = search_with_indexes(
            query,
            index_dir="indexes",
            top_k=25,
            alpha=0.4,
            verbose=False
        )
        display_results(results, show_text_length=1500)
        print()
