import requests
import json
from typing import Generator, Optional, Dict, Any

OLLAMA_API = "http://ollama:11434/api/chat"
DEFAULT_MODEL = "qwen3:4b"
DEFAULT_OPTIONS = {
    "repeat_penalty": 2.0,
    "top_k": 20,
    "temperature": 0.3,
    "top_p": 0.9
}


def call_ollama(
    messages: list[dict], 
    model: str = DEFAULT_MODEL,
    options: Optional[Dict[str, Any]] = None
) -> str:
    """
    Non-streaming call to Ollama API
    
    Args:
        messages: List of message dicts with 'role' and 'content'
        model: Model name (default: qwen3:4b)
        options: Optional model parameters
        
    Returns:
        Complete response content as string
    """
    if options is None:
        options = DEFAULT_OPTIONS
        
    resp = requests.post(
        OLLAMA_API,
        json={
            "model": model,
            "messages": messages,
            "stream": False,
            "options": options
        },
        timeout=120
    )
    resp.raise_for_status()
    
    # Extract content from response
    data = resp.json()
    if "message" in data and "content" in data["message"]:
        return data["message"]["content"]
    return ""


def call_ollama_stream(
    messages: list[dict],
    model: str = DEFAULT_MODEL,
    options: Optional[Dict[str, Any]] = None,
    include_thinking: bool = True
) -> Generator[str, None, None]:
    """
    Streaming call to Ollama API - yields tokens only
    
    Args:
        messages: List of message dicts with 'role' and 'content'
        model: Model name (default: qwen3:4b)
        options: Optional model parameters
        include_thinking: Whether to yield thinking tokens (default: True)
        
    Yields:
        Tokens from the model response
    """
    if options is None:
        options = DEFAULT_OPTIONS
        
    try:
        with requests.post(
            OLLAMA_API,
            json={
                "model": model,
                "messages": messages,
                "stream": True,
                "options": options
            },
            stream=True,
            timeout=120
        ) as r:
            r.raise_for_status()
            
            for line in r.iter_lines():
                if line:
                    try:
                        data = json.loads(line.decode("utf-8"))
                        if "message" in data:
                            msg = data["message"]
                            
                            # Yield thinking if enabled
                            if include_thinking and "thinking" in msg and msg["thinking"]:
                                yield msg["thinking"]
                            
                            # Yield content
                            if "content" in msg and msg["content"]:
                                yield msg["content"]
                                
                    except json.JSONDecodeError:
                        continue
                        
    except Exception as e:
        yield f"[ERROR] {str(e)}"


def stream_ollama_with_collection(
    messages: list[dict],
    model: str = DEFAULT_MODEL,
    options: Optional[Dict[str, Any]] = None,
    include_thinking: bool = True
) -> tuple[Generator[str, None, None], callable]:
    """
    Streaming call to Ollama API that yields tokens and collects full response
    
    Args:
        messages: List of message dicts with 'role' and 'content'
        model: Model name (default: qwen3:4b)
        options: Optional model parameters
        include_thinking: Whether to yield thinking tokens (default: True)
        
    Returns:
        Tuple of (generator, callable_to_get_full_response)
    """
    if options is None:
        options = DEFAULT_OPTIONS
    
    # Store response in a mutable container so it can be accessed after streaming
    response_container = {"full_reply": "", "full_thinking": ""}
    
    def generator():
        try:
            with requests.post(
                OLLAMA_API,
                json={
                    "model": model,
                    "messages": messages,
                    "stream": True,
                    "options": options
                },
                stream=True,
                timeout=120
            ) as r:
                r.raise_for_status()
                
                for line in r.iter_lines():
                    if line:
                        try:
                            data = json.loads(line.decode("utf-8"))
                            if "message" in data:
                                msg = data["message"]
                                
                                # Handle thinking
                                if "thinking" in msg and msg["thinking"]:
                                    thinking = msg["thinking"]
                                    response_container["full_thinking"] += thinking
                                    if include_thinking:
                                        yield thinking
                                
                                # Handle content
                                if "content" in msg and msg["content"]:
                                    content = msg["content"]
                                    response_container["full_reply"] += content
                                    yield content
                                    
                        except json.JSONDecodeError:
                            continue
                            
        except Exception as e:
            error_msg = f"Error: {str(e)}"
            response_container["full_reply"] = error_msg
            yield f"[ERROR] {error_msg}"
    
    # Return generator and function to get full response
    return generator(), lambda: response_container["full_reply"]


if __name__ == "__main__":
    # Test non-streaming
    test_messages = [
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": "Hello, how are you?"}
    ]
    
    print("Testing non-streaming call...")
    reply = call_ollama(test_messages)
    print("Ollama reply:", reply)
    
    print("\nTesting streaming call...")
    for token in call_ollama_stream(test_messages):
        print(token, end="", flush=True)
    print("\n\nDone!")