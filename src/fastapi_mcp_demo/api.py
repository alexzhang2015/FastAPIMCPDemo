from fastapi import APIRouter, HTTPException, Request
from fastapi.responses import StreamingResponse
from typing import Dict, Any, AsyncGenerator
import json
from .main import mcp_manager

router = APIRouter(prefix="/api/v1", tags=["MCP API"])

@router.get("/health")
async def health_check():
    return {"status": "healthy", "mcp_status": "active"}

@router.post("/mcp/call")
async def call_mcp_function(request: Dict[str, Any]):
    try:
        result = await mcp_manager.call_function(
            request.get("function_name"),
            request.get("parameters", {})
        )
        return {"success": True, "result": result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/mcp/stream")
async def stream_mcp_function(request: Dict[str, Any]):
    try:
        async def generate_stream() -> AsyncGenerator[str, None]:
            async for chunk in mcp_manager.stream_function(
                request.get("function_name"),
                request.get("parameters", {})
            ):
                yield f"data: {json.dumps(chunk)}\n\n"
        
        return StreamingResponse(
            generate_stream(),
            media_type="text/plain",
            headers={"Content-Type": "text/event-stream"}
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/mcp/functions")
async def list_mcp_functions():
    return {"functions": await mcp_manager.list_functions()}