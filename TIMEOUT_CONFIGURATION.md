# Timeout Configuration Guide

## Overview

All OSINT tools support configurable timeouts. Timeouts can be set per-tool via the `timeout` parameter in tool arguments.

## Tool Timeout Support

| Tool | Timeout Parameter | Default | Recommended |
|------|------------------|---------|-------------|
| Sherlock | ✅ `timeout` | 10000s | 300-600s |
| Holehe | ✅ `timeout` | 10000s | 30-60s |
| Maigret | ✅ `timeout` | 10000s | 60-120s |
| Blackbird | ✅ `timeout` | 10000s | 60-120s |
| GHunt | ✅ `timeout` | 10000s | 30-60s |
| theHarvester | ❌ N/A | Tool default | N/A |
| SpiderFoot | ✅ `timeout` | Varies | 300-600s+ |

## Usage Examples

### Setting Timeout in Tool Call

```json
{
  "jsonrpc": "2.0",
  "id": 1,
  "method": "tools/call",
  "params": {
    "name": "sherlock_username_search",
    "arguments": {
      "username": "testuser",
      "timeout": 300
    }
  }
}
```

### Fast Tools (30-60 seconds)

**Holehe:**
```json
{
  "name": "holehe_email_search",
  "arguments": {
    "email": "test@example.com",
    "timeout": 60
  }
}
```

**GHunt:**
```json
{
  "name": "ghunt_google_search",
  "arguments": {
    "identifier": "test@gmail.com",
    "timeout": 60
  }
}
```

### Medium Tools (60-120 seconds)

**Maigret:**
```json
{
  "name": "maigret_username_search",
  "arguments": {
    "username": "testuser",
    "timeout": 120
  }
}
```

**Blackbird:**
```json
{
  "name": "blackbird_username_search",
  "arguments": {
    "username": "testuser",
    "timeout": 120
  }
}
```

### Slow Tools (300+ seconds)

**Sherlock:**
```json
{
  "name": "sherlock_username_search",
  "arguments": {
    "username": "testuser",
    "timeout": 600,
    "sites": ["twitter", "github", "reddit"]
  }
}
```

**SpiderFoot:**
```json
{
  "name": "spiderfoot_scan",
  "arguments": {
    "target": "example.com",
    "modules": "sfp_dnsresolve",
    "timeout": 600
  }
}
```

## MCP Client Timeout

In addition to tool timeouts, you may need to configure the MCP client timeout:

### Claude Desktop Configuration

```json
{
  "mcpServers": {
    "osint-tools": {
      "command": "docker",
      "args": [
        "run",
        "--rm",
        "-i",
        "osint-tools-mcp-server:latest"
      ],
      "timeout": 600
    }
  }
}
```

### Python Client Example

```python
response = send_mcp_request(
    docker_cmd,
    "tools/call",
    {
        "name": "sherlock_username_search",
        "arguments": {
            "username": "testuser",
            "timeout": 300
        }
    },
    timeout=600  # MCP client timeout
)
```

## Timeout Best Practices

1. **Start with Defaults**: Use default timeouts (10000s) for initial testing
2. **Adjust Based on Results**: Reduce timeouts for faster tools, increase for comprehensive scans
3. **Use Site Filtering**: For Sherlock, use `sites` parameter to limit scope
4. **Monitor Performance**: Track actual execution times and adjust accordingly
5. **Handle Timeouts Gracefully**: Check for timeout errors and retry with longer timeouts if needed

## Troubleshooting

### Tool Times Out

**Solution**: Increase the timeout parameter:
```json
{
  "timeout": 1800  // 30 minutes
}
```

### MCP Client Times Out

**Solution**: Increase MCP client timeout in configuration:
```json
{
  "timeout": 1800
}
```

### Tool Completes but Takes Too Long

**Solution**: 
- Use smaller test sets (Sherlock: `sites` parameter)
- Use specific modules (SpiderFoot: `modules` parameter)
- Reduce scope (theHarvester: `limit` parameter)

## Notes

- **Default timeout (10000s)**: Very generous, suitable for comprehensive scans
- **Tool timeouts**: Control how long the tool waits for each site/request
- **MCP client timeout**: Controls how long the client waits for the tool to complete
- **theHarvester**: Uses internal limits (`limit` parameter) instead of timeout


