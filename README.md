# Examplary MCP Server

A Model Context Protocol (MCP) server for [Examplary](https://examplary.ai), providing AI assistants with access to the Examplary exam management API.

## Features

- **60+ API Endpoints** - Full access to Examplary's exam management capabilities
- **Auto-generated Tools** - All API operations automatically available as MCP tools via OpenAPI specification
- **Secure Authentication** - User-specific API key authentication
- **Cross-platform** - Works on macOS, Linux, and Windows via UV runtime
- **One-click Installation** - Install as a .mcpb package in Claude Desktop

## What is Examplary?

Examplary is an AI-powered exam management platform that helps educators:
- Create and manage exams with AI assistance
- Generate questions from source materials
- Grade student responses automatically
- Organize content in collaborative workspaces
- Share resources via publisher libraries

## Installation

### Option 1: Claude Desktop (.mcpb package)

1. Download the latest `examplary-mcp.mcpb` from the [releases page](https://github.com/examplary/examplary-mcp/releases)
2. Open Claude Desktop
3. Go to Settings → Extensions
4. Click "Install Extension" and select the downloaded .mcpb file
5. When prompted, enter your Examplary API key

### Option 2: Manual Installation

1. Clone this repository:
   ```bash
   git clone https://github.com/examplary/examplary-mcp.git
   cd examplary-mcp
   ```

2. Install UV (if not already installed):
   ```bash
   curl -LsSf https://astral.sh/uv/install.sh | sh
   ```

3. Run the server:
   ```bash
   export EXAMPLARY_API_KEY="your-api-key-here"
   uv run src/server.py
   ```

## Getting Your API Key

1. Log in to [Examplary](https://app.examplary.ai)
2. Navigate to [Account → Developer](https://app.examplary.ai/account/developer)
3. Click "Generate New API Key"
4. Copy the API key and save it securely

**Note:** Keep your API key secret. Never commit it to version control or share it publicly.

## Usage

Once installed in Claude Desktop, you can ask Claude to interact with Examplary:

- "Create a new exam about Python programming"
- "List all my exams"
- "Generate questions from this document"
- "Get the results for exam ID 12345"
- "Create a new organization workspace"

The MCP server provides access to all Examplary API endpoints, including:

### Exam Management
- Create, read, update, and delete exams
- Duplicate exams
- Export to PDF or Word
- AI-powered question generation

### Question Bank
- Store and organize reusable questions
- Public and private question types
- Bulk import from various formats

### Student Sessions
- Create grading sessions
- Scan documents for answers
- AI-powered grading and feedback
- Accept or reject grading suggestions

### Organizations & Collaboration
- Manage workspaces
- Invite team members
- Organize exams in folders

### Publisher Library
- Browse public content
- Share exam templates
- Discover featured resources

## Development

### Project Structure

```
examplary-mcp/
├── manifest.json       # MCPB manifest configuration
├── pyproject.toml      # Python dependencies
├── src/
│   ├── __init__.py
│   └── server.py       # Main MCP server
├── .mcpbignore        # Files excluded from .mcpb package
└── .github/
    └── workflows/
        └── release.yml # Automated release workflow
```

### Local Development

1. Install dependencies:
   ```bash
   uv pip install -e .
   ```

2. Set your API key:
   ```bash
   export EXAMPLARY_API_KEY="your-api-key"
   ```

3. Run the server:
   ```bash
   uv run src/server.py
   ```

### Building the .mcpb Package

To build the .mcpb package manually:

```bash
zip -r examplary-mcp.mcpb \
  manifest.json \
  pyproject.toml \
  src/ \
  icon.png \
  -x "*.pyc" -x "__pycache__/*" -x ".git/*"
```

### Testing

The server uses stdio transport for communication with Claude Desktop. To test locally:

1. Run the server with your API key set
2. The server will start and listen for MCP protocol messages on stdin
3. Send MCP requests via stdin and receive responses on stdout

## API Rate Limits

Examplary enforces rate limits on certain operations:
- Exam generation: 3 requests per 60 seconds
- Question operations: 10 requests per 60 seconds
- Other endpoints: Standard rate limiting applies

## Security

- API keys are stored securely by Claude Desktop
- All communication uses HTTPS
- API keys can be revoked at any time from the Examplary dashboard
- Never share your API key or commit it to version control

## Support

- **Examplary Documentation**: https://developers.examplary.ai
- **Examplary Support**: support@examplary.ai
- **Issues**: https://github.com/examplary/examplary-mcp/issues

## License

MIT License - see LICENSE file for details

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## Credits

Built with:
- [FastMCP](https://gofastmcp.com) - Python framework for MCP servers
- [Model Context Protocol](https://modelcontextprotocol.io) - Open protocol for AI-application integration
- [Examplary API](https://api.examplary.ai) - Exam management platform
