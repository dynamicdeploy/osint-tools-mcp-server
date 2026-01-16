# Docker-based MCP Server Usage Guide

This guide explains how to use the OSINT Tools MCP Server as a Docker container.

## Quick Start

### Build the Docker Image

```bash
docker build -t osint-tools-mcp-server:latest .
```

### Run the Container

The MCP server communicates via stdio (standard input/output), so you can run it interactively:

```bash
docker run --rm -i osint-tools-mcp-server:latest
```

### Using with Docker Compose

```bash
docker-compose up
```

## Testing the MCP Server

### Run Functional Tests

```bash
# Test the Docker image
./test_docker.sh

# Test MCP server functionality
python3 test_mcp_functional.py
```

### Manual Testing

You can test the MCP server manually by sending JSON-RPC requests:

```bash
# Initialize
echo '{"jsonrpc":"2.0","id":1,"method":"initialize","params":{"protocolVersion":"2024-11-05","capabilities":{},"clientInfo":{"name":"test","version":"1.0.0"}}}' | docker run --rm -i osint-tools-mcp-server:latest

# List tools
echo '{"jsonrpc":"2.0","id":2,"method":"tools/list"}' | docker run --rm -i osint-tools-mcp-server:latest

# Call a tool
echo '{"jsonrpc":"2.0","id":3,"method":"tools/call","params":{"name":"holehe_email_search","arguments":{"email":"test@example.com","timeout":5}}}' | docker run --rm -i osint-tools-mcp-server:latest
```

## Using with Claude Desktop

To use this Docker-based MCP server with Claude Desktop, you need to configure it to run the Docker container. Add this to your Claude Desktop configuration:

**macOS**: `~/Library/Application Support/Claude/claude_desktop_config.json`
**Windows**: `%APPDATA%\Claude\claude_desktop_config.json`
**Linux**: `~/.config/Claude/claude_desktop_config.json`

```json
{
  "mcpServers": {
    "osint-tools-docker": {
      "command": "docker",
      "args": [
        "run",
        "--rm",
        "-i",
        "osint-tools-mcp-server:latest"
      ],
      "env": {
        "PYTHONUNBUFFERED": "1"
      }
    }
  }
}
```

**Note**: Make sure Docker is running and the image is built before starting Claude Desktop.

## Available Tools

The Docker container exposes all 7 OSINT tools:

1. **sherlock_username_search** - Search for username across 399+ platforms
2. **holehe_email_search** - Check if email is registered on 120+ platforms
3. **spiderfoot_scan** - Comprehensive OSINT scan
4. **ghunt_google_search** - Google account information
5. **maigret_username_search** - Advanced username search across 3000+ sites
6. **theharvester_domain_search** - Domain intelligence gathering
7. **blackbird_username_search** - Fast username search across 581 sites

## Troubleshooting

### Container won't start
- Ensure Docker is running: `docker ps`
- Check if image exists: `docker images | grep osint-tools-mcp-server`

### Tools not working
- Verify tools are installed in container:
  ```bash
  docker run --rm osint-tools-mcp-server:latest which sherlock holehe maigret
  ```

### Timeout issues
- Some tools (especially SpiderFoot) can take a long time. Increase timeout parameters in tool calls.

## Development

### Rebuilding the Image

```bash
docker build --no-cache -t osint-tools-mcp-server:latest .
```

### Inspecting the Container

```bash
# Run an interactive shell
docker run --rm -it osint-tools-mcp-server:latest /bin/bash

# Check installed tools
docker run --rm osint-tools-mcp-server:latest which sherlock holehe maigret
```

### Viewing Logs

Since MCP uses stdio, logs go to stdout/stderr. You can capture them:

```bash
docker run --rm -i osint-tools-mcp-server:latest 2>&1 | tee mcp.log
```


