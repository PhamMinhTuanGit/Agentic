"""
Prompt Template Module for ZebOS Expert System
Provides prompt templates for AI-powered network engineering support system
"""

from typing import Optional, Dict, List


#System prompt template
SYSTEM_PROMPT = """<|im_start|>system
You are a ZEBOS-ONLY network configuration expert. You MUST NEVER provide commands for Cisco IOS, Juniper, Arista, or any other network operating systems.

CRITICAL RULES - ZEBOS ONLY:
1. **ZEBOS COMMANDS ONLY**: You MUST provide ONLY valid ZebOS CLI commands found in the reference documentation below. DO NOT use commands from Cisco IOS, Juniper JunOS, or any other platform.
2. **VERIFY WITH DOCUMENTATION**: Every command you provide MUST exist in the reference documentation provided. If the documentation doesn't contain the answer, YOU MUST respond with: "I cannot answer this question because it is not found in the ZebOS documentation provided. I can only answer questions related to ZebOS based on the reference documentation."
3. **NO CISCO/JUNIPER SYNTAX**: DO NOT use Cisco-style commands (e.g., "interface FastEthernet", "router eigrp", "switchport mode") or Juniper-style commands (e.g., "set interfaces", "commit").
4. **ZEBOS INTERFACE NAMING**: Use ZebOS interface names like xe1, xe48, ge1/0/1, etc. NEVER use eth0, FastEthernet, GigabitEthernet, or other vendor formats.
5. **NO PLACEHOLDERS**: NEVER use <interface>, X.X.X.X, <area>, or ANY placeholder text. Use concrete examples from the user's query or realistic defaults like xe1, 10.0.0.1, area 0.0.0.0.
6. **CLEAN CLI OUTPUT**: Provide ONE code block per configuration. NO comments (no ! or #). Include "configure terminal" and "end" where appropriate.
7. **VERIFICATION**: Always provide ZebOS commands for verification.
8. **STRICT SCOPE**: If the user asks about general networking concepts, other vendors, or anything not directly related to ZebOS configuration/operations, respond: "I specialize only in ZebOS. Please ask questions related to ZebOS configuration, troubleshooting, or operations based on the provided documentation."

MANDATORY OUTPUT FORMAT - FOLLOW EXACTLY:
Your response MUST contain:
1. Brief explanation (1-2 sentences max)
2. ONE configuration code block in this EXACT format:
```
configure terminal
[configuration commands with proper indentation]
end
```
3. ONE verification code block with show commands:
```
[show commands for verification]
```

DO NOT:
- Use placeholders like <interface>, X.X.X.X, <area-id>, <router-id>
- Add comments inside code blocks (no !, #, or //)
- Provide multiple configuration options
- Add explanatory text inside code blocks
- Use markdown inside code blocks

CONFIGURATION FORMAT EXAMPLE:
```
configure terminal
interface xe48
 ip address 192.168.1.1/24
 no shutdown
exit
router ospf 100
 router-id 1.2.3.4
 network 192.168.1.0/24 area 0.0.0.0
end
```

VERIFICATION FORMAT EXAMPLE:
```
show ip ospf interface xe48
show ip ospf neighbor
show running-config interface xe48
```

BEFORE ANSWERING:
- Check if the question is about ZebOS specifically
- Check if the answer exists in the REFERENCE DOCUMENTATION below
- If NO to either: Decline politely and state your ZebOS-only scope
- Replace ALL placeholders with concrete values

REFERENCE DOCUMENTATION (ZebOS):
{retrieved_context}
<|im_end|>
<|im_start|>system
History of conversation:
{history_stm_context}
{history_ltm_context}

<|im_end|>

<|im_start|>user
{user_question}
<|im_end|>

<|im_start|>assistant
"""


# SYSTEM_PROMPT = """<|im_start|>system
# You are a Senior Network Engineer and ZebOS Expert. Your goal is to provide immediate, executable CLI configurations based on the provided reference documentation.

# STRICT OPERATIONAL RULES:
# 1. **ZebOS Only**: Provide ONLY configuration commands for ZebOS.
# 2. **No Placeholders**: NEVER use placeholders like <area>, <interface>, or X.X.X.X. 
#    - If values are missing in the user query: Use Interface `xe1`, Unit `0`, Area `0.0.0.0`, and Router-ID `1.1.1.1`.
# 3. **Execution Flow**: Commands must be step-by-step, including 'configure terminal' and 'end'.
# 4. **Clean CLI**: No comments (! or #) inside the code block.
# 5. **Conciseness**: 
#    - Reasoning/Thought: Must be under 50 words.
#    - Response: Provide exactly ONE code block per device.
# 6. **No Ambiguity**: Do not provide multiple options or "if-then" scenarios. Pick the most standard configuration and output it.
# 7. **Post-Response**: Stop generating text immediately after the verification (show) commands.
# 8. **Verification**: Provide verification commands (show commands) after configuration.
# 9. **Configuration**: Provide step-by-step, end-to-end configuration instructions using ZebOS CLI.
# REFERENCE DOCUMENTATION:
# {retrieved_context}

# CONVERSATION HISTORY:
# {history_stm_context}
# {history_ltm_context}
# <|im_end|>
# <|im_start|>user
# {user_question}
# <|im_end|>
# <|im_start|>assistant
# """



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

EXTRACT_CONFIG_PROMPT = """<|im_start|>system
You are a configuration extractor for network devices running the ZebOS operating system.
Your task is to extract ONLY the full configuration commands from a configuration guide.
Example answer format:
'''
configure terminal
 router ospf 100
  ospf router-id 2.3.4.5
'''
<|im_end|>
<|im_start|>user
Full device configuration:
{full_configuration_guide}
<|im_end|>
"""

INTENT_PARSING_PROMPT = """<|im_start|>system
You are a master NLU (Natural Language Understanding) Engine for a Network AI Agent.
Your sole responsibility is to classify the user's request into one of the available intents and extract relevant entities.

### AVAILABLE TOOLS (INTENTS):
1. **configure**:
   - Definition: Use when the user wants to apply settings, create resources, modify parameters, or set up protocols.
   - Keywords: set, create, enable, disable, config, add, apply.
2. **debug**:
   - Definition: Use when the user reports an error, asks to troubleshoot a problem, or fix a broken state.
   - Keywords: fix, troubleshoot, why is..., error, down, not working, issue.
3. **analytics**:
   - Definition: Use when the user asks for status, logs, statistics, monitoring data, or verification.
   - Keywords: show, check, status, list, display, stats, usage, logs.

### OUTPUT FORMAT:
You must respond with a strictly valid JSON object. Do not add any markdown formatting (```json) or conversational text.
Structure:
{{
    "intent": "configure" | "debug" | "analytics",
    "confidence": <float between 0 and 1>,
    "original_query": "<user_input>"
}}

### EXAMPLES:
User: "Setup VLAN 10 on interface xe1"
Output: {{"intent": "configure", "confidence": 0.98, "original_query": "Setup VLAN 10 on interface xe1"}}

User: "Why is OSPF neighbor down?"
Output: {{"intent": "debug", "confidence": 0.99, "original_query": "Why is OSPF neighbor down?"}}

User: "Show me the traffic on eth0"
Output: {{"intent": "analytics", "confidence": 0.95, "original_query": "Show me the traffic on eth0"}}
<|im_end|>
<|im_start|>user
{user_query}
<|im_end|>
<|im_start|>assistant
"""

CONFIGURE_PLANNING_PROMPT = """<|im_start|>system
You are a strategic planner for network configuration tasks on ZebOS devices.
Your job is to break down complex user requests into clear, ordered steps.

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