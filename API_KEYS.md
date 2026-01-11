# API Keys and Configuration Guide

## Current State

**The current setup uses only FREE/public sources by default.** No API keys are required for basic functionality, but many tools can be enhanced with API keys for:
- Higher rate limits
- Access to premium data sources
- More comprehensive results
- Additional features

## Tools That Support API Keys

### 1. **SpiderFoot** 🕷️
- **Config File**: `/opt/spiderfoot/spiderfoot.cfg`
- **API Keys Supported**:
  - Shodan API
  - VirusTotal API
  - HaveIBeenPwned API
  - AbuseIPDB API
  - Censys API
  - And 100+ more modules
- **Current Behavior**: Uses free modules only, skips modules requiring APIs
- **Enhancement**: Configure API keys in `spiderfoot.cfg` for full functionality

### 2. **GHunt** 🔎
- **Config File**: `/opt/ghunt/.env` or environment variables
- **API Keys Supported**:
  - Google API Key (for enhanced searches)
  - Google CX (Custom Search Engine ID)
  - Google OAuth tokens (for authenticated searches)
- **Current Behavior**: Uses public Google searches (limited)
- **Enhancement**: Add Google API keys for better results

### 3. **theHarvester** 🌾
- **Command-line flags**: API keys passed via environment variables or command args
- **API Keys Supported**:
  - Bing API (`-b bingapi` requires `BING_API_KEY`)
  - Hunter.io (`-b hunter` requires `HUNTER_API_KEY`)
  - Shodan (`-b shodan` requires `SHODAN_API_KEY`)
  - SecurityTrails (`-b securityTrails` requires `SECURITYTRAILS_API_KEY`)
  - And more...
- **Current Behavior**: Uses free sources only (baidu, duckduckgo, etc.)
- **Enhancement**: Pass API keys via environment variables

### 4. **Sherlock** 🔍
- **Mostly Free**: No API keys required
- **Optional**: Some sites may require authentication (handled automatically)

### 5. **Holehe** 📧
- **Free**: No API keys required
- **All 120+ platforms checked without API keys**

### 6. **Maigret** 🌐
- **Free**: No API keys required
- **All 3000+ sites checked without API keys**

### 7. **Blackbird** 🐦
- **Free**: No API keys required
- **All 581 sites checked without API keys**

## How API Keys Are Passed to Tools

**Technical Flow**: Docker environment variables → Python `os.environ` → `run_command_in_venv()` function → Subprocess environment → OSINT tools read from environment

The MCP server uses Python's standard subprocess mechanism:
1. All Docker environment variables are automatically available in Python's `os.environ`
2. The `run_command_in_venv()` function copies `os.environ` and passes it to subprocesses via `env=env`
3. OSINT tools read API keys from their environment (standard Unix/Python behavior)

**See `API_KEY_FLOW.md` for detailed technical explanation with code examples.**

## How to Add API Keys

### Method 1: Environment Variables (Recommended for Docker)

Pass API keys as environment variables when running the Docker container:

```bash
docker run --rm -i \
  -e SHODAN_API_KEY="your_shodan_key" \
  -e VIRUSTOTAL_API_KEY="your_vt_key" \
  -e HUNTER_API_KEY="your_hunter_key" \
  -e GOOGLE_API_KEY="your_google_key" \
  -e GOOGLE_CX="your_cx_id" \
  osint-tools-mcp-server:latest
```

**How it works**: These environment variables are automatically inherited by the Python process (`os.environ`) and passed to all tool subprocesses via the `run_command_in_venv()` function.

### Method 2: Config Files (Mount Volumes)

Create config files locally and mount them into the container:

```bash
# Create SpiderFoot config
cat > spiderfoot.cfg << EOF
[modules]
shodan_api_key = your_shodan_key
virustotal_api_key = your_vt_key
EOF

# Create GHunt .env
cat > ghunt.env << EOF
GOOGLE_API_KEY=your_google_key
GOOGLE_CX=your_cx_id
EOF

# Run with mounted configs
docker run --rm -i \
  -v $(pwd)/spiderfoot.cfg:/opt/spiderfoot/spiderfoot.cfg:ro \
  -v $(pwd)/ghunt.env:/opt/ghunt/.env:ro \
  osint-tools-mcp-server:latest
```

### Method 3: Docker Compose with Environment File

Create a `.env` file:

```bash
# .env
SHODAN_API_KEY=your_shodan_key
VIRUSTOTAL_API_KEY=your_vt_key
HUNTER_API_KEY=your_hunter_key
GOOGLE_API_KEY=your_google_key
GOOGLE_CX=your_cx_id
```

Update `docker-compose.yml`:

```yaml
services:
  osint-mcp:
    build: .
    image: osint-tools-mcp-server:latest
    env_file:
      - .env
    environment:
      - PYTHONUNBUFFERED=1
    volumes:
      - ./reports:/app/reports
    stdin_open: true
    tty: true
```

### Method 4: Tool-Specific Parameters (theHarvester Only)

For `theHarvester`, you can pass API keys directly in the tool call. These are converted to environment variables and passed to the tool:

```json
{
  "name": "theharvester_domain_search",
  "arguments": {
    "domain": "example.com",
    "sources": "hunter",
    "hunter_api_key": "optional_api_key_here"
  }
}
```

**How it works**: The `handle_theharvester()` function extracts API key parameters, converts them to environment variable format (e.g., `hunter_api_key` → `HUNTER_API_KEY`), and passes them to `run_command_in_venv()` via the `extra_env` parameter. These are merged with `os.environ` before creating the subprocess.

## Security Best Practices

1. **Never commit API keys to git**
   - Add `.env` to `.gitignore`
   - Use environment variables or secrets management

2. **Use Docker secrets** (for production):
   ```bash
   echo "your_api_key" | docker secret create shodan_api_key -
   ```

3. **Rotate keys regularly**
   - Update keys periodically
   - Revoke old keys when rotating

4. **Limit key permissions**
   - Use read-only keys when possible
   - Set rate limits on API keys

## Testing API Key Configuration

### Test SpiderFoot with API keys:
```bash
# Set environment variable
export SHODAN_API_KEY="your_key"

# Run SpiderFoot scan
docker run --rm -i \
  -e SHODAN_API_KEY="$SHODAN_API_KEY" \
  osint-tools-mcp-server:latest
```

### Test theHarvester with Hunter.io:
```bash
docker run --rm -i \
  -e HUNTER_API_KEY="your_hunter_key" \
  osint-tools-mcp-server:latest
```

## Current Limitations

1. **No API key validation**: The server doesn't validate if API keys are working
2. **No key management UI**: Keys must be configured manually
3. **No per-request keys**: All requests use the same configured keys
4. **No key rotation**: Keys must be manually updated

## Future Enhancements

- [ ] Add API key parameters to tool schemas
- [ ] Implement API key validation
- [ ] Add key rotation support
- [ ] Create key management interface
- [ ] Support per-request API keys
- [ ] Add API key usage monitoring

