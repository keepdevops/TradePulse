#!/bin/bash
# TradePulse FastAPI + Panel Docker Build and Run Script

set -e  # Exit on any error

echo "🐳 TradePulse FastAPI + Panel Docker Setup"
echo "=========================================="

# Check if Docker is installed
if ! command -v docker &> /dev/null; then
    echo "❌ Docker is not installed. Please install Docker first."
    echo "   Download from: https://docs.docker.com/get-docker/"
    exit 1
fi

# Check if Docker Compose is installed
if ! command -v docker-compose &> /dev/null; then
    echo "❌ Docker Compose is not installed. Please install Docker Compose first."
    echo "   Download from: https://docs.docker.com/compose/install/"
    exit 1
fi

echo "✅ Docker found: $(docker --version)"
echo "✅ Docker Compose found: $(docker-compose --version)"

# Create necessary directories
echo "📁 Creating necessary directories..."
mkdir -p uploads redline_data model_training_data logs

# Set permissions
chmod 755 uploads redline_data model_training_data logs

# Build the Docker image
echo "🔨 Building Docker image..."
docker-compose -f docker-compose.fastapi.yml build

if [ $? -eq 0 ]; then
    echo "✅ Docker image built successfully!"
else
    echo "❌ Docker build failed. Please check the error messages above."
    exit 1
fi

# Start the services
echo "🚀 Starting TradePulse services..."
docker-compose -f docker-compose.fastapi.yml up -d

if [ $? -eq 0 ]; then
    echo "✅ Services started successfully!"
    echo ""
    echo "🎯 Services are now running:"
    echo "   📡 FastAPI Server: http://localhost:8000"
    echo "   📊 Panel UI: http://localhost:5006"
    echo "   📚 API Documentation: http://localhost:8000/docs"
    echo "   📖 ReDoc Documentation: http://localhost:8000/redoc"
    echo ""
    echo "🔍 Check service status:"
    echo "   docker-compose -f docker-compose.fastapi.yml ps"
    echo ""
    echo "📋 View logs:"
    echo "   docker-compose -f docker-compose.fastapi.yml logs -f"
    echo ""
    echo "🛑 Stop services:"
    echo "   docker-compose -f docker-compose.fastapi.yml down"
    echo ""
    echo "🧹 Clean up (removes containers and images):"
    echo "   docker-compose -f docker-compose.fastapi.yml down --rmi all --volumes"
    echo ""
    echo "🎉 Setup complete!"
else
    echo "❌ Failed to start services. Please check the error messages above."
    exit 1
fi

# Wait a moment for services to fully start
echo "⏳ Waiting for services to start..."
sleep 10

# Check if services are healthy
echo "🔍 Checking service health..."
if curl -f http://localhost:8000/health > /dev/null 2>&1; then
    echo "✅ FastAPI server is healthy!"
else
    echo "⚠️  FastAPI server health check failed. It may still be starting up."
fi

echo ""
echo "🎯 Next steps:"
echo "1. Open your browser and navigate to:"
echo "   - Panel UI: http://localhost:5006"
echo "   - API Docs: http://localhost:8000/docs"
echo ""
echo "2. Upload redline data using the Panel UI or API"
echo ""
echo "3. Monitor logs: docker-compose -f docker-compose.fastapi.yml logs -f"
