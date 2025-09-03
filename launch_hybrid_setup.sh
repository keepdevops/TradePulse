#!/bin/bash
"""
TradePulse Hybrid Setup Launcher
Starts FastAPI server in Docker and Panel UI locally
"""

set -e

echo "🚀 TradePulse Hybrid Setup Launcher"
echo "=========================================="

# Check if Docker is running
if ! docker info > /dev/null 2>&1; then
    echo "❌ Docker is not running. Please start Docker Desktop first."
    exit 1
fi

# Check if conda environment exists
if ! conda env list | grep -q "tradepulse"; then
    echo "❌ Conda environment 'tradepulse' not found."
    echo "💡 Please create it first: conda env create -f environment.yml"
    exit 1
fi

# Create necessary directories
echo "📁 Creating necessary directories..."
mkdir -p uploads upload_data model_training_data logs

# Start FastAPI server in Docker
echo "🔨 Starting FastAPI server in Docker..."
docker-compose -f docker-compose.api-only.yml up -d

# Wait for FastAPI server to start
echo "⏳ Waiting for FastAPI server to start..."
sleep 10

# Check if FastAPI server is healthy
echo "🔍 Checking FastAPI server health..."
if curl -f http://localhost:8000/health > /dev/null 2>&1; then
    echo "✅ FastAPI server is healthy"
else
    echo "⚠️ FastAPI server may still be starting..."
fi

# Activate conda environment and start Panel
echo "🎯 Starting Panel UI locally..."
echo "📊 Panel UI will be available at: http://localhost:5006"
echo "📡 FastAPI Server will be available at: http://localhost:8000"
echo ""

# Activate conda environment and run Panel
conda activate tradepulse
python launch_panel_local.py
