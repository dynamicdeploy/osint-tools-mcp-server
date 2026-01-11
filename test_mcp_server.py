#!/usr/bin/env python3
"""
Test script for OSINT Tools MCP Server
Tests the MCP server by sending JSON-RPC requests and verifying responses.
"""

import json
import subprocess
import sys
import time
from typing import Dict, Any, Optional

def send_request(process, method: str, params: Optional[Dict[str, Any]] = None, request_id: int = 1) -> Dict[str, Any]:
    """Send a JSON-RPC request to the MCP server."""
    request = {
        "jsonrpc": "2.0",
        "id": request_id,
        "method": method
    }
    if params:
        request["params"] = params
    
    request_json = json.dumps(request) + "\n"
    print(f"→ Sending: {request_json.strip()}", file=sys.stderr)
    
    process.stdin.write(request_json.encode())
    process.stdin.flush()
    
    # Read response
    response_line = process.stdout.readline()
    if not response_line:
        return {"error": "No response received"}
    
    response = json.loads(response_line.decode())
    print(f"← Received: {json.dumps(response, indent=2)}", file=sys.stderr)
    return response

def test_initialize(process) -> bool:
    """Test the initialize method."""
    print("\n" + "="*60)
    print("TEST 1: Initialize")
    print("="*60)
    
    response = send_request(process, "initialize", {
        "protocolVersion": "2024-11-05",
        "capabilities": {},
        "clientInfo": {
            "name": "test-client",
            "version": "1.0.0"
        }
    })
    
    if "result" in response and "serverInfo" in response["result"]:
        print("✅ Initialize test passed")
        print(f"   Server: {response['result']['serverInfo']['name']} v{response['result']['serverInfo']['version']}")
        return True
    else:
        print("❌ Initialize test failed")
        print(f"   Response: {response}")
        return False

def test_tools_list(process) -> bool:
    """Test the tools/list method."""
    print("\n" + "="*60)
    print("TEST 2: List Tools")
    print("="*60)
    
    response = send_request(process, "tools/list", request_id=2)
    
    if "result" in response and "tools" in response["result"]:
        tools = response["result"]["tools"]
        print(f"✅ Tools list test passed - Found {len(tools)} tools:")
        for tool in tools:
            print(f"   - {tool['name']}: {tool['description'][:60]}...")
        return True
    else:
        print("❌ Tools list test failed")
        print(f"   Response: {response}")
        return False

def test_tool_call(process, tool_name: str, arguments: Dict[str, Any], test_name: str) -> bool:
    """Test calling a specific tool."""
    print("\n" + "="*60)
    print(f"TEST: {test_name}")
    print("="*60)
    print(f"Tool: {tool_name}")
    print(f"Arguments: {arguments}")
    
    response = send_request(process, "tools/call", {
        "name": tool_name,
        "arguments": arguments
    }, request_id=3)
    
    if "result" in response:
        print("✅ Tool call test passed")
        # Print a preview of the result
        if "content" in response["result"] and len(response["result"]["content"]) > 0:
            content = response["result"]["content"][0].get("text", "")
            try:
                result_data = json.loads(content)
                if result_data.get("success"):
                    print(f"   Result: Success - {len(str(result_data.get('content', '')))} characters")
                else:
                    print(f"   Result: Failed - {result_data.get('error', 'Unknown error')}")
            except:
                print(f"   Result preview: {content[:200]}...")
        return True
    else:
        print("❌ Tool call test failed")
        if "error" in response:
            print(f"   Error: {response['error']}")
        return False

def main():
    """Run all tests."""
    print("Starting MCP Server Tests")
    print("="*60)
    
    # Start the MCP server process
    print("\nStarting MCP server...")
    process = subprocess.Popen(
        [sys.executable, "src/osint_tools_mcp_server.py"],
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        bufsize=0
    )
    
    try:
        # Give the server a moment to start
        time.sleep(0.5)
        
        # Run tests
        tests_passed = 0
        tests_total = 0
        
        # Test 1: Initialize
        tests_total += 1
        if test_initialize(process):
            tests_passed += 1
        
        # Test 2: List tools
        tests_total += 1
        if test_tools_list(process):
            tests_passed += 1
        
        # Test 3: Quick tool test (using holehe with a test email)
        # Note: This will likely fail if the email doesn't exist, but we're testing the server response
        tests_total += 1
        if test_tool_call(
            process,
            "holehe_email_search",
            {"email": "test@example.com", "only_used": True, "timeout": 5},
            "Holehe Email Search (Quick Test)"
        ):
            tests_passed += 1
        
        # Summary
        print("\n" + "="*60)
        print("TEST SUMMARY")
        print("="*60)
        print(f"Tests passed: {tests_passed}/{tests_total}")
        
        if tests_passed == tests_total:
            print("✅ All tests passed!")
            return 0
        else:
            print("⚠️  Some tests failed")
            return 1
            
    except Exception as e:
        print(f"\n❌ Test error: {e}", file=sys.stderr)
        return 1
    finally:
        # Clean up
        process.terminate()
        try:
            process.wait(timeout=5)
        except subprocess.TimeoutExpired:
            process.kill()
        
        # Print any stderr output
        stderr_output = process.stderr.read().decode()
        if stderr_output:
            print("\nServer stderr:", file=sys.stderr)
            print(stderr_output, file=sys.stderr)

if __name__ == "__main__":
    sys.exit(main())

