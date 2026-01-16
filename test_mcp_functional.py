#!/usr/bin/env python3
"""
Functional test for Docker-based MCP Server
Tests the MCP server by sending JSON-RPC requests via Docker exec
"""

import json
import subprocess
import sys
import time

def send_mcp_request(docker_cmd, method, params=None, request_id=1):
    """Send a JSON-RPC request to the MCP server running in Docker."""
    request = {
        "jsonrpc": "2.0",
        "id": request_id,
        "method": method
    }
    if params:
        request["params"] = params
    
    request_json = json.dumps(request) + "\n"
    
    # Send request via Docker exec
    process = subprocess.Popen(
        docker_cmd,
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True
    )
    
    stdout, stderr = process.communicate(input=request_json, timeout=10)
    
    if stderr:
        print(f"Stderr: {stderr}", file=sys.stderr)
    
    try:
        # Get first line of response
        response_line = stdout.strip().split('\n')[0] if stdout.strip() else ""
        if response_line:
            return json.loads(response_line)
        else:
            return {"error": "No response received", "stdout": stdout, "stderr": stderr}
    except json.JSONDecodeError as e:
        return {"error": f"JSON decode error: {e}", "stdout": stdout, "stderr": stderr}

def test_docker_mcp_server():
    """Test the MCP server running in Docker."""
    print("="*60)
    print("Docker MCP Server Functional Test")
    print("="*60)
    
    # Docker command to run the MCP server
    docker_cmd = [
        "docker", "run", "--rm", "-i",
        "osint-tools-mcp-server:latest"
    ]
    
    tests_passed = 0
    tests_total = 0
    
    # Test 1: Initialize
    print("\n[TEST 1] Testing initialize...")
    tests_total += 1
    response = send_mcp_request(
        docker_cmd,
        "initialize",
        {
            "protocolVersion": "2024-11-05",
            "capabilities": {},
            "clientInfo": {"name": "test-client", "version": "1.0.0"}
        },
        request_id=1
    )
    
    if "result" in response and "serverInfo" in response.get("result", {}):
        server_info = response["result"]["serverInfo"]
        print(f"✅ Initialize passed - Server: {server_info.get('name')} v{server_info.get('version')}")
        tests_passed += 1
    else:
        print(f"❌ Initialize failed - Response: {json.dumps(response, indent=2)}")
    
    # Test 2: List tools
    print("\n[TEST 2] Testing tools/list...")
    tests_total += 1
    response = send_mcp_request(docker_cmd, "tools/list", request_id=2)
    
    if "result" in response and "tools" in response.get("result", {}):
        tools = response["result"]["tools"]
        print(f"✅ Tools list passed - Found {len(tools)} tools:")
        for tool in tools[:3]:  # Show first 3
            print(f"   - {tool['name']}")
        if len(tools) > 3:
            print(f"   ... and {len(tools) - 3} more")
        tests_passed += 1
        
        # Verify all expected tools are present
        expected_tools = [
            "sherlock_username_search",
            "holehe_email_search",
            "spiderfoot_scan",
            "ghunt_google_search",
            "maigret_username_search",
            "theharvester_domain_search",
            "blackbird_username_search"
        ]
        tool_names = [t["name"] for t in tools]
        missing = [t for t in expected_tools if t not in tool_names]
        if missing:
            print(f"⚠️  Missing tools: {missing}")
        else:
            print("✅ All expected tools are present")
    else:
        print(f"❌ Tools list failed - Response: {json.dumps(response, indent=2)}")
    
    # Test 3: Quick tool call test (holehe with test email - fast)
    print("\n[TEST 3] Testing tool call (holehe_email_search)...")
    tests_total += 1
    response = send_mcp_request(
        docker_cmd,
        "tools/call",
        {
            "name": "holehe_email_search",
            "arguments": {
                "email": "test@example.com",
                "only_used": True,
                "timeout": 5
            }
        },
        request_id=3
    )
    
    if "result" in response:
        print("✅ Tool call test passed (server responded)")
        if "content" in response["result"]:
            print("   Response received with content")
        tests_passed += 1
    else:
        print(f"❌ Tool call failed - Response: {json.dumps(response, indent=2)[:500]}")
    
    # Summary
    print("\n" + "="*60)
    print("TEST SUMMARY")
    print("="*60)
    print(f"Tests passed: {tests_passed}/{tests_total}")
    
    if tests_passed == tests_total:
        print("✅ All functional tests passed!")
        return 0
    else:
        print("⚠️  Some tests failed")
        return 1

if __name__ == "__main__":
    sys.exit(test_docker_mcp_server())


