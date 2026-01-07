#!/usr/bin/env python3
"""
Initialize Ollama by pulling required models.
This script ensures all needed models are available before the application starts.
"""

import os
import sys
import time
import requests
import subprocess

OLLAMA_HOST = os.getenv('OLLAMA_HOST', 'http://localhost:11434')
MODELS_TO_PULL = ['qwen3:4b', 'nomic-embed-text']

def wait_for_ollama(max_retries=60):
    """Wait for Ollama service to be ready"""
    print(f"Waiting for Ollama service at {OLLAMA_HOST}...")
    
    for attempt in range(max_retries):
        try:
            response = requests.get(f"{OLLAMA_HOST}/api/tags", timeout=5)
            if response.status_code == 200:
                print("✓ Ollama service is ready")
                return True
        except requests.RequestException:
            pass
        
        print(f"  Attempt {attempt + 1}/{max_retries}...")
        time.sleep(2)
    
    print("✗ Ollama service did not respond in time")
    return False

def pull_models():
    """Pull required models from Ollama"""
    # Use ollama CLI to pull models
    try:
        import ollama
        client = ollama.Client(host=OLLAMA_HOST)
        
        for model in MODELS_TO_PULL:
            print(f"\n⏳ Pulling {model}...")
            try:
                client.pull(model)
                print(f"✓ {model} pulled successfully")
            except Exception as e:
                print(f"✗ Failed to pull {model}: {e}")
                return False
    except ImportError:
        # Fallback to subprocess if ollama module not available
        print("Using ollama CLI for model pulling...")
        for model in MODELS_TO_PULL:
            print(f"\n⏳ Pulling {model}...")
            result = subprocess.run(['ollama', 'pull', model], capture_output=True, text=True)
            if result.returncode != 0:
                print(f"✗ Failed to pull {model}: {result.stderr}")
                return False
            print(f"✓ {model} pulled successfully")
    
    return True

def list_models():
    """List available models"""
    try:
        import ollama
        client = ollama.Client(host=OLLAMA_HOST)
        models = client.list()
        print("\n✓ Available models:")
        for model in models['models']:
            print(f"  - {model['name']}")
    except Exception as e:
        print(f"Warning: Could not list models: {e}")

def main():
    print("=" * 60)
    print("Ollama Model Initialization")
    print("=" * 60)
    
    # Wait for service
    if not wait_for_ollama():
        sys.exit(1)
    
    # Pull models
    print("\nPulling required models...")
    if not pull_models():
        sys.exit(1)
    
    # List available models
    list_models()
    
    print("\n" + "=" * 60)
    print("✓ Initialization complete!")
    print("=" * 60)

if __name__ == '__main__':
    main()
