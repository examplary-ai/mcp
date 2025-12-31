#!/bin/bash
# Build script for creating .mcpb package locally

set -e

echo "Building Examplary MCP Server..."
echo ""

# Clean up old package
rm -f examplary-mcp.mcpb

# Create the package
echo "Creating .mcpb package..."
zip -r examplary-mcp.mcpb \
  manifest.json \
  pyproject.toml \
  src/ \
  $([ -f icon.png ] && echo "icon.png") \
  -x "*.pyc" \
  -x "*__pycache__/*" \
  -x ".git/*" \
  -x ".github/*" \
  -x "*.md" \
  -x ".mcpbignore"

echo ""
echo "Package created: examplary-mcp.mcpb"
echo ""
echo "Package contents:"
unzip -l examplary-mcp.mcpb

echo ""
echo "Build complete!"
echo ""
echo "To install in Claude Desktop:"
echo "1. Open Claude Desktop"
echo "2. Go to Settings → Extensions"
echo "3. Click 'Install Extension'"
echo "4. Select examplary-mcp.mcpb"
