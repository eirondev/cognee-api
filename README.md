# Cognee API

A FastAPI server wrapper for [Cognee](https://github.com/topoteretes/cognee) that exposes AI memory graph functionality via REST API. Perfect for integration with Claude Code Skills, automation workflows, and building AI-powered applications.

## Overview

Cognee API provides a RESTful interface to Cognee's powerful knowledge graph capabilities, enabling you to:

- Ingest and process text data into structured knowledge graphs
- Build semantic relationships between concepts
- Query AI memory using natural language
- Manage and enrich knowledge bases programmatically

## Features

- **RESTful API** - Clean HTTP endpoints for all Cognee operations
- **Async by Default** - Built on FastAPI for high-performance async operations
- **Type Safety** - Full Pydantic validation for requests and responses
- **Multiple Search Modes** - Graph completion, insights extraction, and coding rules
- **Multi-tenant Support** - User and node set isolation for different contexts
- **Production Ready** - Health checks, error handling, and structured responses

## Quick Start

### Installation

```bash
pip install fastapi uvicorn cognee httpx
```

### Configuration

Create a `.env` file based on `.env.example`:

```bash
LLM_API_KEY=your-openai-api-key-here
# LLM_PROVIDER=ollama  # Uncomment for local LLM usage
```

### Running the Server

```bash
# Development mode with auto-reload
uvicorn server:app --reload

# Production mode
uvicorn server:app --host 0.0.0.0 --port 8000
```

The server will start at `http://localhost:8000`. Visit `http://localhost:8000/docs` for interactive API documentation.

## Deployment to eva_cognee Server

### From Development Machine

1. Create your `.env` file in the project directory with your environment variables:
   ```bash
   LLM_API_KEY=your-api-key-here
   ```

2. Run the deployment script:
   ```bash
   ./deploy.sh
   ```

### Setup on eva_cognee Server

After deploying files to the server, SSH into eva_cognee and set up the environment:

```bash
# SSH into the server
ssh root@eva_cognee

# Navigate to the project directory
cd /root/cognee-api

# Create a virtual environment
python3 -m venv venv

# Activate the virtual environment
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Run the server
python server.py
```

The server will start on `http://0.0.0.0:8000` (accessible at `http://eva_cognee:8000` or `http://192.168.30.33:8000`)

### Running the Server on eva_cognee

To run the server after initial setup:

```bash
cd /root/cognee-api
source venv/bin/activate
python server.py
```

## API Endpoints

### Health Check
```http
GET /health
```

### Add Data
```http
POST /add
Content-Type: application/json

{
  "text": "Your text content here",
  "user_id": "optional-user-id",
  "node_set": "optional-node-set",
  "dataset_name": "optional-dataset-name"
}
```

### Build Knowledge Graph
```http
POST /cognify
Content-Type: application/json

{
  "datasets": ["dataset1", "dataset2"]
}
```

### Enrich Graph
```http
POST /memify
Content-Type: application/json

{
  "dataset": "dataset-name",
  "extraction_tasks": [],
  "enrichment_tasks": []
}
```

### Search
```http
POST /search
Content-Type: application/json

{
  "query_text": "What is Cognee?",
  "query_type": "GRAPH_COMPLETION",
  "user_id": "optional-user-id",
  "node_set": "optional-node-set",
  "node_name": []
}
```

**Search Types:**
- `GRAPH_COMPLETION` - General knowledge graph queries
- `INSIGHTS` - Extract insights and patterns
- `CODING_RULES` - Query coding-specific rules

### Delete Data
```http
POST /delete
Content-Type: application/json

{
  "data_id": "data-id-to-delete"
}
```

### Clear All Data
```http
POST /prune
```

## Using the Python Client

```python
import asyncio
from client import CogneeClient, SearchType

async def main():
    client = CogneeClient(base_url="http://localhost:8000")

    # Ingest data
    add_result = await client.add(
        "Cognee builds AI memory graphs.",
        dataset_name="demo"
    )

    # Build knowledge graph
    await client.cognify(datasets=["demo"])

    # Enrich (optional)
    await client.memify(dataset="demo")

    # Query the graph
    search_result = await client.search(
        "What is Cognee?",
        query_type=SearchType.GRAPH_COMPLETION
    )
    print(search_result["data"])

    await client.close()

asyncio.run(main())
```

## Typical Workflow

1. **Ingest** - Add your text data using `/add`
2. **Process** - Build the knowledge graph with `/cognify`
3. **Enrich** - Optionally enhance with `/memify`
4. **Query** - Search your knowledge base with `/search`
5. **Manage** - Clean up with `/delete` or `/prune`

## Response Format

All endpoints return consistent JSON responses:

```json
{
  "success": true,
  "data": {},
  "message": "Operation description"
}
```

Error responses follow the same structure with `"success": false`.

## Development

### Project Structure

```
cognee-api/
├── server.py          # FastAPI server implementation
├── client.py          # Python client library
├── .env.example       # Environment variables template
├── README.md          # This file
└── CLAUDE.md          # Claude Code integration guide
```

### Requirements

- Python 3.8+
- FastAPI
- Uvicorn
- Cognee
- httpx (for client)
- Pydantic

## Use Cases

- **Claude Code Skills** - Build AI assistants with persistent memory
- **Documentation Q&A** - Ingest docs and query with natural language
- **Knowledge Management** - Create searchable knowledge bases
- **Code Analysis** - Extract and query coding patterns and rules
- **Research Tools** - Build semantic research databases

## License

[Add your license here]

## Contributing

[Add contribution guidelines here]

## Support

For issues and questions:
- Cognee documentation: [Cognee GitHub](https://github.com/topoteretes/cognee)
- FastAPI documentation: [FastAPI Docs](https://fastapi.tiangolo.com/)
