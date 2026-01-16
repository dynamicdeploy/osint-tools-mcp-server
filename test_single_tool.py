#!/usr/bin/env python3
"""Test a single OSINT tool at a time."""

import json
import subprocess
import sys
import time

def send_mcp_request(docker_cmd, method, params=None, request_id=1, timeout=60):
    """Send a JSON-RPC request to the MCP server."""
    request = {
        "jsonrpc": "2.0",
        "id": request_id,
        "method": method
    }
    if params:
        request["params"] = params
    
    request_json = json.dumps(request) + "\n"
    
    process = subprocess.Popen(
        docker_cmd,
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True
    )
    
    try:
        stdout, stderr = process.communicate(input=request_json, timeout=timeout)
    except subprocess.TimeoutExpired:
        process.kill()
        return {"error": "Request timeout", "timeout": True}
    
    if stderr:
        print(f"Stderr: {stderr[:300]}", file=sys.stderr)
    
    try:
        response_line = stdout.strip().split('\n')[0] if stdout.strip() else ""
        if response_line:
            return json.loads(response_line)
        else:
            return {"error": "No response received", "stdout": stdout[:200], "stderr": stderr[:200]}
    except json.JSONDecodeError as e:
        return {"error": f"JSON decode error: {e}", "stdout": stdout[:200], "stderr": stderr[:200]}

def test_tool(tool_name, arguments, test_name):
    """Test a specific tool."""
    print(f"\n{'='*70}")
    print(f"Testing: {test_name}")
    print(f"{'='*70}")
    print(f"Tool: {tool_name}")
    print(f"Arguments: {json.dumps(arguments, indent=2)}")
    print()
    
    docker_cmd = ["docker", "run", "--rm", "-i", "osint-tools-mcp-server:latest"]
    
    start_time = time.time()
    response = send_mcp_request(
        docker_cmd,
        "tools/call",
        {
            "name": tool_name,
            "arguments": arguments
        },
        request_id=1,
        timeout=120
    )
    elapsed = time.time() - start_time
    
    print(f"Response time: {elapsed:.2f}s")
    print()
    
    if "error" in response:
        if response.get("timeout"):
            print(f"❌ TIMEOUT after 120s")
            return False
        else:
            print(f"❌ Request failed: {response.get('error')}")
            return False
    
    if "result" in response:
        print("✅ Tool call successful")
        if "content" in response["result"]:
            try:
                result_data = json.loads(response["result"]["content"][0].get("text", "{}"))
                if result_data.get("success"):
                    print("✅ Tool execution successful")
                    content = result_data.get("content", "")
                    if isinstance(content, str):
                        print(f"   Result length: {len(content)} characters")
                        if len(content) > 0:
                            preview = content[:300].replace('\n', ' ')
                            print(f"   Preview: {preview}...")
                    elif isinstance(content, dict):
                        print(f"   Result keys: {list(content.keys())}")
                else:
                    error = result_data.get("error", "Unknown")
                    print(f"❌ Tool returned error: {error[:500]}")
                    return False
            except Exception as e:
                print(f"⚠️  Response received but parsing failed: {e}")
                print(f"   Raw response: {str(response['result'])[:300]}")
        return True
    else:
        print(f"❌ Unexpected response format")
        print(f"   Response: {json.dumps(response, indent=2)[:500]}")
        return False

def main():
    if len(sys.argv) < 2:
        print("Usage: python3 test_single_tool.py <tool_name>")
        print("\nAvailable tools:")
        print("  1. sherlock")
        print("  2. holehe")
        print("  3. maigret")
        print("  4. blackbird")
        print("  5. theharvester")
        print("  6. ghunt")
        print("  7. spiderfoot")
        sys.exit(1)
    
    tool = sys.argv[1].lower()
    
    # Test identities
    username = "philsdetection"
    email1 = "philsdetective@yahoo.com"
    email2 = "phillip.morris@gmail.com"
    domain = "yahoo.com"
    
    if tool == "sherlock":
        test_tool(
            "sherlock_username_search",
            {"username": username, "timeout": 30},
            "Sherlock Username Search"
        )
    elif tool == "holehe":
        test_tool(
            "holehe_email_search",
            {"email": email1, "timeout": 30},
            "Holehe Email Search"
        )
    elif tool == "maigret":
        test_tool(
            "maigret_username_search",
            {"username": username, "timeout": 30},
            "Maigret Username Search"
        )
    elif tool == "blackbird":
        test_tool(
            "blackbird_username_search",
            {"username": username, "timeout": 30},
            "Blackbird Username Search"
        )
    elif tool == "theharvester":
        test_tool(
            "theharvester_domain_search",
            {"domain": domain, "sources": "baidu", "limit": 10},
            "theHarvester Domain Search"
        )
    elif tool == "ghunt":
        test_tool(
            "ghunt_google_search",
            {"identifier": email2, "timeout": 30},
            "GHunt Google Search"
        )
    elif tool == "spiderfoot":
        test_tool(
            "spiderfoot_scan",
            {"target": domain, "modules": "sfp_dnsresolve", "timeout": 60},
            "SpiderFoot Scan"
        )
    else:
        print(f"Unknown tool: {tool}")
        sys.exit(1)

if __name__ == "__main__":
    main()


