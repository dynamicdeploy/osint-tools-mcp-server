#!/bin/bash
# Test all services using Docker Hub images
#
# Usage:
#   ./test_all_from_dockerhub.sh

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

print_header() {
    echo -e "\n${YELLOW}=========================================="
    echo "$1"
    echo "==========================================${NC}\n"
}

# List of all services
SERVICES=("sherlock" "holehe" "maigret" "blackbird" "spiderfoot" "ghunt" "theharvester")

# Pull all images from Docker Hub
pull_images() {
    print_header "Pulling Images from Docker Hub"
    
    for service in "${SERVICES[@]}"; do
        print_info "Pulling hackerdogs/${service}-mcp-server:latest..."
        if docker pull "hackerdogs/${service}-mcp-server:latest" > /dev/null 2>&1; then
            print_success "${service} pulled successfully"
        else
            print_error "Failed to pull ${service}"
            return 1
        fi
    done
}

# Test a service
test_service() {
    local service=$1
    
    print_header "Testing ${service} Service"
    
    if [ -f "${service}/test_${service}.py" ]; then
        cd "${service}"
        if python3 "test_${service}.py" > /tmp/test_${service}.log 2>&1; then
            print_success "${service} tests passed"
            cd ..
            return 0
        else
            print_error "${service} tests failed"
            cat /tmp/test_${service}.log | tail -10
            cd ..
            return 1
        fi
    else
        print_error "Test script not found for ${service}"
        return 1
    fi
}

# Main execution
main() {
    print_header "Docker Hub Images Test Suite"
    
    # Check Docker
    if ! docker info > /dev/null 2>&1; then
        print_error "Docker is not running"
        exit 1
    fi
    
    # Pull images
    if ! pull_images; then
        print_error "Failed to pull some images"
        exit 1
    fi
    
    # Test each service
    total_passed=0
    total_failed=0
    failed_services=()
    
    for service in "${SERVICES[@]}"; do
        if test_service "${service}"; then
            total_passed=$((total_passed + 1))
        else
            total_failed=$((total_failed + 1))
            failed_services+=("${service}")
        fi
    done
    
    # Summary
    print_header "Test Summary"
    print_success "Services passed: ${total_passed}/${#SERVICES[@]}"
    
    if [ ${total_failed} -gt 0 ]; then
        print_error "Services failed: ${total_failed}"
        print_error "Failed services: ${failed_services[*]}"
        return 1
    else
        print_success "All services tested successfully from Docker Hub!"
        return 0
    fi
}

# Run main function
main
