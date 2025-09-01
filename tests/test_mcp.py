import pytest
import asyncio
from src.fastapi_mcp_demo.mcp import MCPManager, MCPFunction

@pytest.mark.asyncio
async def test_mcp_manager_lifecycle():
    manager = MCPManager()
    
    assert not manager.is_running
    
    await manager.start()
    assert manager.is_running
    
    await manager.stop()
    assert not manager.is_running

@pytest.mark.asyncio
async def test_mcp_builtin_functions():
    manager = MCPManager()
    await manager.start()
    
    try:
        result = await manager.call_function("echo", {"message": "test"})
        assert result["echo"] == "test"
        
        result = await manager.call_function("math_add", {"a": 5, "b": 3})
        assert result["result"] == 8
        
        result = await manager.call_function("get_time")
        assert "current_time" in result
        
    finally:
        await manager.stop()

@pytest.mark.asyncio
async def test_mcp_streaming():
    manager = MCPManager()
    await manager.start()
    
    try:
        chunks = []
        async for chunk in manager.stream_function("streaming_count", {"count_to": 3, "delay": 0.1}):
            chunks.append(chunk)
        
        assert len(chunks) >= 4  # start + 3 counts + complete
        assert chunks[0]["type"] == "start"
        assert chunks[-1]["type"] == "complete"
        assert chunks[-1]["final"] == True
        
    finally:
        await manager.stop()

@pytest.mark.asyncio
async def test_custom_function_registration():
    manager = MCPManager()
    await manager.start()
    
    async def custom_handler(params):
        return {"custom": "response", "input": params}
    
    custom_function = MCPFunction(
        name="custom_test",
        description="Test custom function",
        parameters={"input": {"type": "string"}},
        handler=custom_handler
    )
    
    manager.register_function(custom_function)
    
    try:
        result = await manager.call_function("custom_test", {"input": "test_value"})
        assert result["custom"] == "response"
        assert result["input"]["input"] == "test_value"
        
    finally:
        await manager.stop()