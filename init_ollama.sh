#!/bin/bash

# Wait for Ollama service to be ready
echo "Waiting for Ollama service to be ready..."
MAX_RETRIES=60
RETRY_COUNT=0

while [ $RETRY_COUNT -lt $MAX_RETRIES ]; do
    if curl -s http://localhost:11434/api/tags > /dev/null 2>&1; then
        echo "✓ Ollama service is ready"
        break
    fi
    RETRY_COUNT=$((RETRY_COUNT + 1))
    echo "Waiting... ($RETRY_COUNT/$MAX_RETRIES)"
    sleep 2
done

if [ $RETRY_COUNT -eq $MAX_RETRIES ]; then
    echo "✗ Ollama service did not respond in time"
    exit 1
fi

# Pull required models
echo ""
echo "Pulling required models..."
echo "⏳ Pulling qwen3:4b..."
ollama pull qwen3:4b
if [ $? -ne 0 ]; then
    echo "✗ Failed to pull qwen3:4b"
    exit 1
fi

echo "⏳ Pulling nomic-embed-text..."
ollama pull nomic-embed-text
if [ $? -ne 0 ]; then
    echo "✗ Failed to pull nomic-embed-text"
    exit 1
fi

echo ""
echo "✓ All models pulled successfully!"
echo ""
echo "Available models:"
ollama list
