#!/bin/bash

# TradePulse Modular Panel UI Docker Management Script
# This script manages the Docker containers for the modular panel UI

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Configuration
COMPOSE_FILE_DEV="docker-compose.dev.yml"
COMPOSE_FILE_PROD="docker-compose.modular.yml"
PROJECT_NAME="tradepulse_modular"

# Function to print colored output
print_status() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

print_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Function to check if Docker is running
check_docker() {
    if ! docker info > /dev/null 2>&1; then
        print_error "Docker is not running. Please start Docker and try again."
        exit 1
    fi
    print_success "Docker is running"
}

# Function to check if Docker Compose is available
check_docker_compose() {
    if ! command -v docker-compose &> /dev/null; then
        print_error "Docker Compose is not installed. Please install it and try again."
        exit 1
    fi
    print_success "Docker Compose is available"
}

# Function to build and start development environment
start_dev() {
    print_status "Starting TradePulse Modular Panel UI development environment..."
    
    check_docker
    check_docker_compose
    
    # Create necessary directories
    mkdir -p data config logs
    
    # Build and start services
    docker-compose -f $COMPOSE_FILE_DEV -p $PROJECT_NAME up --build -d
    
    print_success "Development environment started successfully!"
    print_status "Services available at:"
    print_status "  - Modular Panel UI: http://localhost:5006"
    print_status "  - Message Bus: localhost:5555 (PUB), 5556 (SUB)"
    print_status "  - Database: localhost:5432 (PostgreSQL), 8000 (DuckDB)"
    print_status "  - Redis: localhost:6379"
    
    # Show running containers
    docker-compose -f $COMPOSE_FILE_DEV -p $PROJECT_NAME ps
}

# Function to start production environment
start_prod() {
    print_status "Starting TradePulse Modular Panel UI production environment..."
    
    check_docker
    check_docker_compose
    
    # Create necessary directories
    mkdir -p data config logs ssl monitoring
    
    # Build and start services
    docker-compose -f $COMPOSE_FILE_PROD -p $PROJECT_NAME --profile production up --build -d
    
    print_success "Production environment started successfully!"
    print_status "Services available at:"
    print_status "  - Modular Panel UI: http://localhost:5006"
    print_status "  - Nginx: http://localhost:80, https://localhost:443"
    print_status "  - Grafana: http://localhost:3000 (admin/admin)"
    print_status "  - Prometheus: http://localhost:9090"
    
    # Show running containers
    docker-compose -f $COMPOSE_FILE_PROD -p $PROJECT_NAME --profile production ps
}

# Function to stop services
stop_services() {
    print_status "Stopping TradePulse services..."
    
    # Stop development environment
    if docker-compose -f $COMPOSE_FILE_DEV -p $PROJECT_NAME ps -q | grep -q .; then
        docker-compose -f $COMPOSE_FILE_DEV -p $PROJECT_NAME down
        print_success "Development environment stopped"
    fi
    
    # Stop production environment
    if docker-compose -f $COMPOSE_FILE_PROD -p $PROJECT_NAME ps -q | grep -q .; then
        docker-compose -f $COMPOSE_FILE_PROD -p $PROJECT_NAME --profile production down
        print_success "Production environment stopped"
    fi
}

# Function to restart services
restart_services() {
    print_status "Restarting TradePulse services..."
    stop_services
    sleep 2
    start_dev
}

# Function to show logs
show_logs() {
    local service=${1:-"modular_panel_ui"}
    
    print_status "Showing logs for $service..."
    
    if docker-compose -f $COMPOSE_FILE_DEV -p $PROJECT_NAME ps -q | grep -q .; then
        docker-compose -f $COMPOSE_FILE_DEV -p $PROJECT_NAME logs -f $service
    elif docker-compose -f $COMPOSE_FILE_PROD -p $PROJECT_NAME ps -q | grep -q .; then
        docker-compose -f $COMPOSE_FILE_PROD -p $PROJECT_NAME --profile production logs -f $service
    else
        print_warning "No services are running"
    fi
}

# Function to show status
show_status() {
    print_status "TradePulse services status:"
    
    # Check development environment
    if docker-compose -f $COMPOSE_FILE_DEV -p $PROJECT_NAME ps -q | grep -q .; then
        print_status "Development environment:"
        docker-compose -f $COMPOSE_FILE_DEV -p $PROJECT_NAME ps
    fi
    
    # Check production environment
    if docker-compose -f $COMPOSE_FILE_PROD -p $PROJECT_NAME ps -q | grep -q .; then
        print_status "Production environment:"
        docker-compose -f $COMPOSE_FILE_PROD -p $PROJECT_NAME --profile production ps
    fi
    
    if ! docker-compose -f $COMPOSE_FILE_DEV -p $PROJECT_NAME ps -q | grep -q . && \
       ! docker-compose -f $COMPOSE_FILE_PROD -p $PROJECT_NAME ps -q | grep -q .; then
        print_warning "No services are running"
    fi
}

# Function to clean up
cleanup() {
    print_status "Cleaning up TradePulse containers and volumes..."
    
    # Stop and remove containers
    stop_services
    
    # Remove volumes
    docker volume prune -f
    
    # Remove networks
    docker network prune -f
    
    print_success "Cleanup completed"
}

# Function to show help
show_help() {
    echo "TradePulse Modular Panel UI Docker Management Script"
    echo ""
    echo "Usage: $0 [COMMAND]"
    echo ""
    echo "Commands:"
    echo "  start-dev     Start development environment"
    echo "  start-prod    Start production environment"
    echo "  stop          Stop all services"
    echo "  restart       Restart development environment"
    echo "  logs [SERVICE] Show logs (default: modular_panel_ui)"
    echo "  status        Show services status"
    echo "  cleanup       Clean up containers and volumes"
    echo "  help          Show this help message"
    echo ""
    echo "Examples:"
    echo "  $0 start-dev"
    echo "  $0 logs database"
    echo "  $0 status"
}

# Main script logic
case "${1:-help}" in
    start-dev)
        start_dev
        ;;
    start-prod)
        start_prod
        ;;
    stop)
        stop_services
        ;;
    restart)
        restart_services
        ;;
    logs)
        show_logs "$2"
        ;;
    status)
        show_status
        ;;
    cleanup)
        cleanup
        ;;
    help|--help|-h)
        show_help
        ;;
    *)
        print_error "Unknown command: $1"
        show_help
        exit 1
        ;;
esac
