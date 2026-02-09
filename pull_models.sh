#!/bin/bash

# Start ollama server in background
ollama serve &
SERVER_PID=$!

# Wait for server to be ready
echo "Waiting for Ollama server to start..."
sleep 5

# Pull models
echo "Pulling models..."
ollama pull qwen3:4b
ollama pull nomic-embed-text

echo "Models pulled successfully!"

# Keep server running
wait $SERVER_PID
