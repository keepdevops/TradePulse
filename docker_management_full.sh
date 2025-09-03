#!/bin/bash

# TradePulse v10.7 Full Docker Management Script
# Comprehensive management for all TradePulse services

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Configuration
COMPOSE_FILE="docker-compose.full.yml"
PROJECT_NAME="tradepulse_full"
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
        print_error "Docker Compose is not installed. Please install Docker Compose and try again."
        exit 1
    fi
    print_success "Docker Compose is available"
}

# Function to build all services
build_services() {
    print_status "Building all TradePulse v$VERSION services..."
    
    # Clean up any existing images
    docker system prune -f
    
    # Build all services
    docker-compose -f $COMPOSE_FILE build --no-cache
    
    print_success "All services built successfully!"
}

# Function to start all services
start_services() {
    print_status "Starting all TradePulse v$VERSION services..."
    
    # Start all services in detached mode
    docker-compose -f $COMPOSE_FILE up -d
    
    print_success "All services started successfully!"
    
    # Wait a moment for services to initialize
    sleep 5
    
    # Show service status
    show_status
}

# Function to stop all services
stop_services() {
    print_status "Stopping all TradePulse v$VERSION services..."
    
    docker-compose -f $COMPOSE_FILE down
    
    print_success "All services stopped successfully!"
}

# Function to restart all services
restart_services() {
    print_status "Restarting all TradePulse v$VERSION services..."
    
    stop_services
    start_services
    
    print_success "All services restarted successfully!"
}

# Function to show service status
show_status() {
    print_status "TradePulse v$VERSION Service Status:"
    echo "=========================================="
    
    # Show running containers
    docker-compose -f $COMPOSE_FILE ps
    
    echo ""
    print_status "Container Health Status:"
    echo "============================="
    
    # Check health of each service
    services=("message_bus" "ai_module" "data_grid" "models_grid" "analysis_grid" "trading_grid" "portfolio_grid" "main_app")
    
    for service in "${services[@]}"; do
        container_name="tradepulse_${service}"
        if docker ps --format "table {{.Names}}\t{{.Status}}" | grep -q "$container_name"; then
            status=$(docker inspect --format='{{.State.Health.Status}}' "$container_name" 2>/dev/null || echo "no-health-check")
            echo "$service: $status"
        else
            echo "$service: not running"
        fi
    done
}

# Function to show logs for all services
show_logs() {
    print_status "Showing logs for all services (Ctrl+C to exit)..."
    
    docker-compose -f $COMPOSE_FILE logs -f
}

# Function to show logs for a specific service
show_service_logs() {
    if [ -z "$1" ]; then
        print_error "Please specify a service name"
        echo "Available services: message_bus, ai_module, data_grid, models_grid, analysis_grid, trading_grid, portfolio_grid, testing, main_app"
        exit 1
    fi
    
    print_status "Showing logs for service: $1"
    docker-compose -f $COMPOSE_FILE logs -f "$1"
}

# Function to run tests
run_tests() {
    print_status "Running TradePulse v$VERSION tests..."
    
    # Run the testing service
    docker-compose -f $COMPOSE_FILE run --rm testing
    
    print_success "Tests completed!"
}

# Function to access service shell
access_shell() {
    if [ -z "$1" ]; then
        print_error "Please specify a service name"
        echo "Available services: message_bus, ai_module, data_grid, models_grid, analysis_grid, trading_grid, portfolio_grid, main_app"
        exit 1
    fi
    
    print_status "Accessing shell for service: $1"
    docker-compose -f $COMPOSE_FILE exec "$1" conda run -n tradepulse /bin/bash
}

# Function to clean up everything
cleanup() {
    print_warning "This will remove ALL TradePulse containers, images, and networks. Are you sure? (y/N)"
    read -r response
    
    if [[ "$response" =~ ^([yY][eE][sS]|[yY])$ ]]; then
        print_status "Cleaning up all TradePulse resources..."
        
        # Stop and remove containers
        docker-compose -f $COMPOSE_FILE down -v
        
        # Remove images
        docker rmi $(docker images | grep tradepulse | awk '{print $3}') 2>/dev/null || true
        
        # Remove networks
        docker network rm tradepulse_network_v10_7_full 2>/dev/null || true
        
        # Clean up volumes
        docker volume prune -f
        
        print_success "Cleanup completed!"
    else
        print_status "Cleanup cancelled"
    fi
}

# Function to show system resources
show_resources() {
    print_status "TradePulse v$VERSION System Resources:"
    echo "============================================="
    
    # Show container resource usage
    docker stats --no-stream --format "table {{.Name}}\t{{.CPUPerc}}\t{{.MemUsage}}\t{{.NetIO}}\t{{.BlockIO}}"
    
    echo ""
    print_status "Disk Usage:"
    echo "============="
    df -h | grep -E "(Filesystem|/dev/)"
}

# Function to show help
show_help() {
    echo "TradePulse v$VERSION Docker Management Script"
    echo "============================================="
    echo ""
    echo "Usage: $0 [COMMAND]"
    echo ""
    echo "Commands:"
    echo "  build           Build all services"
    echo "  start           Start all services"
    echo "  stop            Stop all services"
    echo "  restart         Restart all services"
    echo "  status          Show service status"
    echo "  logs            Show logs for all services"
    echo "  logs [SERVICE]  Show logs for specific service"
    echo "  test            Run portfolio optimization tests"
    echo "  shell [SERVICE] Access shell for specific service"
    echo "  resources       Show system resource usage"
    echo "  cleanup         Remove all containers, images, and networks"
    echo "  help            Show this help message"
    echo ""
    echo "Examples:"
    echo "  $0 start                    # Start all services"
    echo "  $0 logs ai_module           # Show AI module logs"
    echo "  $0 shell message_bus        # Access message bus shell"
    echo "  $0 test                     # Run tests"
}

# Main script logic
main() {
    # Check prerequisites
    check_docker
    check_docker_compose
    
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
        status)
            show_status
            ;;
        logs)
            if [ -z "$2" ]; then
                show_logs
            else
                show_service_logs "$2"
            fi
            ;;
        test)
            run_tests
            ;;
        shell)
            access_shell "$2"
            ;;
        resources)
            show_resources
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
}

# Run main function with all arguments
main "$@"
