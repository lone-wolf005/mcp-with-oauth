"""
Utility script to reload environment variables from .env file
"""
import os
from dotenv import load_dotenv

def reload_env():
    """Reload environment variables from .env file"""
    # Clear existing environment variables (optional - only if you want to remove old ones)
    # Be careful with this as it clears ALL env vars
    # os.environ.clear()
    
    # Reload from .env file, override existing values
    load_dotenv(override=True)
    
    print("Environment variables reloaded from .env file")
    print(f"SCALEKIT_ENVIRONMENT_URL: {os.environ.get('SCALEKIT_ENVIRONMENT_URL')}")
    print(f"SCALEKIT_CLIENT_ID: {os.environ.get('SCALEKIT_CLIENT_ID')}")
    print(f"MCP_RESOURCE_URL: {os.environ.get('MCP_RESOURCE_URL')}")

if __name__ == "__main__":
    reload_env()

# Made with Bob
