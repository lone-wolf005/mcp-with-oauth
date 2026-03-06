from fastapi import FastAPI
from fastmcp import FastMCP
from fastmcp.server.dependencies import get_access_token

from scalekit_auth import ScalekitAuth
from config import MCP_RESOURCE_URL


mcp = FastMCP(
    "Scalekit MCP Server",
    auth=ScalekitAuth()
)

@mcp.tool()
def get_profile():

    token = get_access_token()
    email = token.claims.get("email")

    return f"Hello {email}"


@mcp.tool()
def analytics():

    token = get_access_token()

    if "analytics:read" not in token.scopes:
        return "Access denied"

    return "Analytics data"


# create MCP ASGI app
mcp_app = mcp.http_app(path="/")


# IMPORTANT: attach lifespan
app = FastAPI(lifespan=mcp_app.lifespan)

# mount MCP server
app.mount("/mcp", mcp_app)


@app.get("/.well-known/oauth-protected-resource/mcp")
async def oauth_metadata():

    return {
        "authorization_servers": [
            "https://personal-agmrnd6eaadae.scalekit.dev"
        ],
        "bearer_methods_supported": ["header"],
        "resource": MCP_RESOURCE_URL,
        "resource_documentation": f"{MCP_RESOURCE_URL}/docs",
        "scopes_supported": [
            "profile:read",
            "analytics:read"
        ]
    }