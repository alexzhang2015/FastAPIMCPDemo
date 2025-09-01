from contextlib import asynccontextmanager
from fastapi import FastAPI
from .mcp import MCPManager

mcp_manager = MCPManager()

@asynccontextmanager
async def lifespan(app: FastAPI):
    await mcp_manager.start()
    yield
    await mcp_manager.stop()

app = FastAPI(
    title="FastAPI MCP Demo",
    description="A FastAPI application with MCP capabilities and streamable HTTP support",
    version="1.0.0",
    lifespan=lifespan
)

from .api import router
app.include_router(router)

@app.get("/")
async def hello_world():
    return {"message": "Hello, World!"}