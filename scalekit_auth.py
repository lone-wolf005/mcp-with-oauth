from scalekit import ScalekitClient
from scalekit.common.scalekit import TokenValidationOptions
from fastmcp.server.auth import AuthProvider, AccessToken
from fastapi import Request, HTTPException
from jwt import ExpiredSignatureError

import os
from config import MCP_RESOURCE_URL, SCALEKIT_CLIENT_SECRET,SCALEKIT_ENVIRONMENT_URL,SCALEKIT_CLIENT_ID

scalekit_client = ScalekitClient(
    SCALEKIT_ENVIRONMENT_URL,
    SCALEKIT_CLIENT_ID,
    SCALEKIT_CLIENT_SECRET
)


class ScalekitAuth(AuthProvider):

    async def authenticate(self, request: Request):
        """Authenticate a request using bearer token.
        
        Returns:
            AccessToken if authenticated, None if not authenticated
        """
        # allow metadata endpoint without auth
        if ".well-known" in request.url.path:
            return None

        auth_header = request.headers.get("authorization")

        if not auth_header:
            # Return None - middleware will handle 401 with WWW-Authenticate header
            return None

        token = auth_header.replace("Bearer ", "")

        return await self.verify_token(token)


    async def verify_token(self, token: str):
        """Verify a bearer token and return access info if valid.
        
        Returns:
            AccessToken object if valid, None if invalid or expired
        """
        options = TokenValidationOptions(
            issuer=os.environ["SCALEKIT_ENVIRONMENT_URL"],
            audience=["http://localhost:9000"]
        )

        try:
            claims = scalekit_client.validate_token(
                token,
                options=options
            )
            
            return AccessToken(
                token=token,
                claims=claims,
                scopes=claims.get("scope", "").split(),
                client_id=os.environ["SCALEKIT_CLIENT_ID"]
            )

        except ExpiredSignatureError:
            # Return None for expired tokens - middleware will handle 401 response
            return None

        except Exception as e:
            # Return None for any validation failure - middleware will handle 401 response
            return None