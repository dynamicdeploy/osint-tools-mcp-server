#!/bin/bash
# Test all individual MCP server services
#
# Usage:
#   ./test_all_services.sh [service_name]
#   ./test_all_services.sh sherlock
#   ./test_all_services.sh        # Tests all services

set -e

# Colors for output
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

print_info() {
    echo -e "${BLUE}ℹ️  $1${NC}"
}

print_success() {
    echo -e "${GREEN}✅ $1${NC}"
}

print_error() {
    echo -e "${RED}❌ $1${NC}"
}

print_warning() {
    echo -e "${YELLOW}⚠️  $1${NC}"
}

print_header() {
    echo -e "\n${YELLOW}=========================================="
    echo "$1"
    echo "==========================================${NC}\n"
}

# List of all services
SERVICES=("sherlock" "holehe" "spiderfoot" "ghunt" "maigret" "theharvester" "blackbird")

# Check if Docker is running
check_docker() {
    print_info "Checking Docker..."
    if ! docker info > /dev/null 2>&1; then
        print_error "Docker is not running. Please start Docker Desktop."
        exit 1
    fi
    print_success "Docker is running"
}

# Build a service
build_service() {
    local service=$1
    print_header "Building ${service} Service"
    
    cd "${service}"
    print_info "Building ${service}-mcp-server:latest..."
    docker build -t "${service}-mcp-server:latest" .
    print_success "${service} image built successfully"
    cd ..
}

# Test a service
test_service() {
    local service=$1
    print_header "Testing ${service} Service"
    
    if [ -f "${service}/test_${service}.py" ]; then
        print_info "Running test script for ${service}..."
        python3 "${service}/test_${service}.py"
        if [ $? -eq 0 ]; then
            print_success "${service} tests passed"
            return 0
        else
            print_error "${service} tests failed"
            return 1
        fi
    else
        print_warning "No test script found for ${service}"
        return 0
    fi
}

# Main execution
main() {
    print_header "OSINT Tools MCP Services Test Suite"
    
    # Pre-flight checks
    check_docker
    
    # Determine which services to test
    if [ -n "$1" ]; then
        if [[ " ${SERVICES[@]} " =~ " ${1} " ]]; then
            SERVICES=("$1")
        else
            print_error "Unknown service: $1"
            print_info "Available services: ${SERVICES[*]}"
            exit 1
        fi
    fi
    
    # Build and test each service
    total_passed=0
    total_failed=0
    
    for service in "${SERVICES[@]}"; do
        print_info "Processing ${service}..."
        
        # Build
        if build_service "${service}"; then
            # Test
            if test_service "${service}"; then
                total_passed=$((total_passed + 1))
            else
                total_failed=$((total_failed + 1))
            fi
        else
            print_error "Failed to build ${service}"
            total_failed=$((total_failed + 1))
        fi
    done
    
    # Summary
    print_header "Test Summary"
    print_info "Services passed: ${total_passed}"
    print_info "Services failed: ${total_failed}"
    
    if [ ${total_failed} -eq 0 ]; then
        print_success "All services built and tested successfully!"
        return 0
    else
        print_error "Some services failed"
        return 1
    fi
}

# Run main function
main "$@"

