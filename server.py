import os
from typing import Optional, List, Any
from enum import Enum
from fastapi import FastAPI, HTTPException, Body
from pydantic import BaseModel
import asyncio
import cognee
from cognee import SearchType  # Import for query_type validation

# Set Cognee config (e.g., via env; adjust as needed)
os.environ["LLM_API_KEY"] = os.getenv("LLM_API_KEY", "your-openai-key")  # Or use .env
# os.environ["LLM_PROVIDER"] = "ollama"  # For local, etc.

app = FastAPI(title="Cognee API Wrapper", version="1.0")

class AddRequest(BaseModel):
    text: str
    user_id: Optional[str] = None
    node_set: Optional[str] = None
    dataset_name: Optional[str] = None

class CognifyRequest(BaseModel):
    datasets: Optional[List[str]] = None

class MemifyRequest(BaseModel):
    dataset: str
    extraction_tasks: Optional[List[Any]] = None  # Cognee Task objects; serialize if needed
    enrichment_tasks: Optional[List[Any]] = None

class SearchRequest(BaseModel):
    query_text: str
    query_type: SearchType = SearchType.GRAPH_COMPLETION
    user_id: Optional[str] = None
    node_set: Optional[str] = None
    node_name: Optional[List[str]] = None  # For advanced filters like CODING_RULES

class DeleteRequest(BaseModel):
    data_id: str

@app.post("/add", response_model=dict)
async def api_add(req: AddRequest):
    try:
        # Map to cognee.add (handles list of texts too; extend if needed)
        result = await cognee.add(
            req.text,
            user_id=req.user_id,
            node_set=req.node_set,
            dataset_name=req.dataset_name
        )
        return {"success": True, "data": {"data_id": result}, "message": "Data added"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/cognify", response_model=dict)
async def api_cognify(req: CognifyRequest):
    try:
        result = await cognee.cognify(datasets=req.datasets)
        return {"success": True, "data": result, "message": "Graph built"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/memify", response_model=dict)
async def api_memify(req: MemifyRequest):
    try:
        # Note: Tasks are Cognee objects; for API, pass serialized params or simplify to defaults
        result = await cognee.memify(
            dataset=req.dataset,
            extraction_tasks=req.extraction_tasks,
            enrichment_tasks=req.enrichment_tasks
        )
        return {"success": True, "data": result, "message": "Graph enriched"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/search", response_model=dict)
async def api_search(req: SearchRequest = Body(...)):
    try:
        results = await cognee.search(
            query_text=req.query_text,
            query_type=req.query_type,
            user_id=req.user_id,
            node_set=req.node_set,
            node_name=req.node_name  # If supported in search
        )
        return {"success": True, "data": results, "message": "Search complete"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/delete", response_model=dict)
async def api_delete(req: DeleteRequest):
    try:
        result = await cognee.delete(data_id=req.data_id)
        return {"success": True, "data": result, "message": "Data deleted"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/prune", response_model=dict)
async def api_prune():
    try:
        result = await cognee.prune()
        return {"success": True, "data": result, "message": "All memory cleared"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/health")
async def health():
    return {"status": "healthy"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
