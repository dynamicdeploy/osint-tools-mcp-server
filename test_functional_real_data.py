#!/usr/bin/env python3
"""
Functional Tests with Real Data
Tests all OSINT tools with provided identities:
- Handle: philsdetection
- Email 1: philsdetective@yahoo.com
- Email 2: phillip.morris@gmail.com
"""

import json
import subprocess
import sys
import time
from typing import Dict, Any, Optional

def send_mcp_request(docker_cmd, method, params=None, request_id=1, timeout=120):
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
        stdout, stderr = process.communicate(input=request_json, timeout=timeout)
    except subprocess.TimeoutExpired:
        process.kill()
        return {"error": "Request timeout", "timeout": True}
    
    if stderr:
        print(f"Stderr: {stderr[:200]}", file=sys.stderr)
    
    try:
        response_line = stdout.strip().split('\n')[0] if stdout.strip() else ""
        if response_line:
            return json.loads(response_line)
        else:
            return {"error": "No response received", "stdout": stdout, "stderr": stderr}
    except json.JSONDecodeError as e:
        return {"error": f"JSON decode error: {e}", "stdout": stdout, "stderr": stderr}

def test_tool(docker_cmd, tool_name, arguments, test_name, timeout=120):
    """Test a specific tool."""
    print(f"\n{'='*70}")
    print(f"TEST: {test_name}")
    print(f"{'='*70}")
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
        request_id=3,
        timeout=timeout
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
                        # Show preview
                        preview = content[:200].replace('\n', ' ')
                        print(f"   Preview: {preview}...")
                    elif isinstance(content, dict):
                        print(f"   Result keys: {list(content.keys())}")
                        if "files" in content:
                            print(f"   Files found: {len(content.get('files', []))}")
                else:
                    print(f"   ⚠️  Tool returned error: {result_data.get('error', 'Unknown')[:200]}")
                    return False
            except Exception as e:
                print(f"   Response received (parsing skipped: {e})")
        return True
    else:
        print(f"❌ Unexpected response format")
        return False

def main():
    """Run functional tests with real data."""
    print("="*70)
    print("Functional Tests with Real Data")
    print("="*70)
    print("\nTest Identities:")
    print("  Handle: philsdetection")
    print("  Email 1: philsdetective@yahoo.com")
    print("  Email 2: phillip.morris@gmail.com")
    print("="*70)
    
    docker_cmd = ["docker", "run", "--rm", "-i", "osint-tools-mcp-server:latest"]
    
    tests_passed = 0
    tests_total = 0
    
    # Test 1: Sherlock - Username search
    tests_total += 1
    if test_tool(
        docker_cmd,
        "sherlock_username_search",
        {"username": "philsdetection", "timeout": 30},
        "Sherlock Username Search: philsdetection",
        timeout=180
    ):
        tests_passed += 1
    
    # Test 2: Holehe - Email 1
    tests_total += 1
    if test_tool(
        docker_cmd,
        "holehe_email_search",
        {"email": "philsdetective@yahoo.com", "timeout": 30},
        "Holehe Email Search: philsdetective@yahoo.com",
        timeout=60
    ):
        tests_passed += 1
    
    # Test 3: Holehe - Email 2
    tests_total += 1
    if test_tool(
        docker_cmd,
        "holehe_email_search",
        {"email": "phillip.morris@gmail.com", "timeout": 30},
        "Holehe Email Search: phillip.morris@gmail.com",
        timeout=60
    ):
        tests_passed += 1
    
    # Test 4: Maigret - Username search
    tests_total += 1
    if test_tool(
        docker_cmd,
        "maigret_username_search",
        {"username": "philsdetection", "timeout": 30},
        "Maigret Username Search: philsdetection",
        timeout=180
    ):
        tests_passed += 1
    
    # Test 5: Blackbird - Username search
    tests_total += 1
    if test_tool(
        docker_cmd,
        "blackbird_username_search",
        {"username": "philsdetection", "timeout": 30},
        "Blackbird Username Search: philsdetection",
        timeout=180
    ):
        tests_passed += 1
    
    # Test 6: theHarvester - Domain from email 1
    tests_total += 1
    if test_tool(
        docker_cmd,
        "theharvester_domain_search",
        {"domain": "yahoo.com", "sources": "baidu,duckduckgo", "limit": 50},
        "theHarvester Domain Search: yahoo.com",
        timeout=60
    ):
        tests_passed += 1
    
    # Test 7: GHunt - Email 2 (Gmail)
    tests_total += 1
    if test_tool(
        docker_cmd,
        "ghunt_google_search",
        {"identifier": "phillip.morris@gmail.com", "timeout": 30},
        "GHunt Google Search: phillip.morris@gmail.com",
        timeout=60
    ):
        tests_passed += 1
    
    # Test 8: theHarvester - Domain from email 2
    tests_total += 1
    if test_tool(
        docker_cmd,
        "theharvester_domain_search",
        {"domain": "gmail.com", "sources": "baidu,duckduckgo", "limit": 50},
        "theHarvester Domain Search: gmail.com",
        timeout=60
    ):
        tests_passed += 1
    
    # Summary
    print("\n" + "="*70)
    print("FUNCTIONAL TEST SUMMARY")
    print("="*70)
    print(f"Tests passed: {tests_passed}/{tests_total}")
    print(f"Success rate: {(tests_passed/tests_total*100):.1f}%")
    
    if tests_passed == tests_total:
        print("\n✅ ALL FUNCTIONAL TESTS PASSED!")
        print("🎉 All tools working correctly with real data!")
        return 0
    else:
        print(f"\n⚠️  {tests_total - tests_passed} test(s) failed")
        return 1

if __name__ == "__main__":
    sys.exit(main())

