# Claude Code Configuration

## Development Commands

### Running the Application
```bash
uv run uvicorn src.fastapi_mcp_demo.main:app --reload --host 0.0.0.0 --port 8000
```

### Testing
```bash
uv run pytest
uv run pytest -v  # Verbose output
uv run pytest --cov=src  # With coverage
```

### Linting and Type Checking
```bash
uv run ruff check src/ tests/
uv run ruff format src/ tests/
uv run mypy src/
```

## Project Structure

- `src/fastapi_mcp_demo/` - Main application code
  - `main.py` - FastAPI application entry point
  - `api.py` - API endpoints for MCP functionality
  - `mcp/` - MCP abstraction layer
    - `manager.py` - Main MCP manager
    - `protocol.py` - MCP protocol implementation
    - `stream.py` - Streaming capabilities
- `tests/` - Test suite
- `pyproject.toml` - Project configuration and dependencies

## API Endpoints

- `GET /` - Hello World endpoint
- `GET /api/v1/health` - Health check
- `GET /api/v1/mcp/functions` - List available MCP functions
- `POST /api/v1/mcp/call` - Call MCP function
- `POST /api/v1/mcp/stream` - Stream MCP function results

## MCP Functions

Built-in functions:
- `echo` - Echo back a message
- `math_add` - Add two numbers
- `get_time` - Get current timestamp
- `streaming_count` - Stream counting with configurable delay
- `streaming_data` - Stream data generation in chunks