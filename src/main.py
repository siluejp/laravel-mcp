from fastmcp import FastMCP
from src.tools.laravel_assistant import assistant_app
from starlette.requests import Request
from starlette.responses import JSONResponse

app = FastMCP(
    title="Laravel 5.6 Coding Assistant MCP Server",
    description="An MCP server providing an AI agent for Laravel 5.6 development.",
    version="0.1.0",
)

@app.exception_handler(Exception)
async def generic_exception_handler(request: Request, exc: Exception):
    """Catches all unhandled exceptions and returns a standard error response."""
    # In a real production app, you would log this exception in more detail.
    print(f"Unhandled exception: {exc}")
    return JSONResponse(
        status_code=500,
        content={"detail": "An internal server error occurred."},
    )

# Mount the assistant tool server
app.mount("/assistant", assistant_app)

@app.get("/")
def read_root():
    """A simple health check endpoint."""
    return {"status": "ok"}
