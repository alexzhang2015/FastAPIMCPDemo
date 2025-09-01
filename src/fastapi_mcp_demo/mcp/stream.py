from typing import AsyncGenerator, Dict, Any
import asyncio
import json

class StreamHandler:
    def __init__(self):
        self.active_streams: Dict[str, bool] = {}

    async def stream_function_call(
        self, 
        function_name: str, 
        parameters: Dict[str, Any],
        protocol
    ) -> AsyncGenerator[Dict[str, Any], None]:
        stream_id = f"{function_name}_{id(parameters)}"
        self.active_streams[stream_id] = True

        try:
            if function_name == "streaming_count":
                async for chunk in self._streaming_count(parameters):
                    if not self.active_streams.get(stream_id, False):
                        break
                    yield chunk
            elif function_name == "streaming_data":
                async for chunk in self._streaming_data(parameters):
                    if not self.active_streams.get(stream_id, False):
                        break
                    yield chunk
            else:
                result = await protocol.call_function(function_name, parameters)
                yield {"type": "result", "data": result, "final": True}

        finally:
            self.active_streams.pop(stream_id, None)

    async def _streaming_count(self, parameters: Dict[str, Any]) -> AsyncGenerator[Dict[str, Any], None]:
        count_to = parameters.get("count_to", 10)
        delay = parameters.get("delay", 1.0)
        
        yield {"type": "start", "data": {"message": f"Starting count to {count_to}"}}
        
        for i in range(1, count_to + 1):
            await asyncio.sleep(delay)
            yield {
                "type": "progress", 
                "data": {
                    "current": i, 
                    "total": count_to,
                    "percentage": (i / count_to) * 100
                }
            }
        
        yield {"type": "complete", "data": {"message": "Count completed!"}, "final": True}

    async def _streaming_data(self, parameters: Dict[str, Any]) -> AsyncGenerator[Dict[str, Any], None]:
        data_size = parameters.get("size", 100)
        chunk_size = parameters.get("chunk_size", 10)
        
        yield {"type": "start", "data": {"message": f"Generating {data_size} data points"}}
        
        for i in range(0, data_size, chunk_size):
            await asyncio.sleep(0.1)
            chunk_data = [{"id": j, "value": j * 2} for j in range(i, min(i + chunk_size, data_size))]
            yield {
                "type": "chunk",
                "data": {
                    "items": chunk_data,
                    "chunk_number": i // chunk_size + 1,
                    "total_chunks": (data_size + chunk_size - 1) // chunk_size
                }
            }
        
        yield {"type": "complete", "data": {"message": "Data generation completed!"}, "final": True}

    def stop_stream(self, stream_id: str) -> None:
        self.active_streams[stream_id] = False