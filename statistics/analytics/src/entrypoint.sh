#!/bin/bash

# Run any setup steps or pre-processing tasks here
echo "Starting Analytics service..."

# Start the main application
uvicorn main:app --host 0.0.0.0 --port 8032