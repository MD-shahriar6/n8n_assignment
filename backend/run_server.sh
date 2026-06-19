#!/bin/bash

# Load environment variables
set -a
if [ -f .env ]; then
    source .env
fi
set +a

# Run the FastAPI server
echo "Starting FastAPI server..."
uvicorn main:app --host 0.0.0.0 --port 8005 --reload