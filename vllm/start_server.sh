#!/bin/bash
# Start vLLM server with Qwen3:4B model

echo "🚀 Starting vLLM server with Qwen3:4B model..."
echo "📡 Server will listen on http://0.0.0.0:8002"
echo ""
echo "Press Ctrl+C to stop the server"
echo ""

# Start vLLM server
python3 -m vllm.entrypoints.openai.api_server \
    --model qwen3:4b \
    --host 0.0.0.0 \
    --port 8002 \
    --dtype auto \
    --max-model-len 4096 \
    --gpu-memory-utilization 0.9 \
    --tensor-parallel-size 1

# Alternative command if above doesn't work:
# vllm serve qwen3:4b --host 0.0.0.0 --port 8000 --dtype auto --max-model-len 4096
