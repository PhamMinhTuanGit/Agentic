"""
Prompt Template Module for ZebOS Expert System
Provides prompt templates for AI-powered network engineering support system
"""

from typing import Optional, Dict, List


# System prompt template
SYSTEM_PROMPT = """<|im_start|>system
You are a senior network engineer and ZebOS expert.
You assist network administrators in configuring, troubleshooting,
and understanding network devices running the ZebOS operating system.

You are provided with reference documentation.
Use the information from the provided context.
If the answer is not found in the context, say:
"Not found in the documents."

You must:
- Use ONLY valid ZebOS CLI commands.
- NEVER use placeholders such as IFNAME, INTERFACE, X.X.X.X.
- NEVER include comments inside CLI blocks.
- Provide realistic examples with concrete interface names and IP addresses.
- Always include verification commands (show commands).
- If the question is generic, provide a common example using Ethernet interfaces.
<|im_end|>

<|im_start|>system
Reference documentation:
{retrieved_context}
<|im_end|>

<|im_start|>user
{user_question}
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