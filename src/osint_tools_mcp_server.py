#!/usr/bin/env python3
"""
OSINT Tools MCP Server
A simple MCP server that exposes OSINT tools through stdio interface.
"""

import asyncio
import json
import subprocess
import tempfile
import os
import sys
from pathlib import Path
from typing import Any, Dict, List, Optional

async def run_command_in_venv(command: List[str], cwd: Optional[str] = None, input_data: Optional[str] = None, extra_env: Optional[Dict[str, str]] = None) -> tuple[str, str, int]:
    """Run a command in the virtual environment.
    
    Args:
        command: Command to run
        cwd: Working directory
        input_data: Input data to send to stdin
        extra_env: Additional environment variables to set
    """
    try:
        # Set up environment - use system Python in container
        env = os.environ.copy()
        if extra_env:
            env.update(extra_env)
        
        process = await asyncio.create_subprocess_exec(
            *command,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE,
            cwd=cwd,
            env=env,
            stdin=asyncio.subprocess.PIPE if input_data else None
        )
        
        stdout, stderr = await process.communicate(input=input_data.encode() if input_data else None)
        
        return stdout.decode('utf-8', errors='ignore'), stderr.decode('utf-8', errors='ignore'), process.returncode
        
    except Exception as e:
        return "", str(e), 1

async def handle_sherlock(params: Dict[str, Any]) -> Dict[str, Any]:
    """Handle Sherlock username search."""
    username = params["username"]
    timeout = params.get("timeout", 10000)
    sites = params.get("sites", [])
    output_format = params.get("output_format", "csv")
    
    cmd = ["sherlock", username, f"--timeout", str(timeout)]
    
    if sites:
        for site in sites:
            cmd.extend(["--site", site])
            
    if output_format == "csv":
        cmd.append("--csv")
    elif output_format == "xlsx":
        cmd.append("--xlsx")
        
    # Create temporary directory for output
    with tempfile.TemporaryDirectory() as temp_dir:
        cmd.extend(["--folderoutput", temp_dir])
        
        stdout, stderr, returncode = await run_command_in_venv(cmd)
        
        if returncode == 0:
            # Read output files
            output_files = list(Path(temp_dir).glob(f"{username}.*"))
            results = {"stdout": stdout, "files": []}
            
            for file_path in output_files:
                try:
                    content = file_path.read_text(encoding='utf-8')
                    results["files"].append({
                        "filename": file_path.name,
                        "content": content
                    })
                except Exception as e:
                    print(f"Could not read file {file_path}: {e}", file=sys.stderr)
            
            return {"success": True, "content": results}
        else:
            return {"success": False, "error": f"Sherlock failed: {stderr}"}

async def handle_holehe(params: Dict[str, Any]) -> Dict[str, Any]:
    """Handle Holehe email search."""
    email = params["email"]
    only_used = params.get("only_used", True)
    timeout = params.get("timeout", 10000)
    
    cmd = ["holehe", email, "--timeout", str(timeout)]
    if only_used:
        cmd.append("--only-used")
    
    stdout, stderr, returncode = await run_command_in_venv(cmd)
    
    if returncode == 0:
        return {"success": True, "content": stdout}
    else:
        return {"success": False, "error": f"Holehe failed: {stderr}"}

async def handle_spiderfoot(params: Dict[str, Any]) -> Dict[str, Any]:
    """Handle SpiderFoot comprehensive OSINT scan."""
    target = params["target"]
    
    # SpiderFoot reads API keys from environment variables or config file
    # Common API keys: SHODAN_API_KEY, VIRUSTOTAL_API_KEY, etc.
    # These are automatically picked up from os.environ by run_command_in_venv
    
    cmd = ["python3", "/opt/spiderfoot/sf.py", 
           "-s", target,
           "-u", "all",      # Use all modules (gracefully skips those needing APIs if not configured)
           "-o", "json",     # JSON output
           "-q"]             # Quiet mode
    
    stdout, stderr, returncode = await run_command_in_venv(cmd)
    
    if returncode == 0:
        return {"success": True, "content": stdout}
    else:
        return {"success": False, "error": f"SpiderFoot failed: {stderr}"}

async def handle_ghunt(params: Dict[str, Any]) -> Dict[str, Any]:
    """Handle GHunt Google account search."""
    identifier = params["identifier"]
    timeout = params.get("timeout", 10000)
    
    # GHunt needs PYTHONPATH to include /opt/ghunt so it can import the ghunt module
    # We'll set PYTHONPATH and run from the ghunt directory
    cwd = "/opt/ghunt"
    
    # Set PYTHONPATH to include /opt/ghunt so the ghunt module can be imported
    # Also add /opt/ghunt to sys.path via Python code
    extra_env = {"PYTHONPATH": "/opt/ghunt"}
    
    # Method 1: Try main.py with PYTHONPATH set (this is the entry point)
    if os.path.exists("/opt/ghunt/main.py"):
        # main.py tries to import from ghunt, so we need PYTHONPATH
        cmd = ["python3", "/opt/ghunt/main.py", "email", identifier]
    # Method 2: Try ghunt.py if it exists
    elif os.path.exists("/opt/ghunt/ghunt.py"):
        cmd = ["python3", "/opt/ghunt/ghunt.py", "email", identifier]
    # Method 3: Try running the ghunt module directly with PYTHONPATH
    else:
        # Try to run ghunt as a module, but we need to ensure PYTHONPATH is set
        cmd = ["python3", "-c", 
               "import sys; sys.path.insert(0, '/opt/ghunt'); from ghunt import ghunt; ghunt.main()",
               "email", identifier]
    
    stdout, stderr, returncode = await run_command_in_venv(
        cmd, 
        cwd=cwd if os.path.exists(cwd) else None,
        extra_env=extra_env
    )
    
    if returncode == 0:
        return {"success": True, "content": stdout}
    else:
        return {"success": False, "error": f"GHunt failed: {stderr}"}

async def handle_maigret(params: Dict[str, Any]) -> Dict[str, Any]:
    """Handle Maigret username search."""
    username = params["username"]
    timeout = params.get("timeout", 10000)
    
    # Create temporary directory for output
    with tempfile.TemporaryDirectory() as temp_dir:
        # Maigret -J requires output type: "simple" or "ndjson" (not "json")
        # --folderoutput specifies where to save results
        cmd = ["maigret", username, "--timeout", str(timeout), "-J", "ndjson", "--folderoutput", temp_dir]
        
        stdout, stderr, returncode = await run_command_in_venv(cmd)
        
        if returncode == 0:
            # Try to find and read JSON output file
            json_files = list(Path(temp_dir).glob("*.json"))
            if json_files:
                try:
                    # Read the first JSON file found
                    json_content = json_files[0].read_text(encoding='utf-8')
                    return {"success": True, "content": json_content}
                except Exception as e:
                    # Fallback to stdout if JSON file read fails
                    return {"success": True, "content": stdout}
            else:
                # No JSON file found, return stdout (may contain text output)
                return {"success": True, "content": stdout}
        else:
            return {"success": False, "error": f"Maigret failed: {stderr}"}

async def handle_theharvester(params: Dict[str, Any]) -> Dict[str, Any]:
    """Handle theHarvester domain/email enumeration."""
    domain = params["domain"]
    sources = params.get("sources", "all")
    limit = params.get("limit", 500)
    
    # API keys can be passed via environment variables or tool parameters
    # Priority: tool parameter > environment variable
    api_keys = {}
    if "hunter_api_key" in params:
        api_keys["HUNTER_API_KEY"] = params["hunter_api_key"]
    if "bing_api_key" in params:
        api_keys["BING_API_KEY"] = params["bing_api_key"]
    if "shodan_api_key" in params:
        api_keys["SHODAN_API_KEY"] = params["shodan_api_key"]
    if "securitytrails_api_key" in params:
        api_keys["SECURITYTRAILS_API_KEY"] = params["securitytrails_api_key"]
    
    # theHarvester - use source version at /opt/theharvester (patched to handle aiosqli)
    import sys
    
    # Set up environment with API keys
    env = api_keys.copy() if api_keys else {}
    
    # Use source version - should be patched during Docker build
    script_path = "/opt/theharvester/theHarvester.py"
    if os.path.exists(script_path):
        cmd = ["python3", script_path, "-d", domain, "-b", sources, "-l", str(limit)]
        stdout, stderr, returncode = await run_command_in_venv(cmd, extra_env=env, cwd="/opt/theharvester")
        
        if returncode == 0:
            return {"success": True, "content": stdout}
        else:
            return {"success": False, "error": f"theHarvester failed: {stderr}"}
    else:
        return {"success": False, "error": "theHarvester script not found at /opt/theharvester/theHarvester.py"}
        
        # Build comprehensive PYTHONPATH
        site_packages = site.getsitepackages()
        pythonpath_parts = []
        
        # Add all site-packages
        for sp in site_packages:
            if sp and os.path.exists(sp):
                pythonpath_parts.append(sp)
        
        # Add script's parent directory (package location)
        script_parent = os.path.dirname(os.path.dirname(script_path))
        if script_parent and os.path.exists(script_parent):
            pythonpath_parts.append(script_parent)
        
        # Add current sys.path entries that exist
        for p in sys.path:
            if p and os.path.exists(p) and p not in pythonpath_parts:
                pythonpath_parts.append(p)
        
        final_pythonpath = ':'.join(pythonpath_parts)
        
        # Build environment - start with current environment and add our settings
        env = {}
        # Copy all current environment variables
        for key, value in os.environ.items():
            env[key] = value
        # Add API keys
        if api_keys:
            env.update(api_keys)
        # Set PYTHONPATH - this is critical
        env['PYTHONPATH'] = final_pythonpath
        
        # Use shell command with explicit PYTHONPATH - escape properly
        import shlex
        safe_pythonpath = final_pythonpath.replace("'", "'\"'\"'")
        exports = [f"export PYTHONPATH='{safe_pythonpath}'"]
        
        if api_keys:
            for k, v in api_keys.items():
                safe_v = str(v).replace("'", "'\"'\"'")
                exports.append(f"export {k}='{safe_v}'")
        
        # Build shell command
        export_cmd = ' && '.join(exports)
        script_cmd = f"python3 {shlex.quote(script_path)} -d {shlex.quote(domain)} -b {shlex.quote(sources)} -l {shlex.quote(str(limit))}"
        shell_cmd = f"{export_cmd} && {script_cmd}"
        
        cmd = ["/bin/sh", "-c", shell_cmd]
        stdout, stderr, returncode = await run_command_in_venv(cmd)
        
        if returncode == 0:
            return {"success": True, "content": stdout}
        else:
            return {"success": False, "error": f"theHarvester failed: {stderr}"}
    
    # Fallback: try direct import and execution
    try:
        import theharvester
        from theharvester.theHarvester import main as harvester_main
        import sys
        
        # Apply API keys to environment FIRST (theHarvester reads from os.environ)
        if api_keys:
            for key, value in api_keys.items():
                os.environ[key] = value
        
        # Save original argv
        original_argv = sys.argv.copy()
        
        # Set up arguments for theHarvester
        sys.argv = ['theHarvester', '-d', domain, '-b', sources, '-l', str(limit)]
        
        # Capture stdout/stderr
        from io import StringIO
        old_stdout = sys.stdout
        old_stderr = sys.stderr
        sys.stdout = StringIO()
        sys.stderr = StringIO()
        
        try:
            # Run theHarvester main function
            harvester_main()
            stdout = sys.stdout.getvalue()
            stderr = sys.stderr.getvalue()
            returncode = 0
        except SystemExit as e:
            # theHarvester uses sys.exit(), catch it
            stdout = sys.stdout.getvalue()
            stderr = sys.stderr.getvalue()
            returncode = e.code if isinstance(e.code, int) else 0
        except Exception as e:
            stdout = sys.stdout.getvalue()
            stderr = sys.stderr.getvalue() + f"\nException: {str(e)}"
            returncode = 1
        finally:
            # Restore stdout/stderr and argv
            sys.stdout = old_stdout
            sys.stderr = old_stderr
            sys.argv = original_argv
        
        if returncode == 0:
            return {"success": True, "content": stdout}
        else:
            return {"success": False, "error": f"theHarvester failed: {stderr}"}
            
    except ImportError as e:
        # Can't import, fallback to subprocess with full environment setup
        import site
        import sys
        
        # Get site-packages
        site_packages = site.getsitepackages()
        pythonpath = ':'.join(site_packages) if site_packages else ''
        
        # Also add current sys.path entries
        all_paths = [p for p in sys.path if p and os.path.exists(p)]
        if pythonpath:
            all_paths.insert(0, pythonpath)
        final_pythonpath = ':'.join(all_paths)
        
        env = api_keys.copy() if api_keys else {}
        env['PYTHONPATH'] = final_pythonpath
        
        # Try module execution
        cmd = [sys.executable, "-m", "theharvester", "-d", domain, "-b", sources, "-l", str(limit)]
        stdout, stderr, returncode = await run_command_in_venv(cmd, extra_env=env)
        
        if returncode == 0:
            return {"success": True, "content": stdout}
        else:
            return {"success": False, "error": f"theHarvester failed (ImportError): {stderr}"}
    except Exception as e:
        # Any other error - log it and try subprocess
        error_msg = str(e)
        import site
        import sys
        
        # Get site-packages for subprocess
        site_packages = site.getsitepackages()
        pythonpath = ':'.join(site_packages) if site_packages else ''
        
        all_paths = [p for p in sys.path if p and os.path.exists(p)]
        if pythonpath:
            all_paths.insert(0, pythonpath)
        final_pythonpath = ':'.join(all_paths)
        
        env = api_keys.copy() if api_keys else {}
        env['PYTHONPATH'] = final_pythonpath
        
        cmd = [sys.executable, "-m", "theharvester", "-d", domain, "-b", sources, "-l", str(limit)]
        stdout, stderr, returncode = await run_command_in_venv(cmd, extra_env=env)
        
        if returncode == 0:
            return {"success": True, "content": stdout}
        else:
            return {"success": False, "error": f"theHarvester failed (Exception: {error_msg}): {stderr}"}
        

async def handle_blackbird(params: Dict[str, Any]) -> Dict[str, Any]:
    """Handle Blackbird username search."""
    username = params["username"]
    timeout = params.get("timeout", 10000)
    
    # Blackbird needs a data directory, create it if it doesn't exist
    data_dir = "/app/data"
    os.makedirs(data_dir, exist_ok=True)
    
    # Set environment variable for data path
    extra_env = {
        "BLACKBIRD_DATA_DIR": data_dir,
        "USERNAME_LIST_PATH": os.path.join(data_dir, "wmn-data.json")
    }
    
    # Try to initialize data file if it doesn't exist
    data_file = extra_env["USERNAME_LIST_PATH"]
    if not os.path.exists(data_file):
        # Create empty JSON file as placeholder
        Path(data_file).parent.mkdir(parents=True, exist_ok=True)
        Path(data_file).write_text("{}")
    
    cmd = ["python3", "/opt/blackbird/blackbird.py", "-u", username, "--timeout", str(timeout)]
    
    stdout, stderr, returncode = await run_command_in_venv(cmd, extra_env=extra_env, cwd="/opt/blackbird")
    
    if returncode == 0:
        return {"success": True, "content": stdout}
    else:
        return {"success": False, "error": f"Blackbird failed: {stderr}"}

async def handle_tool_call(tool_name: str, params: Dict[str, Any]) -> Dict[str, Any]:
    """Handle tool calls by routing to appropriate handlers."""
    try:
        if tool_name == "sherlock_username_search":
            return await handle_sherlock(params)
        elif tool_name == "holehe_email_search":
            return await handle_holehe(params)
        elif tool_name == "spiderfoot_scan":
            return await handle_spiderfoot(params)
        elif tool_name == "ghunt_google_search":
            return await handle_ghunt(params)
        elif tool_name == "maigret_username_search":
            return await handle_maigret(params)
        elif tool_name == "theharvester_domain_search":
            return await handle_theharvester(params)
        elif tool_name == "blackbird_username_search":
            return await handle_blackbird(params)
        else:
            return {"success": False, "error": f"Unknown tool: {tool_name}"}
    except Exception as e:
        return {"success": False, "error": f"Tool execution failed: {str(e)}"}

async def main():
    """Main MCP server loop - handles JSON-RPC over stdio."""
    try:
        # Read from stdin and write to stdout
        while True:
            try:
                line = await asyncio.get_event_loop().run_in_executor(None, sys.stdin.readline)
                if not line:
                    break
                
                # Parse JSON-RPC request
                request = json.loads(line.strip())
                
                # Extract method and params
                method = request.get("method")
                params = request.get("params", {})
                request_id = request.get("id")
                
                # Handle different MCP methods
                if method == "initialize":
                    response = {
                        "jsonrpc": "2.0",
                        "id": request_id,
                        "result": {
                            "protocolVersion": "2024-11-05",
                            "capabilities": {
                                "tools": {}
                            },
                            "serverInfo": {
                                "name": "osint-tools-mcp-server",
                                "version": "1.0.0"
                            }
                        }
                    }
                elif method == "tools/list":
                    tools = [
                        {
                            "name": "sherlock_username_search",
                            "description": "Search for username across 399+ social media platforms and websites",
                            "inputSchema": {
                                "type": "object",
                                "properties": {
                                    "username": {"type": "string", "description": "Username to search for"},
                                    "timeout": {"type": "integer", "description": "Timeout in seconds (default: 10000)"},
                                    "sites": {"type": "array", "items": {"type": "string"}, "description": "Specific sites to search"},
                                    "output_format": {"type": "string", "enum": ["txt", "csv", "xlsx"], "description": "Output format"}
                                },
                                "required": ["username"]
                            }
                        },
                        {
                            "name": "holehe_email_search", 
                            "description": "Check if email is registered on 120+ platforms",
                            "inputSchema": {
                                "type": "object",
                                "properties": {
                                    "email": {"type": "string", "description": "Email address to investigate"},
                                    "only_used": {"type": "boolean", "description": "Show only registered accounts (default: true)"},
                                    "timeout": {"type": "integer", "description": "Request timeout in seconds (default: 10000)"}
                                },
                                "required": ["email"]
                            }
                        },
                        {
                            "name": "spiderfoot_scan",
                            "description": "Comprehensive OSINT scan - auto-detects target type (IP, IPv6, domain, email, phone, username, person name, Bitcoin address, network block, BGP AS). API keys can be provided via environment variables (SHODAN_API_KEY, VIRUSTOTAL_API_KEY, etc.) for enhanced modules.",
                            "inputSchema": {
                                "type": "object",
                                "properties": {
                                    "target": {
                                        "type": "string", 
                                        "description": "Target to scan - SpiderFoot auto-detects type from: IP address, IPv6 address, domain, email, phone number, username, person name, Bitcoin address, network block, or BGP AS"
                                    }
                                },
                                "required": ["target"]
                            }
                        },
                        {
                            "name": "ghunt_google_search",
                            "description": "Search for Google account information using email address or Google ID. API keys can be provided via environment variables (GOOGLE_API_KEY, GOOGLE_CX) for enhanced searches.",
                            "inputSchema": {
                                "type": "object",
                                "properties": {
                                    "identifier": {"type": "string", "description": "Email address or Google ID to search"},
                                    "timeout": {"type": "integer", "description": "Timeout in seconds (default: 10000)"}
                                },
                                "required": ["identifier"]
                            }
                        },
                        {
                            "name": "maigret_username_search",
                            "description": "Search for username across 3000+ sites with detailed analysis and false positive detection",
                            "inputSchema": {
                                "type": "object",
                                "properties": {
                                    "username": {"type": "string", "description": "Username to search for"},
                                    "timeout": {"type": "integer", "description": "Timeout in seconds (default: 10000)"}
                                },
                                "required": ["username"]
                            }
                        },
                        {
                            "name": "theharvester_domain_search",
                            "description": "Gather emails, subdomains, hosts, employee names, open ports and banners from public sources. API keys can be provided via environment variables or optional parameters for enhanced sources (hunter, bingapi, shodan, securityTrails).",
                            "inputSchema": {
                                "type": "object",
                                "properties": {
                                    "domain": {"type": "string", "description": "Domain/company name to search"},
                                    "sources": {"type": "string", "description": "Data sources (default: all). Options: baidu, bing, bingapi, certspotter, crtsh, dnsdumpster, duckduckgo, github-code, google, hackertarget, hunter, linkedin, linkedin_links, otx, pentesttools, projectdiscovery, qwant, rapiddns, securityTrails, sublist3r, threatcrowd, threatminer, trello, twitter, urlscan, virustotal, yahoo"},
                                    "limit": {"type": "integer", "description": "Limit results (default: 500)"},
                                    "hunter_api_key": {"type": "string", "description": "Optional: Hunter.io API key for enhanced email discovery"},
                                    "bing_api_key": {"type": "string", "description": "Optional: Bing API key for bingapi source"},
                                    "shodan_api_key": {"type": "string", "description": "Optional: Shodan API key for shodan source"},
                                    "securitytrails_api_key": {"type": "string", "description": "Optional: SecurityTrails API key for securityTrails source"}
                                },
                                "required": ["domain"]
                            }
                        },
                        {
                            "name": "blackbird_username_search",
                            "description": "Fast OSINT tool to search for accounts by username across 581 sites",
                            "inputSchema": {
                                "type": "object",
                                "properties": {
                                    "username": {"type": "string", "description": "Username to search for"},
                                    "timeout": {"type": "integer", "description": "Timeout in seconds (default: 10000)"}
                                },
                                "required": ["username"]
                            }
                        }
                    ]
                    response = {
                        "jsonrpc": "2.0",
                        "id": request_id,
                        "result": {"tools": tools}
                    }
                elif method == "tools/call":
                    tool_name = params.get("name")
                    tool_params = params.get("arguments", {})
                    
                    result = await handle_tool_call(tool_name, tool_params)
                    
                    response = {
                        "jsonrpc": "2.0",
                        "id": request_id,
                        "result": {
                            "content": [
                                {
                                    "type": "text",
                                    "text": json.dumps(result, indent=2)
                                }
                            ]
                        }
                    }
                else:
                    response = {
                        "jsonrpc": "2.0",
                        "id": request_id,
                        "error": {
                            "code": -32601,
                            "message": f"Method not found: {method}"
                        }
                    }
                
                # Send response
                print(json.dumps(response), flush=True)
                
            except json.JSONDecodeError as e:
                error_response = {
                    "jsonrpc": "2.0",
                    "id": None,
                    "error": {
                        "code": -32700,
                        "message": f"Parse error: {str(e)}"
                    }
                }
                print(json.dumps(error_response), flush=True)
            except Exception as e:
                error_response = {
                    "jsonrpc": "2.0", 
                    "id": request.get("id") if 'request' in locals() else None,
                    "error": {
                        "code": -32603,
                        "message": f"Internal error: {str(e)}"
                    }
                }
                print(json.dumps(error_response), flush=True)
                
    except KeyboardInterrupt:
        pass
    except Exception as e:
        print(f"Server error: {e}", file=sys.stderr)

if __name__ == "__main__":
    asyncio.run(main())