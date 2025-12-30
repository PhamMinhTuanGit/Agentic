#!/usr/bin/env python3
"""
Test refactored Ollama client functions
Tests both streaming and non-streaming calls
"""

import sys
sys.path.insert(0, '/Users/phamminhtuan/Desktop/Agentic/Agentic')

from app.llm.ollama import call_ollama, call_ollama_stream, stream_ollama_with_collection


def test_non_streaming():
    """Test non-streaming call"""
    print("=" * 60)
    print("Test 1: Non-Streaming Call")
    print("=" * 60)
    
    messages = [
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": "What is BGP in networking? Answer in 2 sentences."}
    ]
    
    print("\nCalling Ollama (non-streaming)...")
    response = call_ollama(messages)
    print(f"\nResponse: {response}")
    print("\n✓ Non-streaming test passed!\n")


def test_streaming():
    """Test streaming call"""
    print("=" * 60)
    print("Test 2: Streaming Call (with thinking)")
    print("=" * 60)
    
    messages = [
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": "Explain OSPF in one sentence."}
    ]
    
    print("\nCalling Ollama (streaming with thinking)...")
    print("Response: ", end="", flush=True)
    
    for token in call_ollama_stream(messages, include_thinking=True):
        print(token, end="", flush=True)
    
    print("\n\n✓ Streaming test passed!\n")


def test_streaming_no_thinking():
    """Test streaming without thinking"""
    print("=" * 60)
    print("Test 3: Streaming Call (without thinking)")
    print("=" * 60)
    
    messages = [
        {"role": "user", "content": "What is MPLS? One sentence only."}
    ]
    
    print("\nCalling Ollama (streaming without thinking)...")
    print("Response: ", end="", flush=True)
    
    for token in call_ollama_stream(messages, include_thinking=False):
        print(token, end="", flush=True)
    
    print("\n\n✓ Streaming (no thinking) test passed!\n")


def test_streaming_with_collection():
    """Test streaming with full response collection"""
    print("=" * 60)
    print("Test 4: Streaming with Collection")
    print("=" * 60)
    
    messages = [
        {"role": "user", "content": "Count from 1 to 5."}
    ]
    
    print("\nCalling Ollama (streaming with collection)...")
    print("Response: ", end="", flush=True)
    
    stream = stream_ollama_with_collection(messages, include_thinking=False)
    
    for token in stream:
        print(token, end="", flush=True)
    
    full_response = stream.get_full_response()
    print(f"\n\nFull collected response: '{full_response}'")
    print("\n✓ Streaming with collection test passed!\n")


if __name__ == "__main__":
    print("\n" + "=" * 60)
    print("Testing Refactored Ollama Client")
    print("=" * 60)
    print()
    
    try:
        test_non_streaming()
        test_streaming()
        test_streaming_no_thinking()
        test_streaming_with_collection()
        
        print("=" * 60)
        print("✓ All tests passed!")
        print("=" * 60)
        
    except Exception as e:
        print(f"\n✗ Error: {e}")
        import traceback
        traceback.print_exc()
