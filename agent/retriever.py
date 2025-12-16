from bm25.search import hybrid_search_en, search_with_indexes
import ollama
from agent.prompt_template import SYSTEM_PROMPT, PromptTemplate
from agent.reranker import Reranker

def retriever(query, top_k=25):
    results = search_with_indexes(
        query,
        index_dir="indexes",
        top_k=top_k,
        alpha=0.4,        
        verbose=True
    )
    return results
def construct_prompt(query, results):
    template = PromptTemplate()
    prompt = template.create_search_augmented_prompt(
        query,
        results,
        max_results=10
    )
    return prompt

def model_response(prompt):
    model = ollama.Client()
    response = model.generate(prompt=prompt, model='qwen3:4b')    
    return response


def retriever_with_rerank(query, top_k=25, rerank_top_k=10):
    """
    Retrieve and rerank documents for a query.
    
    Args:
        query: Search query
        top_k: Number of initial documents to retrieve
        rerank_top_k: Number of top reranked documents to return
    
    Returns:
        List of reranked documents
    """
    
    # Step 1: Initial retrieval
    print(f"Retrieving top {top_k} documents...")
    results = search_with_indexes(
        query,
        index_dir="indexes",
        top_k=top_k,
        alpha=0.4,        
        verbose=True
    )
    
    if not results:
        return []
    
    # Step 2: Rerank results
    print(f"\nReranking to top {rerank_top_k}...")
    reranker = Reranker()
    reranked_results = reranker.rerank_batch(
        query,
        results,
        batch_size=8,
        top_k=rerank_top_k
    )
    
    return reranked_results

def pipeline(query):
    # Retrieve and rerank documents
    reranked_results = retriever_with_rerank(query)
    
    # Construct prompt
    prompt = construct_prompt(query, reranked_results)
    
    # Get model response
    response = model_response(prompt)
    
    return {
        "prompt": prompt,
        "response": response
    }


if __name__ == "__main__":
    query = "How do I configure multiple OSPF processes on ZebOS?"
    results = retriever_with_rerank(query)
    prompt = construct_prompt(query, results)
    print("=== Prompt ===")
    print(prompt)
    print("=== Model Response ===")
    response = model_response(prompt)
    print(response['response'])

    