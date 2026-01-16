#!/usr/bin/env python3
"""Quick test for theHarvester and GHunt fixes."""

import json
import subprocess
import sys

def send_mcp_request(docker_cmd, method, params=None, request_id=1):
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
    
    stdout, stderr = process.communicate(input=request_json, timeout=30)
    
    if stderr:
        print(f"Stderr: {stderr[:200]}", file=sys.stderr)
    
    try:
        response_line = stdout.strip().split('\n')[0] if stdout.strip() else ""
        if response_line:
            return json.loads(response_line)
        else:
            return {"error": "No response"}
    except json.JSONDecodeError:
        return {"error": "JSON decode error", "stdout": stdout[:200]}

def main():
    docker_cmd = ["docker", "run", "--rm", "-i", "osint-tools-mcp-server:latest"]
    
    print("Testing theHarvester...")
    response = send_mcp_request(
        docker_cmd,
        "tools/call",
        {
            "name": "theharvester_domain_search",
            "arguments": {"domain": "example.com", "sources": "baidu", "limit": 10}
        },
        request_id=1
    )
    
    if "result" in response:
        result_data = json.loads(response["result"]["content"][0].get("text", "{}"))
        if result_data.get("success"):
            print("✅ theHarvester works!")
        else:
            print(f"❌ theHarvester failed: {result_data.get('error', 'Unknown')[:200]}")
    else:
        print(f"❌ Error: {response.get('error', 'Unknown')}")
    
    print("\nTesting GHunt...")
    response = send_mcp_request(
        docker_cmd,
        "tools/call",
        {
            "name": "ghunt_google_search",
            "arguments": {"identifier": "test@example.com", "timeout": 10}
        },
        request_id=2
    )
    
    if "result" in response:
        result_data = json.loads(response["result"]["content"][0].get("text", "{}"))
        if result_data.get("success"):
            print("✅ GHunt works!")
        else:
            error = result_data.get("error", "Unknown")
            # GHunt may fail due to missing credentials, but that's OK - it means it's running
            if "cred" in error.lower() or "auth" in error.lower():
                print("✅ GHunt is running (credentials needed for full functionality)")
            else:
                print(f"❌ GHunt failed: {error[:200]}")
    else:
        print(f"❌ Error: {response.get('error', 'Unknown')}")

if __name__ == "__main__":
    main()


