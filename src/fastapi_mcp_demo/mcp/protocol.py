from typing import Dict, Any, Optional, List
from abc import ABC, abstractmethod
import asyncio
import json

class MCPFunction:
    def __init__(self, name: str, description: str, parameters: Dict[str, Any], handler=None):
        self.name = name
        self.description = description
        self.parameters = parameters
        self.handler = handler

class MCPProtocol(ABC):
    def __init__(self):
        self.functions: Dict[str, MCPFunction] = {}
        self.is_connected = False

    async def initialize(self) -> None:
        self.is_connected = True
        await self._setup_builtin_functions()

    async def shutdown(self) -> None:
        self.is_connected = False
        self.functions.clear()

    def register_function(self, function: MCPFunction) -> None:
        self.functions[function.name] = function

    async def call_function(self, function_name: str, parameters: Dict[str, Any]) -> Any:
        if not self.is_connected:
            raise RuntimeError("MCP protocol not initialized")
        
        if function_name not in self.functions:
            raise ValueError(f"Function '{function_name}' not found")
        
        function = self.functions[function_name]
        if function.handler:
            return await function.handler(parameters)
        else:
            return await self._execute_function(function_name, parameters)

    async def list_functions(self) -> List[Dict[str, Any]]:
        return [
            {
                "name": func.name,
                "description": func.description,
                "parameters": func.parameters
            }
            for func in self.functions.values()
        ]

    @abstractmethod
    async def _execute_function(self, function_name: str, parameters: Dict[str, Any]) -> Any:
        pass

    async def _setup_builtin_functions(self) -> None:
        async def echo_handler(params: Dict[str, Any]) -> Dict[str, Any]:
            return {"echo": params.get("message", "Hello from MCP!")}

        async def math_add_handler(params: Dict[str, Any]) -> Dict[str, Any]:
            a = params.get("a", 0)
            b = params.get("b", 0)
            return {"result": a + b}

        async def get_time_handler(params: Dict[str, Any]) -> Dict[str, Any]:
            import datetime
            return {"current_time": datetime.datetime.now().isoformat()}

        self.register_function(MCPFunction(
            name="echo",
            description="Echo back a message",
            parameters={"message": {"type": "string", "description": "Message to echo"}},
            handler=echo_handler
        ))

        self.register_function(MCPFunction(
            name="math_add",
            description="Add two numbers",
            parameters={
                "a": {"type": "number", "description": "First number"},
                "b": {"type": "number", "description": "Second number"}
            },
            handler=math_add_handler
        ))

        self.register_function(MCPFunction(
            name="get_time",
            description="Get current time",
            parameters={},
            handler=get_time_handler
        ))