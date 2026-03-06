# ScaleKit MCP Server with OAuth Authentication

A FastAPI-based Model Context Protocol (MCP) server that demonstrates OAuth 2.0 authentication using ScaleKit. This server provides secure, scope-based access to tools and resources.

## Features

- 🔐 **OAuth 2.0 Authentication** - Secure token-based authentication via ScaleKit
- 🛠️ **MCP Tools** - Expose authenticated tools through the Model Context Protocol
- 🎯 **Scope-Based Access Control** - Fine-grained permissions using OAuth scopes
- 📊 **OAuth Metadata Endpoint** - RFC 8414 compliant resource server metadata
- ⚡ **FastAPI Integration** - High-performance async API framework

## Prerequisites

- Python 3.13 or higher
- [uv](https://docs.astral.sh/uv/) package manager
- ScaleKit account with OAuth application configured

## Installation

1. Clone the repository:

```bash
git clone <repository-url>
cd scaleKit-auth
```

2. Install dependencies using uv:

```bash
uv sync
```

3. Configure environment variables:

```bash
cp .env.example .env
```

Edit [`.env`](.env) with your ScaleKit credentials:

```env
SCALEKIT_ENVIRONMENT_URL=https://your-environment.scalekit.dev
SCALEKIT_CLIENT_ID=your_client_id
SCALEKIT_CLIENT_SECRET=your_client_secret
MCP_RESOURCE_URL=http://localhost:9000
```

## Configuration

### ScaleKit Setup

1. Create a ScaleKit account at [scalekit.com](https://scalekit.com)
2. Create an OAuth application
3. Configure the following:
   - **Redirect URIs**: Add your application's callback URL
   - **Scopes**: `profile:read`, `analytics:read`
   - **Audience**: `http://localhost:9000`

### Environment Variables

| Variable                   | Description                   | Example                             |
| -------------------------- | ----------------------------- | ----------------------------------- |
| `SCALEKIT_ENVIRONMENT_URL` | Your ScaleKit environment URL | `https://personal-xxx.scalekit.dev` |
| `SCALEKIT_CLIENT_ID`       | OAuth client ID               | `skc_xxxxx`                         |
| `SCALEKIT_CLIENT_SECRET`   | OAuth client secret           | `test_xxxxx`                        |
| `MCP_RESOURCE_URL`         | MCP server resource URL       | `http://localhost:9000`             |

## Usage

### Starting the Server

Run the server using uvicorn:

```bash
uv run uvicorn main:app --host 0.0.0.0 --port 9000 --reload
```

The server will be available at:

- **MCP Endpoint**: `http://localhost:9000/mcp`
- **OAuth Metadata**: `http://localhost:9000/.well-known/oauth-protected-resource/mcp`
- **API Docs**: `http://localhost:9000/docs`

### Available Tools

#### 1. `get_profile`

Returns the authenticated user's profile information.

**Scopes Required**: None (uses email from token claims)

**Example Response**:

```
Hello user@example.com
```

#### 2. `analytics`

Provides access to analytics data.

**Scopes Required**: `analytics:read`

**Example Response**:

```
Analytics data
```

If the required scope is missing:

```
Access denied
```

## Authentication Flow

1. **Client requests access token** from ScaleKit authorization server
2. **Client includes token** in Authorization header: `Bearer <token>`
3. **Server validates token** using [`ScalekitAuth`](scalekit_auth.py:17) provider
4. **Token verification** checks:
   - Token signature validity
   - Issuer matches ScaleKit environment
   - Audience includes the MCP resource URL
   - Token is not expired
5. **Access granted** if validation succeeds

## Project Structure

```
.
├── main.py                 # FastAPI app and MCP server setup
├── scalekit_auth.py        # ScaleKit authentication provider
├── config.py               # Configuration and environment loading
├── pyproject.toml          # Project dependencies
├── .env                    # Environment variables (not in git)
├── .gitignore             # Git ignore rules
└── README.md              # This file
```

## API Endpoints

### OAuth Metadata Endpoint

**GET** `/.well-known/oauth-protected-resource/mcp`

Returns OAuth 2.0 resource server metadata per [RFC 8414](https://datatracker.ietf.org/doc/html/rfc8414):

```json
{
  "authorization_servers": ["https://personal-xxx.scalekit.dev"],
  "bearer_methods_supported": ["header"],
  "resource": "http://localhost:9000/mcp",
  "resource_documentation": "http://localhost:9000/mcp/docs",
  "scopes_supported": ["profile:read", "analytics:read"]
}
```

## Development

### Hot Reload

The server runs with `--reload` flag enabled, automatically restarting when code changes are detected.

### Environment Reload

Use [`reload_env.py`](reload_env.py) to reload environment variables without restarting:

```bash
uv run python reload_env.py
```

## Security Considerations

- ⚠️ **Never commit** [`.env`](.env) file to version control
- 🔒 Use **HTTPS** in production environments
- 🔑 Rotate **client secrets** regularly
- ✅ Validate **token expiration** and scopes on every request
- 🛡️ Implement **rate limiting** for production deployments

## Dependencies

- **fastapi** - Modern web framework for building APIs
- **fastmcp** - Model Context Protocol server implementation
- **scalekit-sdk-python** - ScaleKit Python SDK for OAuth
- **python-dotenv** - Environment variable management
- **uvicorn** - ASGI server for FastAPI
- **psycopg2-binary** - PostgreSQL adapter (if needed)

## Troubleshooting

### Token Validation Fails

- Verify `SCALEKIT_ENVIRONMENT_URL` matches your ScaleKit environment
- Ensure audience in token matches `http://localhost:9000`
- Check token hasn't expired

### Authentication Returns 401

- Confirm Authorization header format: `Bearer <token>`
- Validate token was issued by correct ScaleKit environment
- Check required scopes are included in token

### Server Won't Start

- Verify Python version is 3.13+
- Run `uv sync` to install dependencies
- Check port 9000 is not already in use

## License

[Add your license here]

## Contributing

[Add contribution guidelines here]

## Support

For issues related to:

- **ScaleKit SDK**: Visit [ScaleKit Documentation](https://docs.scalekit.com)
- **FastMCP**: Check [FastMCP GitHub](https://github.com/jlowin/fastmcp)
- **This Project**: Open an issue in this repository
