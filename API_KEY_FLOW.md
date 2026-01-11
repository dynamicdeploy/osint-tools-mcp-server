# API Key Flow: How Keys Are Passed from MCP Server to Tools

## Technical Flow Diagram

```
┌─────────────────────────────────────────────────────────────┐
│ 1. Docker Container Environment                            │
│    Environment variables set via:                          │
│    - docker run -e KEY=value                               │
│    - docker-compose.yml env_file: .env                     │
│    - docker-compose.yml environment:                       │
└─────────────────┬───────────────────────────────────────────┘
                  │
                  ▼
┌─────────────────────────────────────────────────────────────┐
│ 2. Python os.environ                                       │
│    All Docker environment variables automatically          │
│    available in Python's os.environ                       │
└─────────────────┬───────────────────────────────────────────┘
                  │
                  ▼
┌─────────────────────────────────────────────────────────────┐
│ 3. MCP Server (osint_tools_mcp_server.py)                 │
│                                                             │
│    run_command_in_venv() function:                        │
│    ┌─────────────────────────────────────────┐            │
│    │ env = os.environ.copy()                │            │
│    │ if extra_env:                           │            │
│    │     env.update(extra_env)               │            │
│    │                                         │            │
│    │ subprocess_exec(..., env=env)          │            │
│    └─────────────────────────────────────────┘            │
└─────────────────┬───────────────────────────────────────────┘
                  │
                  ▼
┌─────────────────────────────────────────────────────────────┐
│ 4. OSINT Tool Subprocess                                   │
│    Tool reads API keys from its environment:               │
│    - SpiderFoot: reads from os.environ                    │
│    - GHunt: reads from os.environ or .env file            │
│    - theHarvester: reads from os.environ                   │
└─────────────────────────────────────────────────────────────┘
```

## Detailed Implementation

### Step 1: Environment Variables in Docker

When you run the Docker container with environment variables:

```bash
docker run --rm -i \
  -e SHODAN_API_KEY="your_key" \
  -e HUNTER_API_KEY="your_key" \
  osint-tools-mcp-server:latest
```

These become part of the container's environment.

### Step 2: Python os.environ

The MCP server (Python process) automatically inherits all environment variables:

```python
# In osint_tools_mcp_server.py
import os

# os.environ contains all Docker environment variables
# Example: os.environ['SHODAN_API_KEY'] = "your_key"
```

### Step 3: run_command_in_venv Function

This is the key function that passes environment variables to tools:

```python
async def run_command_in_venv(
    command: List[str], 
    cwd: Optional[str] = None, 
    input_data: Optional[str] = None, 
    extra_env: Optional[Dict[str, str]] = None
) -> tuple[str, str, int]:
    """Run a command in the virtual environment."""
    # Step 3a: Copy all environment variables
    env = os.environ.copy()  # Includes all Docker env vars
    
    # Step 3b: Add any extra environment variables (from tool parameters)
    if extra_env:
        env.update(extra_env)
    
    # Step 3c: Create subprocess with environment
    process = await asyncio.create_subprocess_exec(
        *command,
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE,
        cwd=cwd,
        env=env,  # ← Environment variables passed here
        stdin=asyncio.subprocess.PIPE if input_data else None
    )
```

**Key Point**: The `env=env` parameter in `subprocess_exec` makes all environment variables available to the child process (the OSINT tool).

### Step 4: Tool-Specific Handling

#### For Most Tools (SpiderFoot, GHunt, etc.):

```python
# Example: handle_spiderfoot()
async def handle_spiderfoot(params: Dict[str, Any]) -> Dict[str, Any]:
    cmd = ["python3", "/opt/spiderfoot/sf.py", "-s", target, ...]
    
    # Environment variables automatically available via os.environ
    # SpiderFoot reads: os.environ.get('SHODAN_API_KEY')
    stdout, stderr, returncode = await run_command_in_venv(cmd)
```

**Flow**: Docker env → Python os.environ → subprocess env → Tool reads from environment

#### For theHarvester (with optional tool parameters):

```python
# Example: handle_theharvester()
async def handle_theharvester(params: Dict[str, Any]) -> Dict[str, Any]:
    # Step 1: Extract API keys from tool parameters (if provided)
    api_keys = {}
    if "hunter_api_key" in params:
        api_keys["HUNTER_API_KEY"] = params["hunter_api_key"]
    
    # Step 2: Pass to run_command_in_venv as extra_env
    stdout, stderr, returncode = await run_command_in_venv(
        cmd, 
        extra_env=api_keys  # ← Merged with os.environ in run_command_in_venv
    )
```

**Flow**: Tool parameter → extra_env dict → merged with os.environ → subprocess env → Tool reads

## Code Examples

### Example 1: Environment Variables (Automatic)

```python
# Docker command:
# docker run -e SHODAN_API_KEY="abc123" osint-tools-mcp-server:latest

# In Python:
print(os.environ.get('SHODAN_API_KEY'))  # Output: "abc123"

# When running SpiderFoot:
cmd = ["python3", "/opt/spiderfoot/sf.py", ...]
# SpiderFoot automatically sees SHODAN_API_KEY in its environment
await run_command_in_venv(cmd)  # env includes SHODAN_API_KEY
```

### Example 2: Tool Parameters (theHarvester)

```python
# MCP tool call:
{
  "name": "theharvester_domain_search",
  "arguments": {
    "domain": "example.com",
    "sources": "hunter",
    "hunter_api_key": "xyz789"  # ← Passed as parameter
  }
}

# In handle_theharvester():
api_keys = {"HUNTER_API_KEY": params["hunter_api_key"]}  # "xyz789"
await run_command_in_venv(cmd, extra_env=api_keys)

# In run_command_in_venv():
env = os.environ.copy()  # All Docker env vars
env.update(api_keys)     # Add HUNTER_API_KEY="xyz789"
# theHarvester sees HUNTER_API_KEY in its environment
```

### Example 3: Both Methods (Priority)

```python
# Docker: -e HUNTER_API_KEY="from_docker"
# Tool param: "hunter_api_key": "from_param"

# In handle_theharvester():
api_keys = {"HUNTER_API_KEY": "from_param"}
await run_command_in_venv(cmd, extra_env=api_keys)

# In run_command_in_venv():
env = os.environ.copy()  # HUNTER_API_KEY="from_docker"
env.update(api_keys)     # HUNTER_API_KEY="from_param" (overwrites)
# Result: Tool sees "from_param" (tool parameter takes priority)
```

## Tool-Specific Details

### SpiderFoot
- **Reads from**: `os.environ` (environment variables)
- **Config file**: `/opt/spiderfoot/spiderfoot.cfg` (if mounted)
- **Example**: `os.environ.get('SHODAN_API_KEY')` in SpiderFoot code

### GHunt
- **Reads from**: `os.environ` or `/opt/ghunt/.env` file
- **Variables**: `GOOGLE_API_KEY`, `GOOGLE_CX`
- **Example**: GHunt's code checks `os.environ.get('GOOGLE_API_KEY')`

### theHarvester
- **Reads from**: `os.environ`
- **Variables**: `HUNTER_API_KEY`, `BING_API_KEY`, `SHODAN_API_KEY`, etc.
- **Example**: `os.environ.get('HUNTER_API_KEY')` when using `-b hunter`

### Other Tools
- **Sherlock, Holehe, Maigret, Blackbird**: Don't use API keys (fully free)

## Verification

You can verify the flow by checking environment variables in the container:

```bash
# Check what environment variables are available
docker run --rm -i -e SHODAN_API_KEY="test123" \
  osint-tools-mcp-server:latest \
  python3 -c "import os; print(os.environ.get('SHODAN_API_KEY'))"
# Output: test123
```

## Summary

**The key mechanism**: 
1. Docker environment variables → Python `os.environ`
2. `run_command_in_venv()` copies `os.environ` and passes it to subprocess via `env=env`
3. OSINT tools read API keys from their environment (standard Python/Unix behavior)
4. For theHarvester, tool parameters can also be passed and merged with environment

**No special configuration needed** - it's standard Unix/Python subprocess environment variable inheritance!

