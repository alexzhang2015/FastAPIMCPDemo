import pytest
import json
from fastapi.testclient import TestClient

def test_mcp_call_function(client: TestClient):
    response = client.post("/api/v1/mcp/call", json={
        "function_name": "echo",
        "parameters": {"message": "Hello MCP!"}
    })
    assert response.status_code == 200
    data = response.json()
    assert data["success"] == True
    assert data["result"]["echo"] == "Hello MCP!"

def test_mcp_call_math_function(client: TestClient):
    response = client.post("/api/v1/mcp/call", json={
        "function_name": "math_add",
        "parameters": {"a": 10, "b": 15}
    })
    assert response.status_code == 200
    data = response.json()
    assert data["success"] == True
    assert data["result"]["result"] == 25

def test_mcp_call_nonexistent_function(client: TestClient):
    response = client.post("/api/v1/mcp/call", json={
        "function_name": "nonexistent",
        "parameters": {}
    })
    assert response.status_code == 500

def test_mcp_stream_function(client: TestClient):
    response = client.post("/api/v1/mcp/stream", json={
        "function_name": "streaming_count",
        "parameters": {"count_to": 2, "delay": 0.1}
    })
    assert response.status_code == 200
    
    content = response.text
    lines = content.strip().split('\n\n')
    
    # Filter out empty lines and parse data
    data_lines = [line for line in lines if line.startswith('data: ')]
    assert len(data_lines) >= 3  # start + counts + complete
    
    # Parse first chunk
    first_chunk = json.loads(data_lines[0].replace('data: ', ''))
    assert first_chunk["type"] == "start"