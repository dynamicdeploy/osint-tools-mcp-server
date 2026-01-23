# Docker Hub Publishing Status

## Current Status: **NOT PUBLISHED** ❌

None of the individual OSINT Tools MCP services have been published to Docker Hub yet.

## Services Status

| Service | Docker Hub Image | Status |
|---------|-----------------|--------|
| Sherlock | `hackerdogs/sherlock-mcp-server` | ❌ Not Published |
| Holehe | `hackerdogs/holehe-mcp-server` | ❌ Not Published |
| Maigret | `hackerdogs/maigret-mcp-server` | ❌ Not Published |
| Blackbird | `hackerdogs/blackbird-mcp-server` | ❌ Not Published |
| SpiderFoot | `hackerdogs/spiderfoot-mcp-server` | ❌ Not Published |
| GHunt | `hackerdogs/ghunt-mcp-server` | ❌ Not Published |
| theHarvester | `hackerdogs/theharvester-mcp-server` | ❌ Not Published |

## Original Monolithic Server

| Service | Docker Hub Image | Status |
|---------|-----------------|--------|
| Combined | `hackerdogs/osint-tools-mcp-server` | ❓ Unknown (not checked) |

## How to Publish

Each service has its own publishing script. To publish a service:

### 1. Login to Docker Hub

```bash
docker login
```

### 2. Navigate to Service Directory

```bash
cd services/sherlock  # or any other service
```

### 3. Run Publish Script

```bash
# Publish with 'latest' tag only
./publish_to_docker.sh

# Publish with version tag
./publish_to_docker.sh v1.0.0
```

### 4. Publish All Services

You can publish all services by running the script in each directory:

```bash
cd services
for service in sherlock holehe maigret blackbird spiderfoot ghunt theharvester; do
    echo "Publishing $service..."
    cd $service
    ./publish_to_docker.sh
    cd ..
done
```

## Publishing Scripts Location

All services have `publish_to_docker.sh` scripts:
- `services/sherlock/publish_to_docker.sh`
- `services/holehe/publish_to_docker.sh`
- `services/maigret/publish_to_docker.sh`
- `services/blackbird/publish_to_docker.sh`
- `services/spiderfoot/publish_to_docker.sh`
- `services/ghunt/publish_to_docker.sh`
- `services/theharvester/publish_to_docker.sh`

## Docker Hub Account

All images will be published under: **`hackerdogs/`**

## Expected Docker Hub URLs

Once published, images will be available at:
- https://hub.docker.com/r/hackerdogs/sherlock-mcp-server
- https://hub.docker.com/r/hackerdogs/holehe-mcp-server
- https://hub.docker.com/r/hackerdogs/maigret-mcp-server
- https://hub.docker.com/r/hackerdogs/blackbird-mcp-server
- https://hub.docker.com/r/hackerdogs/spiderfoot-mcp-server
- https://hub.docker.com/r/hackerdogs/ghunt-mcp-server
- https://hub.docker.com/r/hackerdogs/theharvester-mcp-server

## Pull Commands (After Publishing)

```bash
# Pull individual services
docker pull hackerdogs/sherlock-mcp-server:latest
docker pull hackerdogs/holehe-mcp-server:latest
docker pull hackerdogs/maigret-mcp-server:latest
docker pull hackerdogs/blackbird-mcp-server:latest
docker pull hackerdogs/spiderfoot-mcp-server:latest
docker pull hackerdogs/ghunt-mcp-server:latest
docker pull hackerdogs/theharvester-mcp-server:latest
```

## Notes

- All services are **ready to be published** - they build successfully and pass tests
- Each service can be published independently
- Version tags can be added during publishing
- Make sure you're logged into Docker Hub before publishing
