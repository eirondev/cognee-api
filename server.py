import os
from typing import Optional, List, Any
from enum import Enum
from fastapi import FastAPI, HTTPException, Body
from pydantic import BaseModel
import asyncio
import cognee
from cognee import SearchType  # Import for query_type validation
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

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
        # Build kwargs dict with only non-None values to handle different cognee versions
        kwargs = {}
        if req.dataset_name is not None:
            kwargs['dataset_name'] = req.dataset_name
        if req.user_id is not None:
            kwargs['user_id'] = req.user_id
        if req.node_set is not None:
            kwargs['node_set'] = req.node_set

        # Call cognee.add with only supported parameters
        result = await cognee.add(req.text, **kwargs)
        return {"success": True, "data": {"data_id": result}, "message": "Data added"}
    except TypeError as e:
        # If we get a TypeError about unexpected arguments, try with just the text and dataset_name
        if "unexpected keyword argument" in str(e):
            try:
                result = await cognee.add(req.text, dataset_name=req.dataset_name)
                return {"success": True, "data": {"data_id": result}, "message": "Data added"}
            except:
                # If that fails too, try with just the text
                result = await cognee.add(req.text)
                return {"success": True, "data": {"data_id": result}, "message": "Data added"}
        raise HTTPException(status_code=500, detail=str(e))
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
        # Build kwargs dict with only non-None values
        kwargs = {"query_text": req.query_text}

        if req.query_type is not None:
            kwargs['query_type'] = req.query_type
        if req.user_id is not None:
            kwargs['user_id'] = req.user_id
        if req.node_set is not None:
            kwargs['node_set'] = req.node_set
        if req.node_name is not None:
            kwargs['node_name'] = req.node_name

        results = await cognee.search(**kwargs)
        return {"success": True, "data": results, "message": "Search complete"}
    except TypeError as e:
        # If we get a TypeError about unexpected arguments, try with minimal params
        if "unexpected keyword argument" in str(e):
            try:
                results = await cognee.search(
                    query_text=req.query_text,
                    query_type=req.query_type
                )
                return {"success": True, "data": results, "message": "Search complete"}
            except:
                # If that fails, try with just query_text
                results = await cognee.search(req.query_text)
                return {"success": True, "data": results, "message": "Search complete"}
        raise HTTPException(status_code=500, detail=str(e))
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
    """Clear all data (documents, knowledge graphs, etc.)"""
    try:
        result = await cognee.prune.prune_data()
        return {"success": True, "data": result, "message": "All data cleared"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/prune_system", response_model=dict)
async def api_prune_system():
    """Clear system data (graph, vector, metadata, cache)"""
    try:
        result = await cognee.prune.prune_system(graph=True, vector=True, metadata=True, cache=True)
        return {"success": True, "data": result, "message": "System data cleared"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/health")
async def health():
    return {"status": "healthy"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8181)
