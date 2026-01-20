# OSINT Tools MCP Services

This directory contains individual MCP server services, each dedicated to a single OSINT tool. Each service has its own Docker container, test suite, and publishing script.

## Structure

Each service directory contains:
- `src/` - MCP server source code
- `Dockerfile` - Container definition
- `requirements.txt` - Python dependencies
- `publish_to_docker.sh` - Script to publish to Docker Hub
- `test_*.py` - Test suite for the service

## Services

1. **sherlock** - Username search across 399+ platforms
2. **holehe** - Email registration check on 120+ platforms
3. **spiderfoot** - Comprehensive OSINT scan
4. **ghunt** - Google account information search
5. **maigret** - Username search across 3000+ sites
6. **theharvester** - Domain/email enumeration
7. **blackbird** - Fast username search across 581 sites

## Building Individual Services

### Build a single service:

```bash
cd services/sherlock
docker build -t sherlock-mcp-server:latest .
```

### Build all services:

```bash
cd services
docker-compose build
```

## Testing

### Test a single service:

```bash
cd services/sherlock
python3 test_sherlock.py
```

### Test all services:

```bash
cd services
./test_all_services.sh
```

### Test a specific service:

```bash
cd services
./test_all_services.sh sherlock
```

## Running Services

### Using Docker Compose:

```bash
cd services
docker-compose up -d sherlock
```

### Using Docker directly:

```bash
docker run --rm -i sherlock-mcp-server:latest
```

## Publishing to Docker Hub

Each service has its own publishing script:

```bash
cd services/sherlock
./publish_to_docker.sh [version]
```

Example:
```bash
./publish_to_docker.sh v1.0.0
```

## Docker Compose

The `docker-compose.yml` file defines all services. You can:

- Start all services: `docker-compose up -d`
- Start a specific service: `docker-compose up -d sherlock`
- Stop all services: `docker-compose down`
- View logs: `docker-compose logs -f sherlock`

## Differences from Monolithic Server

The original `osint-tools-mcp-server` contains all tools in a single container. This separated architecture provides:

1. **Smaller containers** - Each container only includes one tool and its dependencies
2. **Independent scaling** - Scale individual tools as needed
3. **Faster builds** - Only rebuild containers for changed tools
4. **Better isolation** - Issues with one tool don't affect others
5. **Selective deployment** - Deploy only the tools you need

## Notes

- The original monolithic server is preserved in the root directory
- Each service is completely independent
- API keys can be provided via environment variables or `.env` file
- All services use the same MCP protocol over stdio

