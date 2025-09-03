#!/bin/bash

# TradePulse Docker Management Script v10.7
# Comprehensive Docker management for the refactored modular system

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
PURPLE='\033[0;35m'
CYAN='\033[0;36m'
NC='\033[0m' # No Color

# Configuration
COMPOSE_FILE="docker-compose.yml"
PROJECT_NAME="tradepulse"
VERSION="10.7"

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

print_header() {
    echo -e "${PURPLE}================================${NC}"
    echo -e "${PURPLE}  TradePulse v$VERSION Docker Management${NC}"
    echo -e "${PURPLE}================================${NC}"
}

# Function to check Docker and Docker Compose
check_docker() {
    if ! command -v docker &> /dev/null; then
        print_error "Docker is not installed or not in PATH"
        exit 1
    fi
    
    if ! command -v docker-compose &> /dev/null; then
        print_error "Docker Compose is not installed or not in PATH"
        exit 1
    fi
    
    print_success "Docker and Docker Compose are available"
}

# Function to build all services
build_services() {
    print_status "Building all TradePulse services..."
    
    docker-compose -f $COMPOSE_FILE build \
        --no-cache \
        --parallel \
        --progress=plain
    
    print_success "All services built successfully"
}

# Function to start all services
start_services() {
    print_status "Starting TradePulse services..."
    
    docker-compose -f $COMPOSE_FILE up -d
    
    print_success "Services started successfully"
    print_status "Waiting for services to be healthy..."
    
    # Wait for services to be healthy
    sleep 30
    
    # Check service status
    docker-compose -f $COMPOSE_FILE ps
}

# Function to stop all services
stop_services() {
    print_status "Stopping TradePulse services..."
    
    docker-compose -f $COMPOSE_FILE down
    
    print_success "Services stopped successfully"
}

# Function to restart all services
restart_services() {
    print_status "Restarting TradePulse services..."
    
    docker-compose -f $COMPOSE_FILE restart
    
    print_success "Services restarted successfully"
}

# Function to view logs
view_logs() {
    local service=${1:-""}
    
    if [ -z "$service" ]; then
        print_status "Viewing logs for all services..."
        docker-compose -f $COMPOSE_FILE logs -f
    else
        print_status "Viewing logs for service: $service"
        docker-compose -f $COMPOSE_FILE logs -f $service
    fi
}

# Function to check service health
check_health() {
    print_status "Checking service health..."
    
    docker-compose -f $COMPOSE_FILE ps
    
    echo ""
    print_status "Health check details:"
    
    # Check each service individually
    services=("message_bus" "data_grid" "analysis_grid" "models_grid" "trading_grid" "portfolio_grid" "ai_module" "main_app")
    
    for service in "${services[@]}"; do
        if docker-compose -f $COMPOSE_FILE ps $service | grep -q "Up"; then
            print_success "$service is running"
        else
            print_error "$service is not running"
        fi
    done
}

# Function to run tests
run_tests() {
    print_status "Running TradePulse tests..."
    
    # Start services if not running
    if ! docker-compose -f $COMPOSE_FILE ps | grep -q "Up"; then
        print_warning "Services not running. Starting services first..."
        start_services
        sleep 30
    fi
    
    # Run the testing service
    docker-compose -f $COMPOSE_FILE run --rm testing_service
    
    print_success "Tests completed"
}

# Function to clean up
cleanup() {
    print_warning "This will remove all containers, networks, and volumes. Are you sure? (y/N)"
    read -r response
    
    if [[ "$response" =~ ^([yY][eE][sS]|[yY])$ ]]; then
        print_status "Cleaning up Docker resources..."
        
        docker-compose -f $COMPOSE_FILE down -v --remove-orphans
        docker system prune -f
        docker volume prune -f
        
        print_success "Cleanup completed"
    else
        print_status "Cleanup cancelled"
    fi
}

# Function to update services
update_services() {
    print_status "Updating TradePulse services..."
    
    # Pull latest images
    docker-compose -f $COMPOSE_FILE pull
    
    # Rebuild and restart
    build_services
    restart_services
    
    print_success "Services updated successfully"
}

# Function to show service status
show_status() {
    print_status "TradePulse Service Status:"
    echo ""
    
    docker-compose -f $COMPOSE_FILE ps
    
    echo ""
    print_status "Resource Usage:"
    docker stats --no-stream --format "table {{.Container}}\t{{.CPUPerc}}\t{{.MemUsage}}\t{{.NetIO}}\t{{.BlockIO}}"
}

# Function to access service shell
access_shell() {
    local service=${1:-"ai_module"}
    
    print_status "Accessing shell for service: $service"
    
    if docker-compose -f $COMPOSE_FILE ps $service | grep -q "Up"; then
        docker-compose -f $COMPOSE_FILE exec $service conda run -n tradepulse bash
    else
        print_error "Service $service is not running"
    fi
}

# Function to show help
show_help() {
    echo "Usage: $0 [COMMAND] [OPTIONS]"
    echo ""
    echo "Commands:"
    echo "  build           Build all services"
    echo "  start           Start all services"
    echo "  stop            Stop all services"
    echo "  restart         Restart all services"
    echo "  logs [SERVICE]  View logs (all services or specific service)"
    echo "  health          Check service health"
    echo "  test            Run tests"
    echo "  cleanup         Clean up Docker resources"
    echo "  update          Update and restart services"
    echo "  status          Show service status and resource usage"
    echo "  shell [SERVICE] Access shell for a service (default: ai_module)"
    echo "  help            Show this help message"
    echo ""
    echo "Examples:"
    echo "  $0 start                    # Start all services"
    echo "  $0 logs ai_module           # View AI module logs"
    echo "  $0 shell models_grid        # Access models grid shell"
    echo "  $0 test                     # Run tests"
}

# Main script logic
main() {
    print_header
    
    # Check Docker availability
    check_docker
    
    # Parse command line arguments
    case "${1:-help}" in
        build)
            build_services
            ;;
        start)
            start_services
            ;;
        stop)
            stop_services
            ;;
        restart)
            restart_services
            ;;
        logs)
            view_logs "$2"
            ;;
        health)
            check_health
            ;;
        test)
            run_tests
            ;;
        cleanup)
            cleanup
            ;;
        update)
            update_services
            ;;
        status)
            show_status
            ;;
        shell)
            access_shell "$2"
            ;;
        help|--help|-h)
            show_help
            ;;
        *)
            print_error "Unknown command: $1"
            echo ""
            show_help
            exit 1
            ;;
    esac
}

# Run main function with all arguments
main "$@"
