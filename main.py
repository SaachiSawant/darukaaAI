import os
import sys
import json

CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
API_DIR = os.path.join(CURRENT_DIR, "api")
for p in [CURRENT_DIR, API_DIR, os.getcwd()]:
    if p and p not in sys.path:
        sys.path.insert(0, p)

from typing import Optional, List, Dict, Any
from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException, Query, Response
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse, JSONResponse
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
from src.embedded_data import EMBEDDED_SCENARIOS
from src.embedded_static import INDEX_HTML, STYLE_CSS, APP_JS


app = FastAPI(
    title="Darukaa.Earth - AI Biodiversity Intelligence API",
    description="Knowledge-driven scientific AI system for ecological reasoning, multi-metric environmental analysis, and evidence-backed biodiversity restoration.",
    version="2.0.0"
)

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Multi-path discovery for serverless / Vercel
def find_dir(dir_name: str) -> str:
    candidates = [
        os.path.join(os.path.dirname(os.path.abspath(__file__)), "api", dir_name),
        os.path.join(os.path.dirname(os.path.abspath(__file__)), dir_name),
        os.path.join(os.getcwd(), "api", dir_name),
        os.path.join(os.getcwd(), dir_name),
        os.path.join(os.path.dirname(os.getcwd()), dir_name)
    ]
    for c in candidates:
        if os.path.exists(c):
            return c
    return candidates[1]

STATIC_DIR = find_dir("static")
DATA_DIR = find_dir("data")

# Initialize Core Reasoning Engines
kb_engine = HybridKnowledgeEngine()
causal_engine = MultiMetricCausalEngine(kb_engine)
geo_resolver = GeoSpatialResolver()
conv_engine = ConversationIntelligenceEngine(kb_engine, causal_engine, geo_resolver)

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
    try:
        result = conv_engine.process_chat(req)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/analyze", response_model=EcologicalAnalysisResult)
async def analyze_endpoint(context: StructuredContext):
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
    scenarios_path = os.path.join(DATA_DIR, "scenarios.json")
    if os.path.exists(scenarios_path):
        with open(scenarios_path, "r", encoding="utf-8") as f:
            return json.load(f)
    return EMBEDDED_SCENARIOS

@app.get("/api/knowledge/search")
async def search_knowledge(
    q: str = Query(..., description="Search query for scientific literature"),
    top_k: int = Query(4, ge=1, le=10),
    domain: str = Query(None, description="Optional domain filter")
):
    results = kb_engine.retrieve(query=q, top_k=top_k, domain_filter=domain)
    return {
        "query": q,
        "count": len(results),
        "results": [r.model_dump() for r in results]
    }

@app.get("/api/knowledge/all")
async def get_all_knowledge():
    return {
        "total_documents": len(kb_engine.documents),
        "documents": kb_engine.documents
    }

class GeoLookupRequest(BaseModel):
    lat: Optional[float] = None
    lon: Optional[float] = None
    region_text: Optional[str] = None

@app.post("/api/geo/lookup")
async def geo_lookup(req: GeoLookupRequest):
    if req.lat is not None and req.lon is not None:
        return geo_resolver.resolve_coordinates(req.lat, req.lon)
    elif req.region_text:
        res = geo_resolver.resolve_region_text(req.region_text)
        if res:
            return res
        return {"error": "Region not recognized. Using default global temperate baseline."}
    raise HTTPException(status_code=400, detail="Must provide lat/lon or region_text")

# Direct Static Routes (Zero-dependency on aiofiles/Starlette StaticFiles)
def read_static_file(filename: str) -> str:
    candidates = [
        os.path.join(STATIC_DIR, filename),
        os.path.join(os.path.dirname(os.path.abspath(__file__)), "static", filename),
        os.path.join(os.path.dirname(os.path.abspath(__file__)), "api", "static", filename),
        os.path.join(os.getcwd(), "static", filename),
        os.path.join(os.getcwd(), "api", "static", filename)
    ]
    for c in candidates:
        if os.path.exists(c):
            try:
                with open(c, "r", encoding="utf-8") as f:
                    return f.read()
            except Exception:
                pass
    if filename == "index.html":
        return INDEX_HTML
    elif filename == "style.css":
        return STYLE_CSS
    elif filename == "app.js":
        return APP_JS
    return ""


@app.get("/", response_class=HTMLResponse)
@app.get("/index", response_class=HTMLResponse)
@app.get("/api", response_class=HTMLResponse)
@app.get("/api/index", response_class=HTMLResponse)
async def serve_index():
    content = read_static_file("index.html")
    if content:
        return HTMLResponse(content=content)
    return HTMLResponse(content="<h1>Darukaa.Earth AI Biodiversity Intelligence API is running.</h1>")

@app.get("/health")
async def health_alias():
    return await health_check()

@app.get("/static/style.css")
async def serve_css():
    content = read_static_file("style.css")
    return Response(content=content, media_type="text/css")

@app.get("/static/app.js")
async def serve_js():
    content = read_static_file("app.js")
    return Response(content=content, media_type="application/javascript")

if __name__ == "__main__":
    import uvicorn

    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)

