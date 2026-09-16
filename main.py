import os
import json
from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse, JSONResponse
from pydantic import BaseModel

# Load environment variables from .env if present
load_dotenv()

from src.models import (
    ChatRequest,
    StructuredContext,
    EcologicalAnalysisResult,
    GeoCoordinates
)
from src.knowledge_engine import HybridKnowledgeEngine
from src.causal_engine import MultiMetricCausalEngine
from src.geo_engine import GeoSpatialResolver
from src.conversation_engine import ConversationIntelligenceEngine

app = FastAPI(
    title="Darukaa.Earth - AI Biodiversity Intelligence API",
    description="Knowledge-driven scientific AI system for ecological reasoning, multi-metric environmental analysis, and evidence-backed biodiversity restoration.",
    version="2.0.0"
)

# Enable CORS for local testing and web interfaces
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize Core Reasoning Engines
kb_engine = HybridKnowledgeEngine()
causal_engine = MultiMetricCausalEngine(kb_engine)
geo_resolver = GeoSpatialResolver()
conv_engine = ConversationIntelligenceEngine(kb_engine, causal_engine, geo_resolver)

# Static directory path
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
STATIC_DIR = os.path.join(BASE_DIR, "static")

# Ensure static directory exists
os.makedirs(STATIC_DIR, exist_ok=True)

@app.get("/api/health")
async def health_check():
    return {
        "status": "healthy",
        "system": "Darukaa.Earth AI Biodiversity Intelligence",
        "indexed_papers_count": len(kb_engine.documents),
        "domains_indexed": kb_engine.get_all_domains()
    }

@app.post("/api/chat", response_model=EcologicalAnalysisResult)
async def chat_endpoint(req: ChatRequest):
    """
    Multi-turn conversational intelligence endpoint.
    Handles natural language queries, detects missing variables, generates clarifying questions,
    and executes multi-metric causal reasoning with scientific citation links.
    """
    try:
        result = conv_engine.process_chat(req)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/analyze", response_model=EcologicalAnalysisResult)
async def analyze_endpoint(context: StructuredContext):
    """
    Direct structured JSON analysis endpoint.
    Bypasses conversational clarification and immediately returns quantitative projections and interventions.
    """
    try:
        req = ChatRequest(
            session_id="direct_analysis",
            message="Execute complete structured ecological analysis for the given parameters.",
            structured_context=context
        )
        result = conv_engine.process_chat(req)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/scenarios")
async def get_scenarios():
    """
    Returns benchmark challenge scenarios for one-click testing in the UI.
    """
    scenarios_path = os.path.join(BASE_DIR, "data", "scenarios.json")
    if os.path.exists(scenarios_path):
        with open(scenarios_path, "r", encoding="utf-8") as f:
            return json.load(f)
    return []

@app.get("/api/knowledge/search")
async def search_knowledge(
    q: str = Query(..., description="Search query for scientific literature"),
    top_k: int = Query(4, ge=1, le=10),
    domain: str = Query(None, description="Optional domain filter")
):
    """
    Search the indexed scientific knowledge base using hybrid dense/sparse vector retrieval.
    """
    results = kb_engine.retrieve(query=q, top_k=top_k, domain_filter=domain)
    return {
        "query": q,
        "count": len(results),
        "results": [r.model_dump() for r in results]
    }

@app.get("/api/knowledge/all")
async def get_all_knowledge():
    """
    Returns full metadata for all indexed peer-reviewed studies and reports.
    """
    return {
        "total_documents": len(kb_engine.documents),
        "documents": kb_engine.documents
    }

class GeoLookupRequest(BaseModel):
    lat: float = None
    lon: float = None
    region_text: str = None

@app.post("/api/geo/lookup")
async def geo_lookup(req: GeoLookupRequest):
    """
    Resolves geo-coordinates or regional descriptions to climatic classification and ecological baselines.
    """
    if req.lat is not None and req.lon is not None:
        return geo_resolver.resolve_coordinates(req.lat, req.lon)
    elif req.region_text:
        res = geo_resolver.resolve_region_text(req.region_text)
        if res:
            return res
        return {"error": "Region not recognized. Using default global temperate baseline."}
    raise HTTPException(status_code=400, detail="Must provide lat/lon or region_text")

# Serve frontend static assets
if os.path.exists(STATIC_DIR):
    app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")

@app.get("/")
async def serve_index():
    index_file = os.path.join(STATIC_DIR, "index.html")
    if os.path.exists(index_file):
        return FileResponse(index_file)
    return {"message": "Darukaa.Earth AI Biodiversity Intelligence API is running. UI assets loading."}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
