# Publishing Guide

## Publishing to Docker Hub

### Quick Start

Publish the Docker image to Docker Hub under the `hackerdogs` account:

```bash
# Publish with 'latest' tag only
./publish_to_docker.sh

# Publish with version tag
./publish_to_docker.sh v1.0.0
```

### Prerequisites

1. **Docker installed and running**
   ```bash
   docker --version
   docker info
   ```

2. **Logged into Docker Hub**
   ```bash
   docker login
   ```
   Enter your Docker Hub credentials when prompted.

3. **Permissions**
   - You must have push access to the `hackerdogs` Docker Hub account
   - The repository `hackerdogs/osint-tools-mcp-server` should exist (or will be created on first push)

### Publishing Steps

The `publish_to_docker.sh` script automates the following:

1. **Checks Docker is running**
2. **Verifies Docker Hub login**
3. **Builds the Docker image** (`osint-tools-mcp-server:latest`)
4. **Tags the image** for Docker Hub:
   - `hackerdogs/osint-tools-mcp-server:latest`
   - `hackerdogs/osint-tools-mcp-server:v1.0.0` (if version provided)
5. **Pushes to Docker Hub**
6. **Verifies the push**

### Manual Publishing

If you prefer to publish manually:

```bash
# 1. Build the image
docker build -t osint-tools-mcp-server:latest .

# 2. Tag for Docker Hub
docker tag osint-tools-mcp-server:latest hackerdogs/osint-tools-mcp-server:latest
docker tag osint-tools-mcp-server:latest hackerdogs/osint-tools-mcp-server:v1.0.0

# 3. Push to Docker Hub
docker push hackerdogs/osint-tools-mcp-server:latest
docker push hackerdogs/osint-tools-mcp-server:v1.0.0
```

### Using the Published Image

After publishing, users can pull and use the image:

```bash
# Pull the image
docker pull hackerdogs/osint-tools-mcp-server:latest

# Or with version
docker pull hackerdogs/osint-tools-mcp-server:v1.0.0

# Run the MCP server
docker run --rm -i hackerdogs/osint-tools-mcp-server:latest
```

### Configuration for Claude Desktop

Users can configure Claude Desktop to use the published image:

```json
{
  "mcpServers": {
    "osint-tools": {
      "command": "docker",
      "args": [
        "run",
        "--rm",
        "-i",
        "hackerdogs/osint-tools-mcp-server:latest"
      ],
      "env": {
        "PYTHONUNBUFFERED": "1"
      }
    }
  }
}
```

### Versioning Strategy

- **`latest`**: Always points to the most recent stable release
- **`v1.0.0`**: Semantic version tags for specific releases
- **`v1.0.1`**: Patch releases (bug fixes)
- **`v1.1.0`**: Minor releases (new features)
- **`v2.0.0`**: Major releases (breaking changes)

### Troubleshooting

#### "Cannot connect to Docker daemon"
- Ensure Docker Desktop is running
- Check Docker daemon status: `docker info`

#### "denied: requested access to the resource is denied"
- Verify you're logged in: `docker login`
- Check you have push permissions to `hackerdogs` account
- Ensure the repository name is correct

#### "repository does not exist"
- The repository will be created automatically on first push
- Ensure the repository name matches: `hackerdogs/osint-tools-mcp-server`

#### Build fails
- Check Dockerfile syntax
- Verify all dependencies are available
- Review build logs for specific errors

### Verification

After publishing, verify the image is available:

1. **Check Docker Hub**: https://hub.docker.com/r/hackerdogs/osint-tools-mcp-server
2. **Test pull locally**:
   ```bash
   docker pull hackerdogs/osint-tools-mcp-server:latest
   docker run --rm hackerdogs/osint-tools-mcp-server:latest --help
   ```

### CI/CD Integration

For automated publishing, you can integrate this script into CI/CD pipelines:

```yaml
# Example GitHub Actions
- name: Publish to Docker Hub
  run: |
    echo "${{ secrets.DOCKER_PASSWORD }}" | docker login -u "${{ secrets.DOCKER_USERNAME }}" --password-stdin
    ./publish_to_docker.sh ${{ github.ref_name }}
```

### Security Notes

- Never commit Docker Hub credentials to the repository
- Use environment variables or secrets management for credentials
- Consider using Docker Hub access tokens instead of passwords
- Enable 2FA on Docker Hub account


