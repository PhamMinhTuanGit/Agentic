"""
Prompt Template Module for ZebOS Expert System
Provides prompt templates for AI-powered network engineering support system
"""

from typing import Optional, Dict, List
from sqlalchemy.orm import Session as DBSession


# System prompt template
SYSTEM_PROMPT = """<|im_start|>system
You are a senior network engineer and ZebOS expert.
You assist network administrators in configuring, troubleshooting,
and understanding network devices running the ZebOS operating system.

You are provided with reference documentation.
Use the information from the provided context.
Combine your networking expertise with the documentation to answer user questions accurately.
If the answer is not found in the context, say:
"Not found in the documents."

You must:
- Use ONLY valid ZebOS CLI commands.
- NEVER use placeholders such as IFNAME, INTERFACE, X.X.X.X.
- NEVER include comments inside CLI blocks.
- Provide realistic examples with concrete interface names and IP addresses.
- Always include verification commands (show commands).
- If the question is generic, provide a common example using Ethernet interfaces.
- Keep the reasoning under 200 words.
<|im_end|>

<|im_start|>system
Reference documentation:
{retrieved_context}
<|im_end|>

<|im_start|>system
Historical conversation (if any) is below:
{history_stm_context}
{history_ltm_context}
<|im_end|>

<|im_start|>user
{user_question}
<|im_end|>

<|im_start|>assistant
"""

RERANK_PROMPT = """<|im_start|>system
You are a strict technical reranker for a Retrieval-Augmented Generation (RAG) system.
Your task is to evaluate candidate context chunks for answering network configuration
questions related to devices running the ZebOS operating system.

Evaluation rules (VERY IMPORTANT):
1. Prefer chunks that contain VALID and REALISTIC ZebOS CLI commands.
3. Prefer chunks that:
   - Include both configuration commands and verification ("show") commands.
   - Follow the correct CLI flow (enable → configure terminal → feature config).
4. If a chunk is ambiguous or partially incorrect, rank it lower instead of rejecting it.
5. Do NOT invent or correct commands. Only judge relevance and correctness.

Scoring:
- Score each chunk from 0 to 100.
- 100 = highly relevant, correct, and safe for production use.
- 0 = irrelevant or clearly incorrect.

Output format:
You must return ONLY a JSON array.
Each element must contain:
{
  "chunk_id": <number>,
  "score": <number>,
  "reason": "<short explanation>"
}

Do NOT include any additional text outside the JSON.
Default language for reasons: English.
<|im_end|>

<|im_start|>user
User question:
{user_question}

Candidate context chunks:
{candidate_chunks}
<|im_end|>

<|im_start|>assistant
"""


class PromptTemplate:
    """
    Manages prompts for the ZebOS Expert System.
    Provides methods to construct prompts with different formats and contexts.
    """
    
    def __init__(self, system_prompt: str = SYSTEM_PROMPT):
        """
        Initialize the prompt template.
        
        Args:
            system_prompt: System prompt to use, defaults to SYSTEM_PROMPT
        """
        self.system_prompt = system_prompt
    
    def create_query_prompt(self, query: str, context: Optional[str] = None) -> str:
        """
        Create a prompt for a single user query with optional context.
        
        Args:
            query: User question or query
            context: Additional context or reference documentation (optional)
        
        Returns:
            Complete prompt ready to send to the model
        """
        prompt = self.system_prompt
        
        if context:
            # Replace placeholder with actual context
            prompt = prompt.replace("{retrieved_context}", context)
        else:
            prompt = prompt.replace("{retrieved_context}", "No context provided.")
        
        # Replace user question placeholder
        prompt = prompt.replace("{user_question}", query)
        
        return prompt
    
    def create_multi_turn_prompt(
        self, 
        history: List[Dict[str, str]], 
        current_query: str,
        context: Optional[str] = None
    ) -> str:
        """
        Create a prompt for multi-turn conversation.
        
        Args:
            history: Conversation history, each element has {'user': ..., 'assistant': ...}
            current_query: Current user question
            context: Additional context or reference documentation (optional)
        
        Returns:
            Complete prompt for multi-turn conversation
        """
        prompt = self.system_prompt
        
        if context:
            prompt = prompt.replace("{retrieved_context}", context)
        else:
            prompt = prompt.replace("{retrieved_context}", "No context provided.")
        
        # Add conversation history
        for turn in history:
            if 'user' in turn:
                prompt += f"\n\n<|im_start|>user\n{turn['user']}\n<|im_end|>"
            if 'assistant' in turn:
                prompt += f"\n\n<|im_start|>assistant\n{turn['assistant']}\n<|im_end|>"
        
        # Add current question
        prompt = prompt.replace("{user_question}", current_query)
        
        return prompt
    
    def create_search_augmented_prompt(
        self,
        query: str,
        search_results: List[Dict],
        max_results: int = 3
    ) -> str:
        """
        Create a prompt augmented with search results.
        Integrates search results from FAISS/BM25 as context.
        
        Args:
            query: User question
            search_results: List of search results from hybrid search
            max_results: Maximum number of results to include
        
        Returns:
            Prompt with context from ZebOS documentation
        """
        # Build context from search results
        context_parts = []
        for i, result in enumerate(search_results[:max_results], 1):
            doc_name = result.get('doc_name', 'Unknown')
            text = result.get('text', '')  # Limit to 400 characters
            score = result.get('combined_score', 0)
            
            context_parts.append(
                f"[Document {i}] {doc_name} (Relevance: {score})\n{text}"
            )
        
        context = "\n\n".join(context_parts)
        
        return self.create_query_prompt(query, context)
    
    
    def format(self, **kwargs) -> str:
        """
        Format template with provided parameters.
        Backward compatible with old code.
        
        Args:
            **kwargs: Parameters to format the template
                - retrieved_context: Reference documentation
                - user_question: User's question
        
        Returns:
            Formatted prompt template
        """
        prompt = self.system_prompt
        
        if 'retrieved_context' in kwargs:
            prompt = prompt.replace("{retrieved_context}", kwargs['retrieved_context'])
        
        if 'user_question' in kwargs:
            prompt = prompt.replace("{user_question}", kwargs['user_question'])
        
        # Handle legacy parameter names
        if 'context' in kwargs:
            prompt = prompt.replace("{retrieved_context}", kwargs['context'])
        
        if 'query' in kwargs:
            prompt = prompt.replace("{user_question}", kwargs['query'])
        
        return prompt

class RerankPromptTemplate(PromptTemplate):
    """
    Prompt template for reranking retrieved chunks.
    Evaluates and scores candidate context chunks for relevance.
    """
    
    def __init__(self):
        """Initialize rerank prompt template."""
        super().__init__(RERANK_PROMPT)
    
    def create_rerank_prompt(
        self,
        user_question: str,
        candidate_chunks: List[Dict]
    ) -> str:
        """
        Create a prompt for reranking candidate chunks.
        
        Args:
            user_question: The user's question
            candidate_chunks: List of candidate chunks to evaluate
                Each chunk should have: {'chunk_id': int, 'text': str, ...}
        
        Returns:
            Complete rerank prompt ready for the model
        """
        # Format candidate chunks for the prompt
        chunks_text = []
        for chunk in candidate_chunks:
            chunk_id = chunk.get('chunk_id', chunk.get('id', 0))
            text = chunk.get('text', chunk.get('content', ''))
            doc_name = chunk.get('doc_name', 'Unknown')
            
            chunks_text.append(
                f"Chunk ID: {chunk_id}\n"
                f"Source: {doc_name}\n"
                f"Content:\n{text}\n"
            )
        
        formatted_chunks = "\n---\n".join(chunks_text)
        
        # Replace placeholders
        prompt = self.system_prompt
        prompt = prompt.replace("{user_question}", user_question)
        prompt = prompt.replace("{candidate_chunks}", formatted_chunks)
        
        return prompt
    
    def format(self, **kwargs) -> str:
        """
        Format rerank template with provided parameters.
        
        Args:
            **kwargs: Parameters to format the template
                - user_question: User's question
                - candidate_chunks: List of chunks to rerank
        
        Returns:
            Formatted rerank prompt
        """
        if 'user_question' in kwargs and 'candidate_chunks' in kwargs:
            return self.create_rerank_prompt(
                kwargs['user_question'],
                kwargs['candidate_chunks']
            )
        
        # Fallback to simple replacement
        prompt = self.system_prompt
        for key, value in kwargs.items():
            prompt = prompt.replace(f"{{{key}}}", str(value))
        
        return prompt


class FullPromptTemplate(PromptTemplate):
    """
    Full prompt template including both query and search context.
    Combines user question with retrieved documents for comprehensive prompts.
    """
    def __init__(self, db: DBSession, max_stm: int = 6, system_prompt: str = SYSTEM_PROMPT, max_results: int = 3):
        """
        Initialize full prompt template with database session.
        
        Args:
            db: Database session for retrieval
        """
        super().__init__(SYSTEM_PROMPT)
        self.db = db
    def create_full_prompt(
        self,
        query: str,
        search_results: List[Dict],
        max_results: int = 3,

    ) -> str:
        """
        Create a full prompt with search-augmented context.
        
        Args:
            query: User question
            search_results: List of search results from hybrid search
            max_results: Maximum number of results to include
        
        Returns:
            Complete prompt with integrated search context
        """
        return self.create_search_augmented_prompt(
            query,
            search_results,
            max_results
        )


# Utility functions
def build_prompt(
    query: str, 
    context: Optional[str] = None,
    system_prompt: str = SYSTEM_PROMPT
) -> str:
    """
    Quick utility function to create a prompt.
    
    Args:
        query: User question
        context: Optional context or reference documentation
        system_prompt: Custom system prompt (optional)
    
    Returns:
        Complete prompt ready for the model
    """
    template = PromptTemplate(system_prompt)
    return template.create_query_prompt(query, context)


def build_search_prompt(
    query: str,
    search_results: List[Dict],
    max_results: int = 3,
    system_prompt: str = SYSTEM_PROMPT
) -> str:
    """
    Quick utility function to create a search-augmented prompt.
    
    Args:
        query: User question
        search_results: Results from hybrid search (BM25 + FAISS)
        max_results: Maximum search results to include
        system_prompt: Custom system prompt (optional)
    
    Returns:
        Complete prompt with search context
    """
    template = PromptTemplate(system_prompt)
    return template.create_search_augmented_prompt(query, search_results, max_results)

def build_summarize_prompt(
    messages: List[str],
    system_prompt: Optional[str] = None
) -> str:
    """
    Quick utility function to create a prompt for summarizing chat history.
    Focuses on the 5 most recent messages.
    
    Args:
        messages: List of messages to summarize (will use last 5)
        system_prompt: Custom system prompt (optional)
    
    Returns:
        Complete prompt for summarizing chat history
    """
    # Take only the last 5 messages
    recent_messages = messages[-5:] if len(messages) > 5 else messages
    
    # Custom system prompt for summarization
    if system_prompt is None:
        system_prompt = """<|im_start|>system
You are a helpful assistant that summarizes chat conversations.
Create a concise summary of the chat history, focusing on:
- Main topics discussed
- Key technical questions asked
- Important configurations or commands mentioned
Keep the summary brief and informative.
<|im_end|>

<|im_start|>user
{user_question}
<|im_end|>

<|im_start|>assistant
"""
    
    # Format messages for context
    formatted_messages = []
    for i, msg in enumerate(recent_messages, 1):
        formatted_messages.append(f"Message {i}: {msg}")
    
    summary_context = "\n".join(formatted_messages)
    
    template = PromptTemplate(system_prompt)
    return template.create_query_prompt(
        f"Summarize the following {len(recent_messages)} most recent chat messages:\n\n{summary_context}",
        context=None
    )


if __name__ == "__main__":
    # Example usage
    template = PromptTemplate()
    
    # Example 1: Simple prompt
    print("=" * 80)
    print("Example 1: Simple Query Prompt")
    print("=" * 80)
    prompt = template.create_query_prompt(
        "How do I configure AAA authentication on ZebOS?"
    )
    print(prompt)
    
    # # Example 2: Prompt with context
    # print("\n" + "=" * 80)
    # print("Example 2: Query Prompt with Context")
    # print("=" * 80)
    # context = "Device: Zebra Z5000, ZebOS version 5.10"
    # prompt = template.create_query_prompt(
    #     "How do I enable BGP?",
    #     context
    # )
    # print(prompt[:250] + "...")
    
    # # Example 3: Multi-turn conversation
    # print("\n" + "=" * 80)
    # print("Example 3: Multi-turn Conversation")
    # print("=" * 80)
    # history = [
    #     {
    #         "user": "How do I configure OSPF?",
    #         "assistant": "To configure OSPF on ZebOS, follow these steps: ..."
    #     }
    # ]
    # prompt = template.create_multi_turn_prompt(
    #     history,
    #     "And how do I set the hello interval?"
    # )
    # print(prompt[:250] + "...")