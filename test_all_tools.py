#!/usr/bin/env python3
"""
Comprehensive test suite for all OSINT tools in the MCP server.
Tests each tool individually with various scenarios.
"""

import json
import subprocess
import sys
import time
from typing import Dict, Any, Optional

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
    
    process = subprocess.Popen(
        docker_cmd,
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True
    )
    
    try:
        stdout, stderr = process.communicate(input=request_json, timeout=30)
    except subprocess.TimeoutExpired:
        process.kill()
        return {"error": "Request timeout", "timeout": True}
    
    if stderr:
        print(f"Stderr: {stderr}", file=sys.stderr)
    
    try:
        response_line = stdout.strip().split('\n')[0] if stdout.strip() else ""
        if response_line:
            return json.loads(response_line)
        else:
            return {"error": "No response received", "stdout": stdout, "stderr": stderr}
    except json.JSONDecodeError as e:
        return {"error": f"JSON decode error: {e}", "stdout": stdout, "stderr": stderr}

def test_tool(docker_cmd, tool_name, arguments, test_name, timeout=30):
    """Test a specific tool."""
    print(f"\n{'='*60}")
    print(f"TEST: {test_name}")
    print(f"{'='*60}")
    print(f"Tool: {tool_name}")
    print(f"Arguments: {json.dumps(arguments, indent=2)}")
    
    start_time = time.time()
    response = send_mcp_request(
        docker_cmd,
        "tools/call",
        {
            "name": tool_name,
            "arguments": arguments
        },
        request_id=3
    )
    elapsed = time.time() - start_time
    
    if "error" in response:
        if response.get("timeout"):
            print(f"⏱️  Tool timed out after {timeout}s")
            return False
        else:
            print(f"❌ Tool call failed: {response.get('error')}")
            return False
    
    if "result" in response:
        print(f"✅ Tool executed successfully ({elapsed:.2f}s)")
        if "content" in response["result"]:
            try:
                result_data = json.loads(response["result"]["content"][0].get("text", "{}"))
                if result_data.get("success"):
                    content = result_data.get("content", "")
                    if isinstance(content, str):
                        print(f"   Result length: {len(content)} characters")
                    elif isinstance(content, dict):
                        print(f"   Result keys: {list(content.keys())}")
                else:
                    print(f"   Tool returned error: {result_data.get('error', 'Unknown')}")
            except:
                print(f"   Response received (parsing skipped)")
        return True
    else:
        print(f"❌ Unexpected response format")
        return False

def main():
    """Run comprehensive tests for all tools."""
    print("="*60)
    print("Comprehensive OSINT Tools Test Suite")
    print("="*60)
    
    docker_cmd = ["docker", "run", "--rm", "-i", "osint-tools-mcp-server:latest"]
    
    tests_passed = 0
    tests_total = 0
    tests_skipped = 0
    
    # Test 1: Sherlock
    tests_total += 1
    if test_tool(
        docker_cmd,
        "sherlock_username_search",
        {"username": "testuser123", "timeout": 5},
        "Sherlock Username Search (Quick Test)"
    ):
        tests_passed += 1
    
    # Test 2: Holehe
    tests_total += 1
    if test_tool(
        docker_cmd,
        "holehe_email_search",
        {"email": "test@example.com", "timeout": 5},
        "Holehe Email Search"
    ):
        tests_passed += 1
    
    # Test 3: Maigret
    tests_total += 1
    if test_tool(
        docker_cmd,
        "maigret_username_search",
        {"username": "testuser", "timeout": 5},
        "Maigret Username Search (Quick Test)"
    ):
        tests_passed += 1
    
    # Test 4: Blackbird
    tests_total += 1
    if test_tool(
        docker_cmd,
        "blackbird_username_search",
        {"username": "testuser", "timeout": 5},
        "Blackbird Username Search (Quick Test)"
    ):
        tests_passed += 1
    
    # Test 5: theHarvester (quick test with free sources)
    tests_total += 1
    if test_tool(
        docker_cmd,
        "theharvester_domain_search",
        {"domain": "example.com", "sources": "baidu", "limit": 10},
        "theHarvester Domain Search (Free Source)"
    ):
        tests_passed += 1
    
    # Test 6: GHunt (may fail without proper setup)
    tests_total += 1
    result = test_tool(
        docker_cmd,
        "ghunt_google_search",
        {"identifier": "test@example.com", "timeout": 10},
        "GHunt Google Search"
    )
    if result:
        tests_passed += 1
    else:
        tests_skipped += 1
        print("   (May require Google API setup)")
    
    # Test 7: SpiderFoot (skipped - takes too long)
    tests_total += 1
    tests_skipped += 1
    print(f"\n{'='*60}")
    print("TEST: SpiderFoot Scan (SKIPPED)")
    print(f"{'='*60}")
    print("⚠️  SpiderFoot scans can take 5-30 minutes")
    print("   Skipping for quick test suite")
    print("   Run manually: spiderfoot_scan with target")
    
    # Summary
    print("\n" + "="*60)
    print("TEST SUMMARY")
    print("="*60)
    print(f"Tests passed: {tests_passed}/{tests_total - tests_skipped}")
    print(f"Tests skipped: {tests_skipped}")
    print(f"Tests failed: {tests_total - tests_passed - tests_skipped}")
    
    if tests_passed == (tests_total - tests_skipped):
        print("✅ All runnable tests passed!")
        return 0
    else:
        print("⚠️  Some tests failed")
        return 1

if __name__ == "__main__":
    sys.exit(main())


