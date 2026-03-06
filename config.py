import os
from dotenv import load_dotenv

# Load environment variables from .env file
# override=True ensures .env values take precedence over existing env vars
load_dotenv(override=True)

SCALEKIT_ENVIRONMENT_URL = os.environ["SCALEKIT_ENVIRONMENT_URL"]
SCALEKIT_CLIENT_ID = os.environ["SCALEKIT_CLIENT_ID"]
SCALEKIT_CLIENT_SECRET = os.environ["SCALEKIT_CLIENT_SECRET"]

MCP_RESOURCE_URL = "http://localhost:9000/mcp"