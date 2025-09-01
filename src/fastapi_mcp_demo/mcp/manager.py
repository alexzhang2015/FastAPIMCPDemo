from typing import Dict, Any, List, AsyncGenerator
import asyncio
from .protocol import MCPProtocol, MCPFunction
from .stream import StreamHandler

class DefaultMCPProtocol(MCPProtocol):
    async def _execute_function(self, function_name: str, parameters: Dict[str, Any]) -> Any:
        return {"function": function_name, "parameters": parameters, "executed": True}

class MCPManager:
    def __init__(self):
        self.protocol = DefaultMCPProtocol()
        self.stream_handler = StreamHandler()
        self.is_running = False

    async def start(self) -> None:
        if not self.is_running:
            await self.protocol.initialize()
            await self._register_streaming_functions()
            self.is_running = True

    async def stop(self) -> None:
        if self.is_running:
            await self.protocol.shutdown()
            self.is_running = False

    async def call_function(self, function_name: str, parameters: Dict[str, Any] = None) -> Any:
        if not self.is_running:
            raise RuntimeError("MCP Manager not started")
        
        if parameters is None:
            parameters = {}
            
        return await self.protocol.call_function(function_name, parameters)

    async def stream_function(
        self, 
        function_name: str, 
        parameters: Dict[str, Any] = None
    ) -> AsyncGenerator[Dict[str, Any], None]:
        if not self.is_running:
            raise RuntimeError("MCP Manager not started")
        
        if parameters is None:
            parameters = {}

        async for chunk in self.stream_handler.stream_function_call(
            function_name, parameters, self.protocol
        ):
            yield chunk

    async def list_functions(self) -> List[Dict[str, Any]]:
        if not self.is_running:
            return []
        return await self.protocol.list_functions()

    def register_function(self, function: MCPFunction) -> None:
        self.protocol.register_function(function)

    async def _register_streaming_functions(self) -> None:
        self.protocol.register_function(MCPFunction(
            name="streaming_count",
            description="Stream counting numbers with configurable delay",
            parameters={
                "count_to": {"type": "number", "description": "Count up to this number", "default": 10},
                "delay": {"type": "number", "description": "Delay between counts in seconds", "default": 1.0}
            }
        ))

        self.protocol.register_function(MCPFunction(
            name="streaming_data",
            description="Stream data generation in chunks",
            parameters={
                "size": {"type": "number", "description": "Total number of items to generate", "default": 100},
                "chunk_size": {"type": "number", "description": "Number of items per chunk", "default": 10}
            }
        ))