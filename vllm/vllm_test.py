"""
Test script for vLLM with Qwen3:4B model
Tests inference with streaming and batch processing
"""

import requests
import json
import time
from typing import Generator

# Configuration
VLLM_SERVER_URL = "http://localhost:8020"
MODEL_NAME = "qwen3:4b"
TIMEOUT = 300  # 5 minutes timeout for long responses

class VLLMClient:
    """Client for vLLM API"""
    
    def __init__(self, base_url: str = VLLM_SERVER_URL):
        self.base_url = base_url.rstrip('/')
        self.model = MODEL_NAME
    
    def test_connection(self) -> bool:
        """Test connection to vLLM server"""
        try:
            print(f"🔗 Testing connection to {self.base_url}...")
            response = requests.get(f"{self.base_url}/v1/models", timeout=10)
            if response.status_code == 200:
                print("✅ Connection successful")
                models = response.json().get('data', [])
                print(f"📦 Available models: {len(models)}")
                for model in models:
                    print(f"   - {model.get('id', 'unknown')}")
                return True
            else:
                print(f"❌ Connection failed: {response.status_code}")
                return False
        except Exception as e:
            print(f"❌ Connection error: {e}")
            return False
    
    def complete(self, prompt: str, max_tokens: int = 100) -> str:
        """Send completion request (non-streaming)"""
        print(f"\n📝 Prompt: {prompt[:100]}...")
        print(f"⏳ Waiting for response...")
        
        payload = {
            "model": self.model,
            "prompt": prompt,
            "max_tokens": max_tokens,
            "temperature": 0.7,
            "top_p": 0.9,
        }
        
        try:
            response = requests.post(
                f"{self.base_url}/v1/completions",
                json=payload,
                timeout=TIMEOUT
            )
            
            if response.status_code == 200:
                result = response.json()
                completion = result['choices'][0]['text']
                print(f"✅ Completion received ({len(completion)} chars)")
                return completion
            else:
                print(f"❌ Error: {response.status_code}")
                print(response.text)
                return ""
        except requests.Timeout:
            print("❌ Request timeout - model might be processing a large response")
            return ""
        except Exception as e:
            print(f"❌ Error: {e}")
            return ""
    
    def complete_stream(self, prompt: str, max_tokens: int = 100) -> Generator[str, None, None]:
        """Send completion request with streaming"""
        print(f"\n📝 Prompt: {prompt[:100]}...")
        print(f"⏳ Streaming response:")
        
        payload = {
            "model": self.model,
            "prompt": prompt,
            "max_tokens": max_tokens,
            "temperature": 0.7,
            "top_p": 0.9,
            "stream": True,
        }
        
        try:
            response = requests.post(
                f"{self.base_url}/v1/completions",
                json=payload,
                stream=True,
                timeout=TIMEOUT
            )
            
            if response.status_code == 200:
                for line in response.iter_lines():
                    if line:
                        line = line.decode('utf-8')
                        if line.startswith('data: '):
                            data = json.loads(line[6:])
                            if 'choices' in data and len(data['choices']) > 0:
                                token = data['choices'][0].get('text', '')
                                if token:
                                    yield token
                                    print(token, end='', flush=True)
                print("\n✅ Streaming complete")
            else:
                print(f"❌ Error: {response.status_code}")
                print(response.text)
        except requests.Timeout:
            print("\n❌ Streaming timeout")
        except Exception as e:
            print(f"\n❌ Error: {e}")
    
    def chat(self, messages: list, max_tokens: int = 100) -> str:
        """Send chat completion request"""
        print(f"\n💬 Chat request with {len(messages)} messages")
        
        payload = {
            "model": self.model,
            "messages": messages,
            "max_tokens": max_tokens,
            "temperature": 0.7,
            "top_p": 0.9,
        }
        
        try:
            response = requests.post(
                f"{self.base_url}/v1/chat/completions",
                json=payload,
                timeout=TIMEOUT
            )
            
            if response.status_code == 200:
                result = response.json()
                completion = result['choices'][0]['message']['content']
                print(f"✅ Response received ({len(completion)} chars)")
                return completion
            else:
                print(f"❌ Error: {response.status_code}")
                print(response.text)
                return ""
        except requests.Timeout:
            print("❌ Request timeout")
            return ""
        except Exception as e:
            print(f"❌ Error: {e}")
            return ""


def test_basic_completion():
    """Test basic completion"""
    print("\n" + "="*80)
    print("TEST 1: Basic Completion")
    print("="*80)
    
    client = VLLMClient()
    prompt = "What is the capital of France?"
    response = client.complete(prompt, max_tokens=50)
    print(f"\n📤 Response:\n{response}")


def test_streaming():
    """Test streaming completion"""
    print("\n" + "="*80)
    print("TEST 2: Streaming Completion")
    print("="*80)
    
    client = VLLMClient()
    prompt = "Write a short poem about the moon:"
    print(f"📝 Prompt: {prompt}")
    print("⏳ Streaming:\n")
    
    for token in client.complete_stream(prompt, max_tokens=100):
        pass


def test_chat():
    """Test chat completion"""
    print("\n" + "="*80)
    print("TEST 3: Chat Completion")
    print("="*80)
    
    client = VLLMClient()
    messages = [
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": "What is 2 + 2?"},
    ]
    
    response = client.chat(messages, max_tokens=50)
    print(f"\n📤 Response:\n{response}")


def test_zebos_config():
    """Test ZebOS configuration prompt"""
    print("\n" + "="*80)
    print("TEST 4: ZebOS Configuration")
    print("="*80)
    
    client = VLLMClient()
    prompt = """Configure OSPF on a ZebOS router with:
- Router ID: 1.1.1.1
- Process: 100
- Network: 10.0.0.0/24 in Area 0

Provide the complete CLI commands:"""
    
    response = client.complete(prompt, max_tokens=150)
    print(f"\n📤 Response:\n{response}")


def test_performance():
    """Test performance with multiple requests"""
    print("\n" + "="*80)
    print("TEST 5: Performance Test (5 sequential requests)")
    print("="*80)
    
    client = VLLMClient()
    prompts = [
        "What is Python?",
        "Explain networking.",
        "What is vLLM?",
        "Describe ZebOS.",
        "What is API?",
    ]
    
    start_time = time.time()
    
    for i, prompt in enumerate(prompts, 1):
        print(f"\n[{i}/5] {prompt}")
        response = client.complete(prompt, max_tokens=30)
        print(f"Response: {response[:50]}..." if len(response) > 50 else f"Response: {response}")
    
    total_time = time.time() - start_time
    avg_time = total_time / len(prompts)
    
    print(f"\n📊 Performance:")
    print(f"   Total time: {total_time:.2f}s")
    print(f"   Average time per request: {avg_time:.2f}s")
    print(f"   Requests per minute: {60/avg_time:.1f}")


def main():
    """Run all tests"""
    print("🧪 vLLM Test Suite - Qwen3:4B Model")
    print("="*80)
    
    client = VLLMClient()
    
    # Test connection first
    if not client.test_connection():
        print("\n❌ Cannot connect to vLLM server. Make sure it's running at:")
        print(f"   {VLLM_SERVER_URL}")
        print("\nTo start vLLM server, run:")
        print(f"   vllm serve {MODEL_NAME} --host 0.0.0.0 --port 8000")
        return
    
    # Run tests
    try:
        test_basic_completion()
        test_streaming()
        test_chat()
        test_zebos_config()
        test_performance()
        
        print("\n" + "="*80)
        print("✅ All tests completed!")
        print("="*80)
    except KeyboardInterrupt:
        print("\n\n⚠️ Tests interrupted by user")
    except Exception as e:
        print(f"\n\n❌ Test failed: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()
