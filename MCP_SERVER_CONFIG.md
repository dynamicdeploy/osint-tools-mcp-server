# MCP Server Configuration Guide

## Claude Desktop Configuration

To use the OSINT Tools MCP Server with Claude Desktop, you need to add it to your Claude Desktop configuration file.

### Configuration File Locations

- **macOS**: `~/Library/Application Support/Claude/claude_desktop_config.json`
- **Windows**: `%APPDATA%\Claude\claude_desktop_config.json`
- **Linux**: `~/.config/Claude/claude_desktop_config.json`

### Basic Configuration (No API Keys)

If you want to use the server with free sources only:

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

### Full Configuration with API Keys

⚠️ **Important**: The API keys in `mcpServer.json` include many unverified key names. See `API_KEYS_VERIFICATION.md` for details.

For verified API keys, use `mcpServer.json.verified` which contains only keys confirmed to work:

For enhanced functionality with API keys, use `mcpServer.json.verified` or `mcpServer.json.example` as a template:

1. **Copy the example file**:
   ```bash
   cp mcpServer.json.example ~/Library/Application\ Support/Claude/claude_desktop_config.json
   ```

2. **Edit the file** and replace placeholder values with your actual API keys:
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
           "PYTHONUNBUFFERED": "1",
           "SHODAN_API_KEY": "your_actual_shodan_key",
           "VIRUSTOTAL_API_KEY": "your_actual_vt_key",
           "HUNTER_API_KEY": "your_actual_hunter_key"
         }
       }
     }
   }
   ```

3. **Restart Claude Desktop** to load the configuration.

### Complete API Keys List

The `mcpServer.json` file includes all supported API keys organized by tool:

#### SpiderFoot API Keys
- `SHODAN_API_KEY` - Shodan internet search
- `VIRUSTOTAL_API_KEY` - VirusTotal malware analysis
- `HAVEIBEENPWNED_API_KEY` - Have I Been Pwned breach database
- `ABUSEIPDB_API_KEY` - AbuseIPDB IP reputation
- `CENSYS_API_ID` / `CENSYS_API_SECRET` - Censys internet search
- And 50+ more (see `mcpServer.json` for complete list)

#### GHunt API Keys
- `GOOGLE_API_KEY` - Google Custom Search API
- `GOOGLE_CX` - Google Custom Search Engine ID
- `GOOGLE_CLIENT_ID` / `GOOGLE_CLIENT_SECRET` - OAuth for authenticated searches

#### theHarvester API Keys
- `HUNTER_API_KEY` - Hunter.io email finder
- `BING_API_KEY` - Bing Search API
- `SHODAN_API_KEY` - Shodan search
- `SECURITYTRAILS_API_KEY` - SecurityTrails domain intelligence
- And more...

### Merging with Existing Configuration

If you already have other MCP servers configured, merge the configuration:

```json
{
  "mcpServers": {
    "existing-server": {
      "command": "python",
      "args": ["path/to/existing/server.py"]
    },
    "osint-tools-docker": {
      "command": "docker",
      "args": [
        "run",
        "--rm",
        "-i",
        "osint-tools-mcp-server:latest"
      ],
      "env": {
        "PYTHONUNBUFFERED": "1",
        "SHODAN_API_KEY": "your_key"
      }
    }
  }
}
```

### Security Notes

⚠️ **Important**: The Claude Desktop configuration file may contain sensitive API keys. 

1. **Never commit** `claude_desktop_config.json` to version control
2. **Use environment variables** for sensitive keys when possible
3. **Rotate keys regularly**
4. **Use read-only API keys** when available

### Alternative: Using .env File

Instead of putting API keys directly in the JSON file, you can:

1. Create a `.env` file with your keys
2. Use Docker Compose (which loads `.env` automatically)
3. Or use a wrapper script that loads `.env` before running Docker

### Verification

After configuring, verify the setup:

1. **Check Docker image exists**:
   ```bash
   docker images | grep osint-tools-mcp-server
   ```

2. **Test Docker command manually**:
   ```bash
   echo '{"jsonrpc":"2.0","id":1,"method":"initialize"}' | \
     docker run --rm -i osint-tools-mcp-server:latest
   ```

3. **Restart Claude Desktop** and check for the server in the MCP panel

### Troubleshooting

**Server not appearing in Claude Desktop:**
- Verify Docker is running: `docker ps`
- Check configuration file syntax: `cat ~/Library/Application\ Support/Claude/claude_desktop_config.json | python3 -m json.tool`
- Check Claude Desktop logs for errors

**API keys not working:**
- Verify keys are set correctly in the `env` section
- Test keys manually: `docker run --rm -i -e SHODAN_API_KEY="your_key" osint-tools-mcp-server:latest`
- Check tool-specific documentation for key format requirements

**Docker command not found:**
- Ensure Docker is installed and in PATH
- On macOS, Docker Desktop must be running
- Try full path: `/usr/local/bin/docker` or `/Applications/Docker.app/Contents/Resources/bin/docker`

