#!/bin/sh
set -e

echo "Starting Docker containers for the project..."
docker-compose -f docker-compose.yml up -d

echo "Waiting for the container ollama to be ready..."
until curl  -s http://localhost:11434/v1/models > /dev/null; do
    echo "Waiting for ollama to be ready..."
    sleep 5
done

echo "Pulling the Mistral model..."
docker exec -it ollama-server ollama pull mistral

echo "Starting Mistral model"
docker exec -d ollama-server bash -c "ollama run mistral > /dev/null 2>&1 &"

echo "Waiting for the Mistral model to start..."
until docker exec ollama-server ollama list | grep -q mistral; do
    echo "Still starting Mistral model..."
    sleep 5
done

echo "Mistral model is running and ready to use via API at http://localhost:11434"