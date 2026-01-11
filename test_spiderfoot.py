#!/usr/bin/env python3
"""
Quick test for SpiderFoot tool
"""

import json
import subprocess
import sys

def test_spiderfoot():
    """Test SpiderFoot with a quick scan."""
    print("Testing SpiderFoot...")
    print("Note: SpiderFoot scans can take 5-30 minutes for full scans")
    print("This test uses a quick scan with limited modules\n")
    
    request = {
        "jsonrpc": "2.0",
        "id": 1,
        "method": "tools/call",
        "params": {
            "name": "spiderfoot_scan",
            "arguments": {
                "target": "example.com"
            }
        }
    }
    
    request_json = json.dumps(request) + "\n"
    
    docker_cmd = ["docker", "run", "--rm", "-i", "osint-tools-mcp-server:latest"]
    
    process = subprocess.Popen(
        docker_cmd,
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True
    )
    
    try:
        stdout, stderr = process.communicate(input=request_json, timeout=60)
        
        if stderr:
            print(f"Stderr: {stderr[:500]}", file=sys.stderr)
        
        try:
            response = json.loads(stdout.strip().split('\n')[0])
            if "result" in response:
                print("✅ SpiderFoot responded successfully")
                result_data = json.loads(response["result"]["content"][0].get("text", "{}"))
                if result_data.get("success"):
                    print("✅ SpiderFoot scan completed")
                    return 0
                else:
                    print(f"⚠️  SpiderFoot returned error: {result_data.get('error', 'Unknown')}")
                    return 1
            else:
                print(f"❌ Unexpected response: {response}")
                return 1
        except json.JSONDecodeError:
            print(f"❌ Failed to parse response: {stdout[:200]}")
            return 1
    except subprocess.TimeoutExpired:
        print("⏱️  Test timed out (SpiderFoot can take a long time)")
        process.kill()
        return 1

if __name__ == "__main__":
    sys.exit(test_spiderfoot())

