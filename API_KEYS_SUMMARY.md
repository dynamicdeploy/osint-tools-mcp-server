# API Keys Configuration Summary

## Current Setup: Free Sources Only (Default)

**By default, the MCP server uses only FREE/public sources.** All tools work without API keys, but with limited functionality:

- ✅ **Sherlock, Holehe, Maigret, Blackbird**: Fully functional without API keys
- ⚠️ **SpiderFoot**: Uses free modules only, skips premium modules requiring APIs
- ⚠️ **GHunt**: Uses public Google searches (limited)
- ⚠️ **theHarvester**: Uses free sources only (baidu, duckduckgo, etc.)

## How API Keys Work

### Method 1: Environment Variables (Recommended)

API keys are automatically passed to tools via environment variables. The `run_command_in_venv` function copies `os.environ`, so any environment variables set in Docker are available to all tools.

**Example:**
```bash
docker run --rm -i \
  -e SHODAN_API_KEY="your_key" \
  -e HUNTER_API_KEY="your_key" \
  osint-tools-mcp-server:latest
```

### Method 2: Docker Compose with .env File

1. Copy `.env.example` to `.env`:
   ```bash
   cp .env.example .env
   ```

2. Edit `.env` and add your API keys:
   ```bash
   SHODAN_API_KEY=your_actual_key_here
   HUNTER_API_KEY=your_actual_key_here
   ```

3. Docker Compose automatically loads `.env`:
   ```bash
   docker-compose up
   ```

### Method 3: Tool Parameters (theHarvester only)

For `theHarvester`, you can pass API keys directly in the tool call:

```json
{
  "name": "theharvester_domain_search",
  "arguments": {
    "domain": "example.com",
    "sources": "hunter",
    "hunter_api_key": "your_key_here"
  }
}
```

## Tools That Support API Keys

### 1. SpiderFoot
- **Environment Variables**: All API keys from environment are available
- **Common Keys**: `SHODAN_API_KEY`, `VIRUSTOTAL_API_KEY`, `HAVEIBEENPWNED_API_KEY`, etc.
- **Config File**: `/opt/spiderfoot/spiderfoot.cfg` (can be mounted as volume)

### 2. GHunt
- **Environment Variables**: `GOOGLE_API_KEY`, `GOOGLE_CX`
- **Config File**: `/opt/ghunt/.env` (can be mounted as volume)

### 3. theHarvester
- **Environment Variables**: `HUNTER_API_KEY`, `BING_API_KEY`, `SHODAN_API_KEY`, `SECURITYTRAILS_API_KEY`
- **Tool Parameters**: Can also pass keys via tool arguments (see above)

### 4. Other Tools
- **Sherlock, Holehe, Maigret, Blackbird**: No API keys needed (fully free)

## Testing API Key Configuration

### Test with Environment Variables:
```bash
# Test theHarvester with Hunter.io API key
echo '{"jsonrpc":"2.0","id":1,"method":"tools/call","params":{"name":"theharvester_domain_search","arguments":{"domain":"example.com","sources":"hunter"}}}' | \
  docker run --rm -i -e HUNTER_API_KEY="your_key" osint-tools-mcp-server:latest
```

### Test with Tool Parameters:
```bash
# Test theHarvester with API key in parameters
echo '{"jsonrpc":"2.0","id":1,"method":"tools/call","params":{"name":"theharvester_domain_search","arguments":{"domain":"example.com","sources":"hunter","hunter_api_key":"your_key"}}}' | \
  docker run --rm -i osint-tools-mcp-server:latest
```

## Security Notes

1. ✅ `.env` is already in `.gitignore` - your keys won't be committed
2. ⚠️ Never commit API keys to version control
3. ✅ Use Docker secrets in production environments
4. ✅ Rotate keys regularly

## How API Keys Are Passed (Technical Flow)

**The mechanism**: Standard Unix/Python subprocess environment variable inheritance

1. **Docker Environment** → Set via `-e KEY=value` or `.env` file
2. **Python os.environ** → Automatically contains all Docker env vars
3. **run_command_in_venv()** → Copies `os.environ` and passes to subprocess via `env=env`
4. **OSINT Tool** → Reads API keys from its environment (standard behavior)

**Code Flow**:
```python
# In run_command_in_venv():
env = os.environ.copy()  # All Docker env vars
if extra_env:
    env.update(extra_env)  # Add tool parameters (theHarvester)
subprocess_exec(..., env=env)  # Pass to tool subprocess
```

**See `API_KEY_FLOW.md` for detailed technical explanation with diagrams and code examples.**

## Implementation Details

The code has been updated to:

1. ✅ Support environment variables (automatically passed via `os.environ`)
2. ✅ Support tool parameters for theHarvester (optional API keys in arguments)
3. ✅ Updated tool schemas to document API key support
4. ✅ Created `.env.example` template file
5. ✅ Updated `docker-compose.yml` to load `.env` file
6. ✅ Created `API_KEY_FLOW.md` with detailed technical explanation

## Next Steps

To use API keys:

1. **Copy `.env.example` to `.env`**
2. **Add your API keys to `.env`**
3. **Run with Docker Compose** (automatically loads `.env`)
   OR
4. **Pass environment variables directly** when running Docker

The tools will automatically use the API keys when available, falling back to free sources if keys are not provided.

