# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is a FastAPI wrapper for the Cognee library that exposes AI memory graph functionality via REST API. The server wraps Cognee's core functions (add, cognify, memify, search, delete, prune) and is designed to be used with Claude Code Skills or other API clients.

## Architecture

The project consists of three main components:

### 1. Server (server.py:1-112)
- FastAPI application that wraps Cognee library functions
- Exposes endpoints: `/add`, `/cognify`, `/memify`, `/search`, `/delete`, `/prune`, `/health`
- Uses Pydantic models for request validation
- Configuration via environment variables (LLM_API_KEY, LLM_PROVIDER)
- All endpoints are async and return JSON with structure: `{"success": bool, "data": any, "message": str}`

### 2. Client (client.py:1-67)
- Async HTTP client using `httpx` for interacting with the server
- Mirrors server API with typed methods
- Includes SearchType enum (GRAPH_COMPLETION, INSIGHTS, CODING_RULES)
- Provides example workflow pattern for typical usage

### 3. Request/Response Models
- `AddRequest`: Ingests text data with optional user_id, node_set, dataset_name
- `CognifyRequest`: Builds knowledge graph from datasets
- `MemifyRequest`: Enriches graphs with extraction/enrichment tasks
- `SearchRequest`: Queries the graph with query_type, filters (user_id, node_set, node_name)
- `DeleteRequest`: Removes data by data_id

## Common Commands

### Running the Server
```bash
# Install dependencies (Cognee library required)
pip install cognee-api

# Run server with auto-reload
uvicorn cognee_api.server:app --reload

# Or run directly
python server.py
```
Server runs on `http://0.0.0.0:8000` by default.

### Development
```bash
# Run server locally for testing
python server.py

# Test client (requires server running)
python client.py
```

## Configuration

The server requires environment variables:
- `LLM_API_KEY`: OpenAI API key or provider-specific key (required)
- `LLM_PROVIDER`: Optional, can be set to "ollama" for local LLM usage

Use `.env.example` as a template (do not commit actual .env files).

## Typical Workflow

1. **Ingest data**: POST to `/add` with text content and optional metadata
2. **Build graph**: POST to `/cognify` with dataset names to process
3. **Enrich graph**: POST to `/memify` with dataset and optional tasks
4. **Query**: POST to `/search` with query_text and query_type
5. **Cleanup**: POST to `/delete` for specific data or `/prune` to clear all

See client.py:56-65 for example async workflow pattern.

## Key Implementation Details

- All Cognee operations are async - use `await` when calling
- Error handling wraps exceptions into HTTPException with 500 status
- SearchType enum must match Cognee's search types
- The server sets LLM_API_KEY from environment on startup (server.py:11)
- Client base_url defaults to `http://localhost:8000` but is configurable
