#!/usr/bin/env python3
"""
Download model for vLLM offline usage
Supports both Hugging Face models and GGUF format
"""

import os
import sys
import subprocess
from pathlib import Path

# Model configurations
MODELS = {
    "qwen2.5": {
        "hf_id": "Qwen/Qwen2.5-7B-Instruct",
        "description": "Qwen 2.5 7B Instruct (Hugging Face)"
    },
    "qwen2": {
        "hf_id": "Qwen/Qwen2-7B-Instruct", 
        "description": "Qwen 2 7B Instruct (Hugging Face)"
    },
    "mistral": {
        "hf_id": "mistralai/Mistral-7B-Instruct-v0.1",
        "description": "Mistral 7B Instruct"
    },
    "llama2": {
        "hf_id": "meta-llama/Llama-2-7b-chat-hf",
        "description": "Llama 2 7B Chat"
    }
}

# Cache directory for models
MODELS_CACHE = os.path.expanduser("~/.cache/huggingface/hub")

def check_dependencies():
    """Check required dependencies"""
    try:
        import torch
        print(f"✅ PyTorch: {torch.__version__}")
    except ImportError:
        print("❌ PyTorch not installed")
        return False
    
    try:
        import transformers
        print(f"✅ Transformers: {transformers.__version__}")
    except ImportError:
        print("❌ Transformers not installed")
        return False
    
    return True

def download_huggingface_model(model_id: str, model_name: str):
    """Download model from Hugging Face"""
    print(f"\n📦 Downloading {model_name}...")
    print(f"   Model ID: {model_id}")
    print(f"   Cache dir: {MODELS_CACHE}")
    
    try:
        from huggingface_hub import snapshot_download
        
        local_path = snapshot_download(
            repo_id=model_id,
            cache_dir=MODELS_CACHE,
            resume_download=True,
            allow_patterns=["*.json", "*.model", "*.safetensors", "*.py", "*.txt", "*.md"],
        )
        
        print(f"\n✅ Downloaded to: {local_path}")
        return local_path
    except Exception as e:
        print(f"❌ Download failed: {e}")
        return None

def download_with_transformers(model_id: str, model_name: str):
    """Download model using transformers library"""
    print(f"\n📦 Downloading {model_name} with transformers...")
    print(f"   Model ID: {model_id}")
    
    try:
        from transformers import AutoTokenizer, AutoModelForCausalLM
        
        print("   Downloading tokenizer...")
        tokenizer = AutoTokenizer.from_pretrained(model_id)
        print("   ✅ Tokenizer downloaded")
        
        print("   Downloading model (this may take a while)...")
        model = AutoModelForCausalLM.from_pretrained(
            model_id,
            torch_dtype="auto",
            device_map="auto"
        )
        print("   ✅ Model downloaded")
        
        # Get model location
        model_location = os.path.join(MODELS_CACHE, f"models--{model_id.replace('/', '--')}")
        print(f"\n✅ Model saved to: {model_location}")
        return model_location
    except Exception as e:
        print(f"❌ Download failed: {e}")
        return None

def list_cached_models():
    """List cached models"""
    print(f"\n📂 Cached models in {MODELS_CACHE}:")
    
    if not os.path.exists(MODELS_CACHE):
        print("   No cached models found")
        return
    
    models = []
    for item in os.listdir(MODELS_CACHE):
        if item.startswith("models--"):
            model_name = item.replace("models--", "").replace("--", "/")
            models.append(model_name)
    
    if models:
        for model in sorted(models):
            print(f"   - {model}")
    else:
        print("   No cached models found")

def get_model_size(model_id: str) -> str:
    """Get approximate model size"""
    sizes = {
        "7B": "~14GB",
        "13B": "~26GB",
        "70B": "~140GB"
    }
    
    for key, size in sizes.items():
        if key in model_id:
            return size
    return "Unknown"

def main():
    """Main function"""
    print("="*80)
    print("🤖 vLLM Model Downloader - Offline Setup")
    print("="*80)
    
    # Check dependencies
    print("\n🔍 Checking dependencies...")
    if not check_dependencies():
        print("\n❌ Missing dependencies. Install with:")
        print("   pip install torch transformers huggingface-hub")
        sys.exit(1)
    
    # Show available models
    print("\n📋 Available models:")
    for key, config in MODELS.items():
        size = get_model_size(config["hf_id"])
        print(f"   [{key}] {config['description']}")
        print(f"        Size: ~{size}")
        print(f"        HF ID: {config['hf_id']}\n")
    
    # List cached
    list_cached_models()
    
    # Get user choice
    print("\n" + "="*80)
    choice = input("\nSelect model to download (qwen2.5/qwen2/mistral/llama2) [qwen2.5]: ").strip().lower()
    
    if not choice:
        choice = "qwen2.5"
    
    if choice not in MODELS:
        print(f"❌ Unknown model: {choice}")
        sys.exit(1)
    
    model_config = MODELS[choice]
    model_id = model_config["hf_id"]
    
    print(f"\n{'='*80}")
    print(f"⬇️  Model: {model_config['description']}")
    print(f"   Size: {get_model_size(model_id)}")
    print(f"   This will take 10-30 minutes depending on your internet speed")
    print(f"{'='*80}\n")
    
    confirm = input("Continue? (y/n) [y]: ").strip().lower()
    if confirm and confirm != 'y':
        print("❌ Cancelled")
        sys.exit(1)
    
    # Download model
    print(f"\n🚀 Starting download...")
    local_path = download_huggingface_model(model_id, model_config["description"])
    
    if local_path:
        print(f"\n✅ Model downloaded successfully!")
        print(f"\n📝 To use with vLLM offline:")
        print(f"   vllm serve {model_id} --host 0.0.0.0 --port 8000")
        print(f"\n📝 Or update your vllm_test.py:")
        print(f'   MODEL_NAME = "{model_id}"')
    else:
        print("\n❌ Download failed")
        sys.exit(1)

if __name__ == "__main__":
    main()
