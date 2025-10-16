from fastmcp import FastMCP
from src.tools.laravel_assistant import assistant_app

app = FastMCP(name="LaravelAssistantMainServer")

# Mount the assistant tool server
app.mount("/assistant", assistant_app)

@app.resource("healthz://")
def health_check():
    """A simple health check resource."""
    return {"status": "ok"}

# Create the ASGI app that uvicorn can run for HTTP transport
asgi_app = app.streamable_http_app()

# Allow running the server directly and handle different transports
if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Run the FastMCP server.")
    parser.add_argument(
        "--transport",
        default="http",
        choices=["http", "stdio"],
        help="The transport protocol to use.",
    )
    args = parser.parse_args()

    if args.transport == "stdio":
        # This mode is used by the Codex extension
        app.run(transport="stdio")
    else:
        # This is for running directly via HTTP, though uvicorn is recommended
        import uvicorn
        print("Running in HTTP mode with uvicorn.")
        uvicorn.run(asgi_app, host="0.0.0.0", port=8000)