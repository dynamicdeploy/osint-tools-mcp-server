# Services Setup Summary

This document summarizes the separated services architecture for OSINT Tools MCP Server.

## Architecture Overview

The original monolithic MCP server has been split into 7 independent services, each with:
- Dedicated MCP server implementation
- Separate Docker container
- Individual test suite
- Independent publishing script

## Directory Structure

```
services/
├── README.md                    # Main documentation
├── docker-compose.yml           # All services orchestration
├── test_all_services.sh         # Test all services script
├── sherlock/
│   ├── src/
│   │   └── sherlock_mcp_server.py
│   ├── Dockerfile
│   ├── requirements.txt
│   ├── publish_to_docker.sh
│   └── test_sherlock.py
├── holehe/
│   ├── src/
│   │   └── holehe_mcp_server.py
│   ├── Dockerfile
│   ├── requirements.txt
│   ├── publish_to_docker.sh
│   └── test_holehe.py
├── spiderfoot/
│   ├── src/
│   │   └── spiderfoot_mcp_server.py
│   ├── Dockerfile
│   ├── requirements.txt
│   ├── publish_to_docker.sh
│   └── test_spiderfoot.py
├── ghunt/
│   ├── src/
│   │   └── ghunt_mcp_server.py
│   ├── Dockerfile
│   ├── requirements.txt
│   ├── publish_to_docker.sh
│   └── test_ghunt.py
├── maigret/
│   ├── src/
│   │   └── maigret_mcp_server.py
│   ├── Dockerfile
│   ├── requirements.txt
│   ├── publish_to_docker.sh
│   └── test_maigret.py
├── theharvester/
│   ├── src/
│   │   └── theharvester_mcp_server.py
│   ├── Dockerfile
│   ├── requirements.txt
│   ├── publish_to_docker.sh
│   └── test_theharvester.py
└── blackbird/
    ├── src/
    │   └── blackbird_mcp_server.py
    ├── Dockerfile
    ├── requirements.txt
    ├── publish_to_docker.sh
    └── test_blackbird.py
```

## Services

### 1. Sherlock
- **Image**: `sherlock-mcp-server:latest`
- **Tool**: Username search across 399+ platforms
- **Dependencies**: sherlock-project

### 2. Holehe
- **Image**: `holehe-mcp-server:latest`
- **Tool**: Email registration check on 120+ platforms
- **Dependencies**: holehe

### 3. SpiderFoot
- **Image**: `spiderfoot-mcp-server:latest`
- **Tool**: Comprehensive OSINT scan
- **Dependencies**: SpiderFoot (cloned from GitHub)
- **API Keys**: SHODAN_API_KEY, VIRUSTOTAL_API_KEY, etc.

### 4. GHunt
- **Image**: `ghunt-mcp-server:latest`
- **Tool**: Google account information search
- **Dependencies**: GHunt (cloned from GitHub)
- **API Keys**: GOOGLE_API_KEY, GOOGLE_CX

### 5. Maigret
- **Image**: `maigret-mcp-server:latest`
- **Tool**: Username search across 3000+ sites
- **Dependencies**: maigret

### 6. theHarvester
- **Image**: `theharvester-mcp-server:latest`
- **Tool**: Domain/email enumeration
- **Dependencies**: theharvester (with patches)
- **API Keys**: HUNTER_API_KEY, BING_API_KEY, SHODAN_API_KEY, SECURITYTRAILS_API_KEY

### 7. Blackbird
- **Image**: `blackbird-mcp-server:latest`
- **Tool**: Fast username search across 581 sites
- **Dependencies**: Blackbird (cloned from GitHub)

## Quick Start

### Build All Services
```bash
cd services
docker-compose build
```

### Build Single Service
```bash
cd services/sherlock
docker build -t sherlock-mcp-server:latest .
```

### Test All Services
```bash
cd services
./test_all_services.sh
```

### Test Single Service
```bash
cd services/sherlock
python3 test_sherlock.py
```

### Run Service with Docker Compose
```bash
cd services
docker-compose up -d sherlock
```

### Publish Service to Docker Hub
```bash
cd services/sherlock
./publish_to_docker.sh v1.0.0
```

## Key Differences from Monolithic Server

1. **Smaller Containers**: Each container only includes one tool (~50-70% smaller)
2. **Faster Builds**: Only rebuild containers for changed tools
3. **Independent Scaling**: Scale individual tools as needed
4. **Better Isolation**: Issues with one tool don't affect others
5. **Selective Deployment**: Deploy only the tools you need

## Original Codebase

The original monolithic server is preserved in the root directory:
- `src/osint_tools_mcp_server.py` - Original combined server
- `Dockerfile` - Original combined container
- `test_all_tools.py` - Original combined tests

## Testing Status

All services have been created with:
- ✅ Individual MCP server implementations
- ✅ Separate Dockerfiles
- ✅ Individual test suites
- ✅ Publishing scripts
- ✅ Docker Compose orchestration

Ready for testing and deployment!

