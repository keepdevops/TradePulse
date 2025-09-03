# TradePulse FastAPI + Panel Docker Setup

This guide explains how to run TradePulse with FastAPI and Panel using Docker and conda.

## Overview

The Docker setup provides:
- **FastAPI Server**: High-performance API server on port 8000
- **Panel UI**: Interactive web interface on port 5006
- **Conda Environment**: Optimized Python environment with all dependencies
- **Data Persistence**: Mounted volumes for uploads, redline data, and models
- **Health Monitoring**: Built-in health checks and monitoring

## Prerequisites

1. **Docker Desktop**
   - Download from: https://docs.docker.com/get-docker/
   - Ensure Docker is running

2. **Docker Compose**
   - Usually included with Docker Desktop
   - Verify with: `docker-compose --version`

## Quick Start

### Method 1: Automated Scripts (Recommended)

#### macOS/Linux
```bash
# Make script executable
chmod +x docker_build_and_run.sh

# Build and run
./docker_build_and_run.sh
```

#### Windows
```cmd
# Run batch file
docker_build_and_run.bat
```

### Method 2: Manual Docker Commands

```bash
# Build the image
docker-compose -f docker-compose.fastapi.yml build

# Start services
docker-compose -f docker-compose.fastapi.yml up -d

# Check status
docker-compose -f docker-compose.fastapi.yml ps
```

## Services

### FastAPI Server
- **Port**: 8000
- **URL**: http://localhost:8000
- **Documentation**: http://localhost:8000/docs
- **Health Check**: http://localhost:8000/health

### Panel UI
- **Port**: 5006
- **URL**: http://localhost:5006
- **Features**: Interactive dashboards, data upload, role-based layouts

## Docker Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    Docker Container                        │
├─────────────────────────────────────────────────────────────┤
│  ┌─────────────────┐  ┌─────────────────┐                  │
│  │   FastAPI       │  │   Panel UI      │                  │
│  │   (Port 8000)   │  │   (Port 5006)   │                  │
│  └─────────────────┘  └─────────────────┘                  │
│                                                             │
│  ┌─────────────────────────────────────────────────────────┐│
│  │              Conda Environment                         ││
│  │  • fastapi, uvicorn                                    ││
│  │  • pandas, numpy, scikit-learn                         ││
│  │  • panel, bokeh                                        ││
│  │  • yfinance, alpha-vantage                             ││
│  └─────────────────────────────────────────────────────────┘│
└─────────────────────────────────────────────────────────────┘
```

## Volume Mounts

The container mounts several directories for data persistence:

- `./uploads` → `/app/uploads` - User uploaded files
- `./redline_data` → `/app/redline_data` - Redline data files
- `./model_training_data` → `/app/model_training_data` - ML models
- `./logs` → `/app/logs` - Application logs

## Environment Variables

| Variable | Default | Description |
|----------|---------|-------------|
| `FASTAPI_HOST` | `0.0.0.0` | FastAPI server host |
| `FASTAPI_PORT` | `8000` | FastAPI server port |
| `PANEL_HOST` | `0.0.0.0` | Panel UI host |
| `PANEL_PORT` | `5006` | Panel UI port |
| `PYTHONUNBUFFERED` | `1` | Python output buffering |

## Docker Commands

### Basic Operations

```bash
# Build image
docker-compose -f docker-compose.fastapi.yml build

# Start services
docker-compose -f docker-compose.fastapi.yml up -d

# Stop services
docker-compose -f docker-compose.fastapi.yml down

# View logs
docker-compose -f docker-compose.fastapi.yml logs -f

# Check status
docker-compose -f docker-compose.fastapi.yml ps
```

### Advanced Operations

```bash
# Rebuild without cache
docker-compose -f docker-compose.fastapi.yml build --no-cache

# Start specific service
docker-compose -f docker-compose.fastapi.yml up -d tradepulse-fastapi

# Execute commands in container
docker-compose -f docker-compose.fastapi.yml exec tradepulse-fastapi bash

# View container resources
docker stats tradepulse-fastapi

# Clean up everything
docker-compose -f docker-compose.fastapi.yml down --rmi all --volumes
```

### Data Management

```bash
# Backup data
tar -czf tradepulse_backup_$(date +%Y%m%d).tar.gz uploads/ redline_data/ model_training_data/

# Restore data
tar -xzf tradepulse_backup_20241201.tar.gz

# View data directory sizes
du -sh uploads/ redline_data/ model_training_data/
```

## Troubleshooting

### Common Issues

1. **Port already in use**
   ```bash
   # Check what's using the ports
   lsof -i :8000
   lsof -i :5006
   
   # Stop conflicting services or change ports in docker-compose.fastapi.yml
   ```

2. **Container won't start**
   ```bash
   # Check logs
   docker-compose -f docker-compose.fastapi.yml logs tradepulse-fastapi
   
   # Check container status
   docker-compose -f docker-compose.fastapi.yml ps
   ```

3. **Permission issues**
   ```bash
   # Fix directory permissions
   sudo chown -R $USER:$USER uploads/ redline_data/ model_training_data/ logs/
   chmod 755 uploads/ redline_data/ model_training_data/ logs/
   ```

4. **Out of disk space**
   ```bash
   # Clean up Docker
   docker system prune -a
   docker volume prune
   ```

### Health Checks

```bash
# Check FastAPI health
curl http://localhost:8000/health

# Check Panel UI
curl http://localhost:5006

# Check container health
docker inspect tradepulse-fastapi | grep -A 10 "Health"
```

### Performance Optimization

1. **Increase memory limit**
   ```yaml
   # In docker-compose.fastapi.yml
   services:
     tradepulse-fastapi:
       deploy:
         resources:
           limits:
             memory: 4G
   ```

2. **Use host networking (Linux)**
   ```yaml
   # In docker-compose.fastapi.yml
   services:
     tradepulse-fastapi:
       network_mode: host
   ```

3. **Enable Docker BuildKit**
   ```bash
   export DOCKER_BUILDKIT=1
   docker-compose -f docker-compose.fastapi.yml build
   ```

## Development

### Building for Development

```bash
# Build with development dependencies
docker-compose -f docker-compose.fastapi.yml build --build-arg ENV=development

# Run with volume mounts for live code changes
docker-compose -f docker-compose.fastapi.yml up -d
```

### Adding New Dependencies

1. Update `environment_fastapi.yml`
2. Rebuild the image:
   ```bash
   docker-compose -f docker-compose.fastapi.yml build --no-cache
   docker-compose -f docker-compose.fastapi.yml up -d
   ```

### Debugging

```bash
# Access container shell
docker-compose -f docker-compose.fastapi.yml exec tradepulse-fastapi bash

# View real-time logs
docker-compose -f docker-compose.fastapi.yml logs -f --tail=100

# Check conda environment
docker-compose -f docker-compose.fastapi.yml exec tradepulse-fastapi conda list
```

## Production Deployment

### Security Considerations

1. **Change default ports**
2. **Use environment variables for secrets**
3. **Enable Docker security features**
4. **Regular security updates**

### Monitoring

```bash
# Set up monitoring
docker run -d \
  --name prometheus \
  -p 9090:9090 \
  -v /path/to/prometheus.yml:/etc/prometheus/prometheus.yml \
  prom/prometheus

# Monitor container metrics
docker stats tradepulse-fastapi
```

### Backup Strategy

```bash
# Create backup script
#!/bin/bash
DATE=$(date +%Y%m%d_%H%M%S)
tar -czf "tradepulse_backup_$DATE.tar.gz" \
  uploads/ redline_data/ model_training_data/ logs/
```

## Support

If you encounter issues:

1. Check the troubleshooting section above
2. Verify Docker and Docker Compose versions
3. Check container logs: `docker-compose logs tradepulse-fastapi`
4. Ensure ports are available
5. Verify disk space and permissions
