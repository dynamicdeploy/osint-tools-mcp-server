#!/bin/bash
# Publish all individual OSINT Tools MCP services to Docker Hub
#
# Usage:
#   ./publish_all_services.sh [version]
#   ./publish_all_services.sh v1.0.0
#   ./publish_all_services.sh        # Uses 'latest' tag only

set -e

# Configuration
VERSION="${1:-latest}"
SERVICES=("sherlock" "holehe" "maigret" "blackbird" "spiderfoot" "ghunt" "theharvester")

# Colors for output
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Function to print colored output
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

# Check if Docker is running
check_docker() {
    print_info "Checking Docker..."
    if ! docker info > /dev/null 2>&1; then
        print_error "Docker is not running. Please start Docker Desktop."
        exit 1
    fi
    print_success "Docker is running"
}

# Check if logged into Docker Hub
check_docker_login() {
    print_info "Checking Docker Hub login..."
    if ! docker info | grep -q "Username"; then
        print_warning "Not logged into Docker Hub"
        print_info "Please login with: docker login"
        read -p "Do you want to login now? (y/n) " -n 1 -r
        echo
        if [[ $REPLY =~ ^[Yy]$ ]]; then
            docker login
        else
            print_error "Cannot proceed without Docker Hub login"
            exit 1
        fi
    fi
    print_success "Logged into Docker Hub"
}

# Publish a single service
publish_service() {
    local service=$1
    local version=$2
    
    print_header "Publishing ${service} Service"
    
    cd "${service}"
    
    # Check if publish script exists
    if [ ! -f "publish_to_docker.sh" ]; then
        print_error "publish_to_docker.sh not found in ${service}/"
        cd ..
        return 1
    fi
    
    # Make sure script is executable
    chmod +x publish_to_docker.sh
    
    # Run publish script
    if [ "$version" == "latest" ]; then
        print_info "Publishing ${service} with 'latest' tag..."
        ./publish_to_docker.sh
    else
        print_info "Publishing ${service} with version '${version}'..."
        ./publish_to_docker.sh "${version}"
    fi
    
    if [ $? -eq 0 ]; then
        print_success "${service} published successfully"
        cd ..
        return 0
    else
        print_error "Failed to publish ${service}"
        cd ..
        return 1
    fi
}

# Main execution
main() {
    print_header "Publishing All OSINT Tools MCP Services"
    print_info "Version: ${VERSION}"
    print_info "Services to publish: ${#SERVICES[@]}"
    echo
    
    # Pre-flight checks
    check_docker
    check_docker_login
    
    # Confirm before proceeding
    print_warning "This will publish ${#SERVICES[@]} services to Docker Hub"
    print_info "Services: ${SERVICES[*]}"
    read -p "Continue? (y/n) " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        print_info "Publishing cancelled"
        exit 0
    fi
    
    # Track results
    published=0
    failed=0
    failed_services=()
    
    # Publish each service
    for service in "${SERVICES[@]}"; do
        if publish_service "${service}" "${VERSION}"; then
            published=$((published + 1))
        else
            failed=$((failed + 1))
            failed_services+=("${service}")
        fi
        echo
    done
    
    # Summary
    print_header "Publishing Summary"
    print_success "Successfully published: ${published}/${#SERVICES[@]}"
    
    if [ ${failed} -gt 0 ]; then
        print_error "Failed to publish: ${failed}"
        print_error "Failed services: ${failed_services[*]}"
    fi
    
    if [ ${failed} -eq 0 ]; then
        print_success "All services published successfully!"
        echo
        print_info "Published images:"
        for service in "${SERVICES[@]}"; do
            print_info "  - hackerdogs/${service}-mcp-server:latest"
            if [ "$VERSION" != "latest" ]; then
                print_info "  - hackerdogs/${service}-mcp-server:${VERSION}"
            fi
        done
        echo
        print_info "Docker Hub: https://hub.docker.com/r/hackerdogs/"
        return 0
    else
        print_error "Some services failed to publish"
        return 1
    fi
}

# Run main function
main
