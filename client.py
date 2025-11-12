import httpx
from typing import Optional, List, Any
from enum import Enum
from pydantic import BaseModel
import asyncio

class SearchType(Enum):  # Mirror Cognee's SearchType enum
    SUMMARIES = "SUMMARIES"
    CHUNKS = "CHUNKS"
    RAG_COMPLETION = "RAG_COMPLETION"
    GRAPH_COMPLETION = "GRAPH_COMPLETION"
    GRAPH_SUMMARY_COMPLETION = "GRAPH_SUMMARY_COMPLETION"
    CODE = "CODE"
    CYPHER = "CYPHER"
    NATURAL_LANGUAGE = "NATURAL_LANGUAGE"
    GRAPH_COMPLETION_COT = "GRAPH_COMPLETION_COT"
    GRAPH_COMPLETION_CONTEXT_EXTENSION = "GRAPH_COMPLETION_CONTEXT_EXTENSION"
    FEELING_LUCKY = "FEELING_LUCKY"
    FEEDBACK = "FEEDBACK"
    TEMPORAL = "TEMPORAL"
    CODING_RULES = "CODING_RULES"
    CHUNKS_LEXICAL = "CHUNKS_LEXICAL"

class CogneeClient:
    def __init__(self, base_url: str = "http://localhost:8000", timeout: float = 300.0):
        self.base_url = base_url
        # Set a longer timeout for operations that may take time (downloading models, processing)
        self.client = httpx.AsyncClient(base_url=base_url, timeout=timeout)

    async def add(self, text: str, user_id: Optional[str] = None, node_set: Optional[str] = None, dataset_name: Optional[str] = None) -> dict:
        data = {"text": text, "user_id": user_id, "node_set": node_set, "dataset_name": dataset_name}
        resp = await self.client.post("/add", json=data)
        try:
            resp.raise_for_status()
        except httpx.HTTPStatusError as e:
            # Try to get more details from the error response
            try:
                error_detail = resp.json()
                print(f"Server error details: {error_detail}")
            except:
                print(f"Server response: {resp.text}")
            raise
        return resp.json()

    async def cognify(self, datasets: Optional[List[str]] = None) -> dict:
        data = {"datasets": datasets} if datasets else {}
        resp = await self.client.post("/cognify", json=data)
        resp.raise_for_status()
        return resp.json()

    async def memify(self, dataset: str, extraction_tasks: Optional[List[Any]] = None, enrichment_tasks: Optional[List[Any]] = None) -> dict:
        data = {"dataset": dataset, "extraction_tasks": extraction_tasks, "enrichment_tasks": enrichment_tasks}
        resp = await self.client.post("/memify", json=data)
        resp.raise_for_status()
        return resp.json()

    async def search(self, query_text: str, query_type: SearchType = SearchType.GRAPH_COMPLETION, user_id: Optional[str] = None, node_set: Optional[str] = None, node_name: Optional[List[str]] = None) -> dict:
        data = {"query_text": query_text, "query_type": query_type.value, "user_id": user_id, "node_set": node_set, "node_name": node_name}
        resp = await self.client.post("/search", json=data)
        try:
            resp.raise_for_status()
        except httpx.HTTPStatusError as e:
            # Try to get more details from the error response
            try:
                error_detail = resp.json()
                print(f"Server error details: {error_detail}")
            except:
                print(f"Server response: {resp.text}")
            raise
        return resp.json()

    async def delete(self, data_id: str) -> dict:
        data = {"data_id": data_id}
        resp = await self.client.post("/delete", json=data)
        resp.raise_for_status()
        return resp.json()

    async def prune(self) -> dict:
        """Clear all data (documents, knowledge graphs, etc.)"""
        resp = await self.client.post("/prune")
        resp.raise_for_status()
        return resp.json()

    async def prune_system(self) -> dict:
        """Clear system data (graph, vector, metadata, cache)"""
        resp = await self.client.post("/prune_system")
        resp.raise_for_status()
        return resp.json()

    async def health(self) -> dict:
        resp = await self.client.get("/health")
        resp.raise_for_status()
        return resp.json()

    async def close(self):
        await self.client.aclose()

# Example Usage (for Claude Code Skill)
async def example_workflow(client: CogneeClient):
    # Ingest and process
    add_res = await client.add("Cognee builds AI memory graphs.", dataset_name="demo")
    await client.cognify(datasets=["demo"])
    await client.memify(dataset="demo")  # Enrich if needed

    # Query
    search_res = await client.search("What is Cognee?", query_type=SearchType.GRAPH_COMPLETION)
    print(search_res["data"])

# Run: asyncio.run(example_workflow(CogneeClient()))
