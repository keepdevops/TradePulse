# TradePulse Modular Panel UI - Docker Setup

This document describes how to run the TradePulse Modular Panel UI using Docker containers.

## 🚀 Quick Start

### Prerequisites

- Docker (version 20.10 or higher)
- Docker Compose (version 1.29 or higher)
- At least 4GB of available RAM
- At least 10GB of available disk space

### Development Environment

1. **Start the development environment:**
   ```bash
   ./docker_management_modular.sh start-dev
   ```

2. **Access the UI:**
   - Open your browser and navigate to: http://localhost:5006
   - The modular panel UI will be available with all TradePulse modules

3. **Check service status:**
   ```bash
   ./docker_management_modular.sh status
   ```

### Production Environment

1. **Start the production environment:**
   ```bash
   ./docker_management_modular.sh start-prod
   ```

2. **Access services:**
   - Modular Panel UI: http://localhost:5006
   - Nginx (reverse proxy): http://localhost:80, https://localhost:443
   - Grafana (monitoring): http://localhost:3000 (admin/admin)
   - Prometheus (metrics): http://localhost:9090

## 🏗️ Architecture

The Docker setup includes the following services:

### Core Services
- **Message Bus**: ZeroMQ-based message broker (ports 5555/5556)
- **Database**: PostgreSQL + DuckDB (ports 5432/8000)
- **Modular Panel UI**: Main web interface (port 5006)

### Optional Services (Production Profile)
- **Nginx**: Reverse proxy and load balancer (ports 80/443)
- **Redis**: Caching layer (port 6379)
- **Prometheus**: Metrics collection (port 9090)
- **Grafana**: Monitoring dashboard (port 3000)

## 📁 File Structure

```
TradePulse/
├── Dockerfile.modular_panel_ui          # Modular Panel UI container
├── docker-compose.dev.yml               # Development environment
├── docker-compose.modular.yml           # Production environment
├── docker_management_modular.sh         # Management script
├── modular_panels/                      # Panel components
│   ├── __init__.py
│   ├── data_panel.py
│   ├── models_panel.py
│   ├── portfolio_panel.py
│   ├── ai_panel.py
│   ├── charts_panel.py
│   ├── alerts_panel.py
│   └── system_panel.py
├── modular_panel_ui_main.py            # Main UI application
├── requirements_panel.txt               # Python dependencies
└── README_Docker_Modular.md            # This file
```

## 🛠️ Management Commands

### Using the Management Script

```bash
# Start development environment
./docker_management_modular.sh start-dev

# Start production environment
./docker_management_modular.sh start-prod

# Stop all services
./docker_management_modular.sh stop

# Restart services
./docker_management_modular.sh restart

# Show logs
./docker_management_modular.sh logs [service_name]

# Show status
./docker_management_modular.sh status

# Clean up
./docker_management_modular.sh cleanup

# Show help
./docker_management_modular.sh help
```

### Using Docker Compose Directly

```bash
# Development environment
docker-compose -f docker-compose.dev.yml -p tradepulse_modular up -d

# Production environment
docker-compose -f docker-compose.modular.yml -p tradepulse_modular --profile production up -d

# View logs
docker-compose -f docker-compose.dev.yml -p tradepulse_modular logs -f

# Stop services
docker-compose -f docker-compose.dev.yml -p tradepulse_modular down
```

## 🔧 Configuration

### Environment Variables

The following environment variables can be configured:

```bash
# Message Bus
MESSAGE_BUS_HOST=message_bus
MESSAGE_BUS_PUB_PORT=5555
MESSAGE_BUS_SUB_PORT=5556

# Database
DATABASE_HOST=database
DATABASE_PORT=5432
POSTGRES_DB=tradepulse_dev
POSTGRES_USER=tradepulse
POSTGRES_PASSWORD=tradepulse123

# Panel UI
PANEL_PORT=5006
PANEL_HOST=0.0.0.0
ENVIRONMENT=development
DEBUG=true
```

### Volume Mounts

- `./data:/app/data` - Persistent data storage
- `./config:/app/config` - Configuration files
- `./logs:/app/logs` - Application logs
- `.:/app` - Source code (development only)

## 📊 Monitoring

### Health Checks

All services include health checks:

- **Message Bus**: ZMQ connectivity test
- **Database**: Connection test
- **Modular Panel UI**: HTTP endpoint test
- **Nginx**: HTTP endpoint test

### Metrics Collection

In production mode, metrics are collected via:

- **Prometheus**: Scrapes metrics from all services
- **Grafana**: Visualizes metrics and provides dashboards

## 🚨 Troubleshooting

### Common Issues

1. **Port conflicts:**
   ```bash
   # Check what's using the ports
   lsof -i :5006
   lsof -i :5555
   lsof -i :5556
   ```

2. **Container won't start:**
   ```bash
   # Check logs
   ./docker_management_modular.sh logs [service_name]
   
   # Check container status
   docker ps -a
   ```

3. **Permission issues:**
   ```bash
   # Fix file permissions
   chmod +x docker_management_modular.sh
   sudo chown -R $USER:$USER data config logs
   ```

4. **Memory issues:**
   ```bash
   # Check Docker memory usage
   docker stats
   
   # Increase Docker memory limit in Docker Desktop
   ```

### Debug Mode

Enable debug mode by setting environment variables:

```bash
export DEBUG=true
export ENVIRONMENT=development
```

### Log Analysis

```bash
# Follow all logs
docker-compose -f docker-compose.dev.yml -p tradepulse_modular logs -f

# Filter logs by service
docker-compose -f docker-compose.dev.yml -p tradepulse_modular logs -f modular_panel_ui

# Search logs for errors
docker-compose -f docker-compose.dev.yml -p tradepulse_modular logs | grep ERROR
```

## 🔄 Updates and Maintenance

### Updating the Application

1. **Pull latest changes:**
   ```bash
   git pull origin main
   ```

2. **Rebuild containers:**
   ```bash
   ./docker_management_modular.sh stop
   ./docker_management_modular.sh start-dev
   ```

### Backup and Restore

1. **Backup data:**
   ```bash
   docker exec tradepulse_database_dev pg_dump -U tradepulse tradepulse_dev > backup.sql
   ```

2. **Restore data:**
   ```bash
   docker exec -i tradepulse_database_dev psql -U tradepulse tradepulse_dev < backup.sql
   ```

## 📚 Additional Resources

- [Docker Documentation](https://docs.docker.com/)
- [Docker Compose Documentation](https://docs.docker.com/compose/)
- [Panel Documentation](https://panel.holoviz.org/)
- [TradePulse Documentation](./README.md)

## 🤝 Support

If you encounter issues:

1. Check the troubleshooting section above
2. Review the logs using the management script
3. Check the TradePulse main documentation
4. Open an issue in the project repository

## 📄 License

This Docker setup is part of the TradePulse project and follows the same licensing terms.
