"""
BGE Reranker Module
Uses BAAI/bge-reranker-large for semantic reranking of search results
"""

from typing import List, Dict, Tuple
from transformers import AutoModelForSequenceClassification, AutoTokenizer
import torch
import numpy as np


class Reranker:
    """
    Reranker using BAAI/bge-reranker-large model.
    Scores query-document pairs for relevance ranking.
    """
    
    def __init__(self, model_name: str = 'BAAI/bge-reranker-large', device: str = None):
        """
        Initialize the BGE reranker.
        
        Args:
            model_name: HuggingFace model identifier
            device: Device to run model on ('cuda', 'cpu', or None for auto-detect)
        """
        self.model_name = model_name
        
        # Auto-detect device if not specified
        if device is None:
            # Check if CUDA is available
            if torch.cuda.is_available():
                try:
                    # Try to allocate small memory on GPU to verify it works
                    torch.zeros(1).cuda()
                    self.device = 'cuda'
                except Exception as e:
                    print(f"Warning: CUDA available but error occurred: {e}. Falling back to CPU.")
                    self.device = 'cpu'
            else:
                self.device = 'cpu'
        else:
            self.device = device
        
        print(f"Loading reranker model: {model_name} on {self.device}...")
        
        try:
            # Load model and tokenizer
            self.tokenizer = AutoTokenizer.from_pretrained(model_name)
            self.model = AutoModelForSequenceClassification.from_pretrained(model_name)
            self.model.to(self.device)
            self.model.eval()
            
            print(f"Reranker loaded successfully on {self.device}!")
        except Exception as e:
            print(f"Error loading model on {self.device}: {e}")
            if self.device == 'cuda':
                print("Retrying with CPU...")
                self.device = 'cpu'
                self.tokenizer = AutoTokenizer.from_pretrained(model_name)
                self.model = AutoModelForSequenceClassification.from_pretrained(model_name)
                self.model.to(self.device)
                self.model.eval()
                print(f"Reranker loaded successfully on CPU!")
    
    def _compute_score(self, query: str, document: str) -> float:
        """
        Compute relevance score for a query-document pair.
        
        Args:
            query: Search query
            document: Document text to score
        
        Returns:
            Relevance score (higher is better)
        """
        # Create query-document pair
        inputs = self.tokenizer(
            [query, document],
            padding=True,
            truncation=True,
            max_length=512,
            return_tensors='pt'
        ).to(self.device)
        
        # Get score from model
        with torch.no_grad():
            scores = self.model(**inputs, return_dict=True).logits.view(-1).float()
        
        return scores.cpu().item()
    
    def rerank(
        self, 
        query: str, 
        documents: List[Dict], 
        top_k: int = None,
        text_key: str = 'text'
    ) -> List[Dict]:
        """
        Rerank documents based on relevance to query.
        
        Args:
            query: Search query
            documents: List of document dictionaries
            top_k: Number of top results to return (None returns all)
            text_key: Key in document dict containing text to rerank
        
        Returns:
            Reranked list of documents with 'rerank_score' added
        """
        if not documents:
            return []
        
        print(f"Reranking {len(documents)} documents...")
        
        # Score each document
        scored_docs = []
        for idx, doc in enumerate(documents):
            text = doc.get(text_key, '')
            
            # Truncate very long texts
            if len(text) > 1000:
                text = text[:1000] + "..."
            
            score = self._compute_score(query, text)
            
            # Create new dict with rerank score
            doc_copy = doc.copy()
            doc_copy['rerank_score'] = round(float(score), 4)
            doc_copy['original_rank'] = idx + 1
            scored_docs.append(doc_copy)
        
        # Sort by rerank score (descending)
        scored_docs.sort(key=lambda x: x['rerank_score'], reverse=True)
        
        # Update ranks after reranking
        for new_idx, doc in enumerate(scored_docs):
            doc['new_rank'] = new_idx + 1
        
        # Return top_k if specified
        if top_k is not None:
            return scored_docs[:top_k]
        
        return scored_docs
    
    def rerank_batch(
        self,
        query: str,
        documents: List[Dict],
        batch_size: int = 8,
        top_k: int = None,
        text_key: str = 'text'
    ) -> List[Dict]:
        """
        Rerank documents in batches for better efficiency.
        
        Args:
            query: Search query
            documents: List of document dictionaries
            batch_size: Number of documents to process at once
            top_k: Number of top results to return
            text_key: Key in document dict containing text
        
        Returns:
            Reranked list of documents
        """
        if not documents:
            return []
        
        print(f"Batch reranking {len(documents)} documents (batch_size={batch_size})...")
        
        scored_docs = []
        
        # Reduce batch size if on GPU to avoid memory issues
        if self.device == 'cuda':
            batch_size = min(batch_size, 4)
        
        # Process in batches
        for i in range(0, len(documents), batch_size):
            batch = documents[i:i + batch_size]
            
            try:
                # Prepare pairs for batch processing
                pairs = []
                for doc in batch:
                    text = doc.get(text_key, '')
                    if len(text) > 1000:
                        text = text[:1000] + "..."
                    pairs.append([query, text])
                
                # Tokenize batch
                inputs = self.tokenizer(
                    pairs,
                    padding=True,
                    truncation=True,
                    max_length=512,
                    return_tensors='pt'
                ).to(self.device)
                
                # Get scores
                with torch.no_grad():
                    scores = self.model(**inputs, return_dict=True).logits.view(-1).float()
                
                # Add scores to documents
                for idx, (doc, score) in enumerate(zip(batch, scores)):
                    doc_copy = doc.copy()
                    doc_copy['rerank_score'] = round(float(score.cpu().item()), 4)
                    doc_copy['original_rank'] = i + idx + 1
                    scored_docs.append(doc_copy)
                    
            except RuntimeError as e:
                if "out of memory" in str(e).lower() or "cuda" in str(e).lower():
                    print(f"Memory error during reranking batch: {e}")
                    print("Falling back to smaller batch size or CPU processing")
                    # Fallback: score documents individually
                    for doc in batch:
                        text = doc.get(text_key, '')
                        if len(text) > 1000:
                            text = text[:1000] + "..."
                        try:
                            score = self._compute_score(query, text)
                            doc_copy = doc.copy()
                            doc_copy['rerank_score'] = round(score, 4)
                            doc_copy['original_rank'] = i + batch.index(doc) + 1
                            scored_docs.append(doc_copy)
                        except:
                            doc_copy = doc.copy()
                            doc_copy['rerank_score'] = 0.0
                            scored_docs.append(doc_copy)
                else:
                    raise
        
        # Sort by rerank score
        scored_docs.sort(key=lambda x: x['rerank_score'], reverse=True)
        
        # Update new ranks
        for new_idx, doc in enumerate(scored_docs):
            doc['new_rank'] = new_idx + 1
        
        if top_k is not None:
            return scored_docs[:top_k]
        
        #normalize scores
        max_score = max(doc['rerank_score'] for doc in scored_docs) if scored_docs else 1
        min_score = min(doc['rerank_score'] for doc in scored_docs) if scored_docs else 0
        score_range = max_score - min_score if max_score != min_score else 1
        for doc in scored_docs:
            doc['rerank_score'] = round((doc['rerank_score'] - min_score) / (score_range+1e-6), 4)
        


        return scored_docs


def display_rerank_results(results: List[Dict], show_text_length: int = 150):
    """
    Display reranked results in a formatted way.
    
    Args:
        results: List of reranked documents
        show_text_length: Number of characters to show from each result
    """
    if not results:
        print("No results to display.")
        return
    
    print("\n" + "=" * 80)
    print(f"Reranked Results ({len(results)} documents)")
    print("=" * 80)
    
    for result in results:
        new_rank = result.get('new_rank', '?')
        original_rank = result.get('original_rank', '?')
        rerank_score = result.get('rerank_score', 0)
        doc_name = result.get('doc_name', 'Unknown')
        text = result.get('text', '')[:show_text_length]
        
        # Show if ranking changed
        rank_change = ""
        if original_rank != '?' and new_rank != '?':
            change = original_rank - new_rank
            if change > 0:
                rank_change = f"↑{change}"
            elif change < 0:
                rank_change = f"↓{abs(change)}"
            else:
                rank_change = "="
        
        print(f"\nRank {new_rank} (was {original_rank} {rank_change})")
        print(f"Score: {rerank_score} | Doc: {doc_name}")
        print(f"Text: {text}...")
    
    print("\n" + "=" * 80)


if __name__ == "__main__":
    from agent.retriever import retriever
    
    # Example query
    query = "How do I configure OSPF on ZebOS?"
    
    print("=" * 80)
    print("BGE Reranker Demo")
    print("=" * 80)
    print(f"Query: {query}\n")
    
    # Get initial search results
    print("Step 1: Retrieving documents...")
    documents = retriever(query, top_k=10)
    
    if documents:
        print(f"Retrieved {len(documents)} documents\n")
        
        # Initialize reranker
        print("Step 2: Initializing reranker...")
        reranker = Reranker()
        
        # Rerank results
        print("\nStep 3: Reranking documents...")
        ranked_results = reranker.rerank_batch(
            query, 
            documents, 
            batch_size=8,
            top_k=5
        )
        
        # Display results
        print(ranked_results)
        print("\n" + "=" * 80)
        print("FINAL RESULTS")
        display_rerank_results(ranked_results, show_text_length=200)
    else:
        print("No documents retrieved!")