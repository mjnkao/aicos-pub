#!/usr/bin/env python3
"""AICOS MCP HTTP-to-Stdio wrapper for OpenClaw"""
import sys
import json
import urllib.request
import urllib.error

DAEMON_URL = "http://127.0.0.1:8000/mcp"
TOKEN = "aApK5miDqcBKfJXYURAKiL9GClP90jcvnyaqCuV5"

def call_mcp(method, params=None):
    payload = {"jsonrpc": "2.0", "id": 1, "method": method, "params": params or {}}
    req = urllib.request.Request(
        DAEMON_URL,
        data=json.dumps(payload).encode(),
        headers={"Authorization": f"Bearer {TOKEN}", "Content-Type": "application/json"},
        method="POST"
    )
    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            return json.loads(resp.read().decode())
    except urllib.error.HTTPError as e:
        return {"error": {"code": e.code, "message": str(e)}}
    except Exception as e:
        return {"error": {"code": "client_error", "message": str(e)}}

if __name__ == "__main__":
    # Read request from stdin
    raw = sys.stdin.read().strip()
    if not raw:
        sys.exit(0)
    
    # Handle batched JSON-RPC (multiple lines)
    lines = [l for l in raw.split('\n') if l.strip()]
    results = []
    
    for line in lines:
        try:
            req = json.loads(line)
            method = req.get("method", "")
            params = req.get("params", {})
            
            if method == "tools/list":
                results.append(call_mcp("tools/list"))
            elif method == "tools/call":
                name = params.get("name", "")
                args = params.get("arguments", {})
                results.append(call_mcp("tools/call", {"name": name, "arguments": args}))
            else:
                results.append({"error": {"code": "method_not_found", "message": f"Unknown method: {method}"}})
        except json.JSONDecodeError:
            results.append({"error": {"code": "parse_error", "message": "Invalid JSON"}})
    
    # Output results (one per line)
    for r in results:
        print(json.dumps(r))