import requests

OLLAMA_API = "http://localhost:11434/api/chat"

def call_ollama(messages: list[dict]) -> str:
    resp = requests.post(
        OLLAMA_API,
        json={"model": "qwen3:4b", "messages": messages, "stream": False, "thinking": False},
        timeout=120
    )
    resp.raise_for_status()
    return resp.json()["message"]["content"]



if __name__ == "__main__":
    test_messages = [
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": "Hello, how are you?"}
    ]
    reply = call_ollama(test_messages)
    print("Ollama reply:", reply)