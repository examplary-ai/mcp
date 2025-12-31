#!/usr/bin/env python3
"""Examplary MCP Server - Main entry point"""

import os
import sys
import httpx
from fastmcp import FastMCP


def get_api_key() -> str:
    """Get the API key from environment or MCP config"""
    # Try environment variable first (for local testing)
    api_key = os.getenv("EXAMPLARY_API_KEY")

    if not api_key:
        # In production, Claude Desktop will set this via MCP_USER_CONFIG
        # The user_config from manifest.json gets passed as environment variables
        # with MCP_USER_CONFIG_ prefix
        api_key = os.getenv("MCP_USER_CONFIG_API_KEY")

    if not api_key:
        print("ERROR: No API key provided. Please set EXAMPLARY_API_KEY environment variable",
              file=sys.stderr)
        print("or configure the api_key in Claude Desktop settings.", file=sys.stderr)
        sys.exit(1)

    return api_key


def patch_openapi_spec(spec: dict) -> dict:
    """Patch OpenAPI spec to fix validation issues and filter endpoints"""
    # Remove unwanted endpoints
    excluded_patterns = [
        "api-key",
        "api_key",
        "library",
        "libraries",
        "oauth"
    ]

    if "paths" in spec:
        paths_to_remove = [
            path for path in spec["paths"].keys()
            if any(pattern in path.lower() for pattern in excluded_patterns)
        ]

        for path in paths_to_remove:
            print(f"Excluding endpoint: {path}", file=sys.stderr)
            del spec["paths"][path]

        # Add missing description fields to response objects
        for path, path_item in spec["paths"].items():
            for method, operation in path_item.items():
                if method in ["get", "post", "put", "patch", "delete"] and "responses" in operation:
                    for status_code, response in operation["responses"].items():
                        # Add description if missing
                        if isinstance(response, dict) and "description" not in response:
                            response["description"] = f"Response for {method.upper()} {path}"

    return spec


def create_server() -> FastMCP:
    """Create and configure the Examplary MCP server"""
    # Get API key
    api_key = get_api_key()

    # Fetch the OpenAPI specification
    print("Fetching OpenAPI specification...", file=sys.stderr)
    try:
        response = httpx.get("https://api.examplary.ai/openapi", timeout=30.0)
        response.raise_for_status()
        openapi_spec = response.json()
        print(f"Successfully loaded OpenAPI spec (version {openapi_spec.get('openapi', 'unknown')})",
              file=sys.stderr)

        # Patch the spec to fix validation issues
        print("Patching OpenAPI spec to fix validation issues...", file=sys.stderr)
        openapi_spec = patch_openapi_spec(openapi_spec)

    except Exception as e:
        print(f"ERROR: Failed to fetch OpenAPI spec: {e}", file=sys.stderr)
        sys.exit(1)

    # Create authenticated HTTP client
    client = httpx.AsyncClient(
        base_url="https://api.examplary.ai",
        headers={
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        },
        timeout=30.0
    )

    # Create MCP server from OpenAPI specification
    print("Creating MCP server from OpenAPI spec...", file=sys.stderr)
    mcp = FastMCP.from_openapi(
        openapi_spec=openapi_spec,
        client=client,
        name="Examplary"
    )

    print("MCP server created successfully!", file=sys.stderr)
    return mcp


def main():
    """Main entry point"""
    try:
        mcp = create_server()
        # Run the server via stdio (default transport for MCPB)
        mcp.run()
    except Exception as e:
        print(f"ERROR: Failed to start Examplary MCP server: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
