# Publishing Guide - All OSINT Tools MCP Services

## Quick Start

To publish all services to Docker Hub:

```bash
cd services
./publish_all_services.sh
```

Or with a version tag:

```bash
./publish_all_services.sh v1.0.0
```

## Prerequisites

1. **Docker must be running**
   ```bash
   docker info
   ```

2. **Login to Docker Hub**
   ```bash
   docker login
   ```
   Enter your Docker Hub username and password/token

3. **Ensure all services are built**
   ```bash
   docker-compose build
   ```

## Publishing Options

### Option 1: Publish All Services (Recommended)

Use the automated script to publish all services at once:

```bash
cd services
./publish_all_services.sh [version]
```

**Examples:**
```bash
# Publish all with 'latest' tag only
./publish_all_services.sh

# Publish all with version tag
./publish_all_services.sh v1.0.0
```

### Option 2: Publish Individual Services

Navigate to each service directory and run its publish script:

```bash
# Example: Publish Sherlock
cd services/sherlock
./publish_to_docker.sh v1.0.0
cd ..

# Example: Publish Holehe
cd services/holehe
./publish_to_docker.sh v1.0.0
cd ..
```

### Option 3: Publish Services in Loop

```bash
cd services
for service in sherlock holehe maigret blackbird spiderfoot ghunt theharvester; do
    echo "Publishing $service..."
    cd $service
    ./publish_to_docker.sh v1.0.0
    cd ..
done
```

## What Gets Published

Each service will be published as:
- `hackerdogs/{service}-mcp-server:latest`
- `hackerdogs/{service}-mcp-server:{version}` (if version specified)

**Services:**
1. `hackerdogs/sherlock-mcp-server`
2. `hackerdogs/holehe-mcp-server`
3. `hackerdogs/maigret-mcp-server`
4. `hackerdogs/blackbird-mcp-server`
5. `hackerdogs/spiderfoot-mcp-server`
6. `hackerdogs/ghunt-mcp-server`
7. `hackerdogs/theharvester-mcp-server`

## Publishing Process

The `publish_all_services.sh` script will:

1. ✅ Check Docker is running
2. ✅ Check Docker Hub login status
3. ✅ Ask for confirmation
4. ✅ Build each service (if needed)
5. ✅ Tag images for Docker Hub
6. ✅ Push images to Docker Hub
7. ✅ Provide summary of results

## Expected Output

```
==========================================
Publishing All OSINT Tools MCP Services
==========================================

ℹ️  Version: latest
ℹ️  Services to publish: 7

⚠️  This will publish 7 services to Docker Hub
ℹ️  Services: sherlock holehe maigret blackbird spiderfoot ghunt theharvester
Continue? (y/n) y

==========================================
Publishing sherlock Service
==========================================
...

==========================================
Publishing Summary
==========================================
✅ Successfully published: 7/7
✅ All services published successfully!
```

## Verification

After publishing, verify on Docker Hub:

1. Visit: https://hub.docker.com/r/hackerdogs/
2. Check each repository:
   - https://hub.docker.com/r/hackerdogs/sherlock-mcp-server
   - https://hub.docker.com/r/hackerdogs/holehe-mcp-server
   - etc.

Or test pulling an image:

```bash
docker pull hackerdogs/sherlock-mcp-server:latest
```

## Troubleshooting

### Issue: "Docker is not running"
**Solution:** Start Docker Desktop

### Issue: "Not logged into Docker Hub"
**Solution:** Run `docker login`

### Issue: "Permission denied"
**Solution:** Make scripts executable:
```bash
chmod +x publish_all_services.sh
chmod +x */publish_to_docker.sh
```

### Issue: "Build failed"
**Solution:** Ensure all services build successfully first:
```bash
docker-compose build
```

### Issue: "Push failed - unauthorized"
**Solution:** 
- Check Docker Hub login: `docker info | grep Username`
- Re-login: `docker logout && docker login`
- Verify you have push access to `hackerdogs` organization

## Time Estimates

- **Per service**: ~2-5 minutes (depending on image size and network speed)
- **All services**: ~15-35 minutes total

## Notes

- Publishing requires internet connection
- Large images may take longer to push
- Docker Hub has rate limits for free accounts
- Version tags are optional but recommended for production

## After Publishing

Once published, users can pull and use the services:

```bash
# Pull a service
docker pull hackerdogs/sherlock-mcp-server:latest

# Run a service
docker run --rm -i hackerdogs/sherlock-mcp-server:latest
```

## Support

If you encounter issues:
1. Check Docker Hub status: https://status.docker.com/
2. Verify Docker Hub account permissions
3. Check network connectivity
4. Review Docker logs: `docker logs <container>`
