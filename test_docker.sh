#!/bin/bash
# Test script for Docker-based MCP Server

set -e

echo "=========================================="
echo "Docker MCP Server Test Suite"
echo "=========================================="

# Colors for output
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Function to print test header
print_test() {
    echo -e "\n${YELLOW}TEST: $1${NC}"
    echo "----------------------------------------"
}

# Function to check if command succeeded
check_result() {
    if [ $? -eq 0 ]; then
        echo -e "${GREEN}✅ $1${NC}"
        return 0
    else
        echo -e "${RED}❌ $1${NC}"
        return 1
    fi
}

# Test 1: Build Docker image
print_test "Building Docker Image"
docker build -t osint-tools-mcp-server:latest .
check_result "Docker image built successfully"

# Test 2: Verify image exists
print_test "Verifying Image"
docker images | grep -q osint-tools-mcp-server
check_result "Image exists in Docker"

# Test 3: Test container can start
print_test "Testing Container Startup"
CONTAINER_ID=$(docker run -d --name osint-mcp-test osint-tools-mcp-server:latest)
sleep 2
docker ps | grep -q osint-mcp-test
check_result "Container started successfully"

# Test 4: Verify all tools are installed
print_test "Verifying OSINT Tools Installation"
docker exec osint-mcp-test which sherlock > /dev/null
check_result "Sherlock installed"

docker exec osint-mcp-test which holehe > /dev/null
check_result "Holehe installed"

docker exec osint-mcp-test which maigret > /dev/null
check_result "Maigret installed"

docker exec osint-mcp-test which theHarvester > /dev/null
check_result "TheHarvester installed"

docker exec osint-mcp-test test -f /opt/spiderfoot/sf.py
check_result "SpiderFoot installed"

docker exec osint-mcp-test test -f /opt/ghunt/ghunt.py
check_result "GHunt installed"

docker exec osint-mcp-test test -f /opt/blackbird/blackbird.py
check_result "Blackbird installed"

# Test 5: Test MCP server responds to initialize
print_test "Testing MCP Server Initialize"
INIT_REQUEST='{"jsonrpc":"2.0","id":1,"method":"initialize","params":{"protocolVersion":"2024-11-05","capabilities":{},"clientInfo":{"name":"test","version":"1.0.0"}}}'
RESPONSE=$(echo "$INIT_REQUEST" | docker exec -i osint-mcp-test python3 /app/src/osint_tools_mcp_server.py | head -1)
echo "$RESPONSE" | grep -q "serverInfo"
check_result "MCP server responds to initialize"

# Test 6: Test tools/list
print_test "Testing MCP Server Tools List"
TOOLS_REQUEST='{"jsonrpc":"2.0","id":2,"method":"tools/list"}'
TOOLS_RESPONSE=$(echo "$TOOLS_REQUEST" | docker exec -i osint-mcp-test python3 /app/src/osint_tools_mcp_server.py | head -1)
echo "$TOOLS_RESPONSE" | grep -q "sherlock_username_search"
check_result "Tools list includes sherlock_username_search"
echo "$TOOLS_RESPONSE" | grep -q "holehe_email_search"
check_result "Tools list includes holehe_email_search"
echo "$TOOLS_RESPONSE" | grep -q "spiderfoot_scan"
check_result "Tools list includes spiderfoot_scan"
echo "$TOOLS_RESPONSE" | grep -q "ghunt_google_search"
check_result "Tools list includes ghunt_google_search"
echo "$TOOLS_RESPONSE" | grep -q "maigret_username_search"
check_result "Tools list includes maigret_username_search"
echo "$TOOLS_RESPONSE" | grep -q "theharvester_domain_search"
check_result "Tools list includes theharvester_domain_search"
echo "$TOOLS_RESPONSE" | grep -q "blackbird_username_search"
check_result "Tools list includes blackbird_username_search"

# Cleanup
print_test "Cleaning Up"
docker stop osint-mcp-test > /dev/null 2>&1
docker rm osint-mcp-test > /dev/null 2>&1
check_result "Test container cleaned up"

echo -e "\n${GREEN}=========================================="
echo "All Docker Tests Completed!"
echo "==========================================${NC}"

