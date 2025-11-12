import httpx
from typing import Optional, List, Any
from enum import Enum
from pydantic import BaseModel
import asyncio

class SearchType(Enum):  # Mirror Cognee's
    GRAPH_COMPLETION = "GRAPH_COMPLETION"
    INSIGHTS = "INSIGHTS"
    CODING_RULES = "CODING_RULES"

class CogneeClient:
    def __init__(self, base_url: str = "http://localhost:8000"):
        self.base_url = base_url
        self.client = httpx.AsyncClient(base_url=base_url)

    async def add(self, text: str, user_id: Optional[str] = None, node_set: Optional[str] = None, dataset_name: Optional[str] = None) -> dict:
        data = {"text": text, "user_id": user_id, "node_set": node_set, "dataset_name": dataset_name}
        resp = await self.client.post("/add", json=data)
        resp.raise_for_status()
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
        resp.raise_for_status()
        return resp.json()

    async def delete(self, data_id: str) -> dict:
        data = {"data_id": data_id}
        resp = await self.client.post("/delete", json=data)
        resp.raise_for_status()
        return resp.json()

    async def prune(self) -> dict:
        resp = await self.client.post("/prune")
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
