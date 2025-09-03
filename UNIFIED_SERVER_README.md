# TradePulse Unified Server: FastAPI + Panel Integration

## Overview

The TradePulse Unified Server combines FastAPI and Panel into a single, high-performance web application. This integration provides:

- **Single Server**: One server handles both API endpoints and UI
- **Unified Port**: Everything runs on port 8000
- **Seamless Integration**: Panel UI embedded within FastAPI
- **API-First Design**: RESTful API with embedded UI
- **Production Ready**: Scalable and maintainable architecture

## Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    Unified Server (Port 8000)              │
├─────────────────────────────────────────────────────────────┤
│  ┌─────────────────┐  ┌─────────────────┐                  │
│  │   FastAPI       │  │   Panel UI      │                  │
│  │   Endpoints     │  │   Embedded      │                  │
│  │   /api/*        │  │   /             │                  │
│  └─────────────────┘  └─────────────────┘                  │
│                                                             │
│  ┌─────────────────────────────────────────────────────────┐│
│  │              Shared Data Layer                          ││
│  │  • Data Access Manager                                  ││
│  │  • Upload Data Support                                  ││
│  │  • Role-Based Dashboards                                ││
│  └─────────────────────────────────────────────────────────┘│
└─────────────────────────────────────────────────────────────┘
```

## Quick Start

### Method 1: Direct Launch
```bash
# Activate conda environment
conda activate tradepulse

# Launch unified server
python launch_unified_server.py
```

### Method 2: Docker
```bash
# Build and run with Docker
./docker_build_and_run.sh
```

### Method 3: Manual Docker
```bash
# Build image
docker-compose -f docker-compose.fastapi.yml build

# Start services
docker-compose -f docker-compose.fastapi.yml up -d
```

## Available Endpoints

### UI Endpoints
- **Main UI**: `http://localhost:8000/` - Panel UI interface
- **Panel Direct**: `http://localhost:8000/panel` - Direct Panel access
- **Status**: `http://localhost:8000/status` - System status

### API Endpoints
- **API Base**: `http://localhost:8000/api/`
- **API Docs**: `http://localhost:8000/api/docs` - Interactive documentation
- **API Health**: `http://localhost:8000/api/health` - API health check
- **System Health**: `http://localhost:8000/health` - Overall health check

### Data Endpoints
- **Data API**: `http://localhost:8000/api/v1/data/`
- **Models API**: `http://localhost:8000/api/v1/models/`
- **Portfolio API**: `http://localhost:8000/api/v1/portfolio/`
- **Alerts API**: `http://localhost:8000/api/v1/alerts/`
- **System API**: `http://localhost:8000/api/v1/system/`
- **Files API**: `http://localhost:8000/api/v1/files/`

## Features

### 1. Unified Interface
- **Single URL**: Access everything at `localhost:8000`
- **Seamless Navigation**: UI and API work together
- **Consistent Experience**: Same data layer for both

### 2. Upload Data Integration
- **File Upload**: Upload data files via API or UI
- **Multiple Formats**: CSV, JSON, Feather, Parquet, DuckDB, Keras
- **M3 Drive Access**: Scan and import from external drives
- **Data Management**: List, view, and delete uploaded files

### 3. Role-Based Dashboards
- **Default Role**: Complete dashboard with all modules
- **Day Trader**: Trading-focused layout (excludes Models, AI)
- **ML Analyst**: Machine learning layout with Matplotlib
- **AI Analyst**: AI-focused layout with Matplotlib
- **Trend Analyst**: Trend analysis layout with Matplotlib

### 4. API-First Design
- **RESTful Endpoints**: Standard HTTP methods
- **JSON Responses**: Consistent data format
- **Error Handling**: Proper HTTP status codes
- **Documentation**: Auto-generated API docs

## File Structure

```
TradePulse/
├── fastapi_panel_advanced_integration.py  # Main unified server
├── launch_unified_server.py              # Launcher script
├── fastapi_panel_integration.py          # Basic integration
├── api/                                  # FastAPI components
│   ├── fastapi_server.py                # FastAPI app
│   ├── fastapi_client.py                # API client
│   ├── endpoints/                       # API endpoints
│   └── models.py                        # Data models
├── modular_panels/                      # Panel UI components
│   ├── data/                           # Data panel
│   ├── models/                         # Models panel
│   ├── portfolio/                      # Portfolio panel
│   ├── ai/                            # AI panel
│   ├── charts/                        # Charts panel
│   ├── alerts/                        # Alerts panel
│   └── system/                        # System panel
├── ui_components/                      # Shared components
│   ├── data_access.py                 # Data access manager
│   ├── data_manager.py                # Data manager
│   └── dashboard_manager.py           # Dashboard manager
├── uploads/                           # Uploaded data files
├── Dockerfile.fastapi                 # Docker configuration
├── docker-compose.fastapi.yml         # Docker Compose
└── upload_data.py                     # Upload utility
```

## Configuration

### Environment Variables
```bash
# Server Configuration
FASTAPI_HOST=0.0.0.0
FASTAPI_PORT=8000
PANEL_HOST=0.0.0.0
PANEL_PORT=8000

# Data Directories
UPLOAD_DIR=uploads
UPLOAD_DATA_DIR=upload_data
```

### Port Configuration
- **Development**: Port 8000 (default)
- **Production**: Configure via environment variables
- **Docker**: Exposed on port 8000

## Development

### Local Development
```bash
# Install dependencies
conda activate tradepulse
pip install fastapi uvicorn panel aiohttp python-multipart

# Run in development mode
python launch_unified_server.py
```

### Code Changes
The server supports hot reloading:
- **FastAPI**: Automatic reload on code changes
- **Panel**: Refresh browser to see UI changes
- **Logs**: Real-time logging in terminal

### Debugging
```bash
# Check server status
curl http://localhost:8000/health

# Check API status
curl http://localhost:8000/api/health

# View logs
docker-compose -f docker-compose.fastapi.yml logs -f
```

## Production Deployment

### Docker Deployment
```bash
# Build production image
docker-compose -f docker-compose.fastapi.yml build

# Deploy with Docker Compose
docker-compose -f docker-compose.fastapi.yml up -d

# Scale if needed
docker-compose -f docker-compose.fastapi.yml up -d --scale tradepulse-fastapi=3
```

### Environment Configuration
```bash
# Production environment variables
export FASTAPI_HOST=0.0.0.0
export FASTAPI_PORT=8000
export PANEL_HOST=0.0.0.0
export PANEL_PORT=8000
export PYTHONUNBUFFERED=1
```

### Monitoring
```bash
# Health monitoring
curl http://localhost:8000/health

# Performance monitoring
docker stats tradepulse-fastapi

# Log monitoring
docker-compose -f docker-compose.fastapi.yml logs -f
```

## API Usage Examples

### Upload Data
```python
from api.fastapi_client import TradePulseAPIClientSync

client = TradePulseAPIClientSync()

# Upload file
with open('data.csv', 'rb') as f:
    response = client.upload_file(f, 'data')

# Import from M3 drive
response = client.import_from_m3_drive('/Volumes/M3/data.csv', 'upload')
```

### Fetch Data
```python
# Get market data
data = client.fetch_market_data('AAPL', '1d')

# Get uploaded data
files = client.list_uploaded_files('upload')
```

### Create Alerts
```python
# Create price alert
alert = client.create_alert('AAPL', 'price_above', 150.0)
```

## Troubleshooting

### Common Issues

1. **Port Already in Use**
   ```bash
   # Check what's using port 8000
   lsof -i :8000
   
   # Kill process
   kill -9 <PID>
   ```

2. **Panel Not Loading**
   ```bash
   # Check Panel status
   curl http://localhost:8000/panel
   
   # Check logs
   docker-compose logs tradepulse-fastapi
   ```

3. **API Endpoints Not Working**
   ```bash
   # Check API health
   curl http://localhost:8000/api/health
   
   # Check API docs
   curl http://localhost:8000/api/docs
   ```

4. **Upload Data Issues**
   ```bash
   # Check upload directory permissions
   ls -la uploads/
   
   # Check file upload endpoint
   curl http://localhost:8000/api/v1/files/files
   ```

### Performance Optimization

1. **Memory Usage**
   ```bash
   # Monitor memory
   docker stats tradepulse-fastapi
   
   # Increase memory limit
   docker-compose -f docker-compose.fastapi.yml up -d --scale tradepulse-fastapi=2
   ```

2. **Caching**
   - Enable Redis for session caching
   - Use CDN for static files
   - Implement API response caching

3. **Load Balancing**
   ```bash
   # Scale horizontally
   docker-compose -f docker-compose.fastapi.yml up -d --scale tradepulse-fastapi=3
   ```

## Migration Guide

### From Separate Servers
If you were running FastAPI and Panel separately:

1. **Stop separate servers**
   ```bash
   # Stop FastAPI server
   pkill -f "launch_fastapi_server.py"
   
   # Stop Panel server
   pkill -f "launch_modular_ui.py"
   ```

2. **Start unified server**
   ```bash
   python launch_unified_server.py
   ```

3. **Update URLs**
   - Old: `http://localhost:8000` (API) + `http://localhost:5006` (UI)
   - New: `http://localhost:8000` (both)

### From Docker
```bash
# Stop old containers
docker-compose down

# Start unified container
docker-compose -f docker-compose.fastapi.yml up -d
```

## Support

For issues and questions:

1. **Check logs**: `docker-compose logs tradepulse-fastapi`
2. **Health check**: `curl http://localhost:8000/health`
3. **API docs**: `http://localhost:8000/api/docs`
4. **Status page**: `http://localhost:8000/status`

The unified server provides a complete, production-ready solution for TradePulse with seamless integration between FastAPI and Panel.
