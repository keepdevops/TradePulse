@echo off
REM TradePulse FastAPI + Panel Docker Build and Run Script (Windows)

echo 🐳 TradePulse FastAPI + Panel Docker Setup
echo ==========================================

REM Check if Docker is installed
where docker >nul 2>nul
if %errorlevel% neq 0 (
    echo ❌ Docker is not installed. Please install Docker first.
    echo    Download from: https://docs.docker.com/get-docker/
    pause
    exit /b 1
)

REM Check if Docker Compose is installed
where docker-compose >nul 2>nul
if %errorlevel% neq 0 (
    echo ❌ Docker Compose is not installed. Please install Docker Compose first.
    echo    Download from: https://docs.docker.com/compose/install/
    pause
    exit /b 1
)

echo ✅ Docker found: 
docker --version
echo ✅ Docker Compose found: 
docker-compose --version

REM Create necessary directories
echo 📁 Creating necessary directories...
if not exist uploads mkdir uploads
if not exist redline_data mkdir redline_data
if not exist model_training_data mkdir model_training_data
if not exist logs mkdir logs

REM Build the Docker image
echo 🔨 Building Docker image...
docker-compose -f docker-compose.fastapi.yml build

if %errorlevel% equ 0 (
    echo ✅ Docker image built successfully!
) else (
    echo ❌ Docker build failed. Please check the error messages above.
    pause
    exit /b 1
)

REM Start the services
echo 🚀 Starting TradePulse services...
docker-compose -f docker-compose.fastapi.yml up -d

if %errorlevel% equ 0 (
    echo ✅ Services started successfully!
    echo.
    echo 🎯 Services are now running:
    echo    📡 FastAPI Server: http://localhost:8000
    echo    📊 Panel UI: http://localhost:5006
    echo    📚 API Documentation: http://localhost:8000/docs
    echo    📖 ReDoc Documentation: http://localhost:8000/redoc
    echo.
    echo 🔍 Check service status:
    echo    docker-compose -f docker-compose.fastapi.yml ps
    echo.
    echo 📋 View logs:
    echo    docker-compose -f docker-compose.fastapi.yml logs -f
    echo.
    echo 🛑 Stop services:
    echo    docker-compose -f docker-compose.fastapi.yml down
    echo.
    echo 🧹 Clean up (removes containers and images):
    echo    docker-compose -f docker-compose.fastapi.yml down --rmi all --volumes
    echo.
    echo 🎉 Setup complete!
) else (
    echo ❌ Failed to start services. Please check the error messages above.
    pause
    exit /b 1
)

REM Wait a moment for services to fully start
echo ⏳ Waiting for services to start...
timeout /t 10 /nobreak >nul

REM Check if services are healthy
echo 🔍 Checking service health...
curl -f http://localhost:8000/health >nul 2>nul
if %errorlevel% equ 0 (
    echo ✅ FastAPI server is healthy!
) else (
    echo ⚠️  FastAPI server health check failed. It may still be starting up.
)

echo.
echo 🎯 Next steps:
echo 1. Open your browser and navigate to:
echo    - Panel UI: http://localhost:5006
echo    - API Docs: http://localhost:8000/docs
echo.
echo 2. Upload redline data using the Panel UI or API
echo.
echo 3. Monitor logs: docker-compose -f docker-compose.fastapi.yml logs -f

pause
