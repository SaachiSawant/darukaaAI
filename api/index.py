import os
import sys
import json
import traceback

CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
PARENT_DIR = os.path.dirname(CURRENT_DIR)
for p in [CURRENT_DIR, PARENT_DIR, os.getcwd()]:
    if p and p not in sys.path:
        sys.path.insert(0, p)

from typing import Optional, List, Dict, Any
from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException, Query, Response, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse, JSONResponse, PlainTextResponse
from pydantic import BaseModel

# Load environment variables from .env if present
load_dotenv()

INIT_ERROR = None

try:
    try:
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
    except ImportError:
        from api.src.models import (
            ChatRequest,
            StructuredContext,
            EcologicalAnalysisResult,
            GeoCoordinates
        )
        from api.src.knowledge_engine import HybridKnowledgeEngine
        from api.src.causal_engine import MultiMetricCausalEngine
        from api.src.geo_engine import GeoSpatialResolver
        from api.src.conversation_engine import ConversationIntelligenceEngine
        from api.src.embedded_data import EMBEDDED_SCENARIOS
        from api.src.embedded_static import INDEX_HTML, STYLE_CSS, APP_JS

    # Initialize Core Reasoning Engines
    kb_engine = HybridKnowledgeEngine()
    causal_engine = MultiMetricCausalEngine(kb_engine)
    geo_resolver = GeoSpatialResolver()
    conv_engine = ConversationIntelligenceEngine(kb_engine, causal_engine, geo_resolver)
except Exception as e:
    INIT_ERROR = traceback.format_exc()

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

# Vercel Serverless Path Normalization Middleware
@app.middleware("http")
async def vercel_path_normalizer(request: Request, call_next):
    override_path = (
        request.query_params.get("path")
        or request.headers.get("x-matched-path")
        or request.headers.get("x-vercel-matched-path")
        or request.headers.get("x-forwarded-uri")
    )
    if override_path and override_path not in ["/api/index.py", "/api/index", "/api/main.py", "/api/main"]:
        if not override_path.startswith("/"):
            override_path = "/" + override_path
        request.scope["path"] = override_path
    else:
        raw_path = request.scope.get("path", "")
        for prefix in ["/api/index.py", "/api/index", "/api/main.py", "/api/main"]:
            if raw_path.startswith(prefix):
                new_path = raw_path[len(prefix):] or "/"
                request.scope["path"] = new_path
                break
    return await call_next(request)



if INIT_ERROR:
    @app.api_route("/{full_path:path}", methods=["GET", "POST", "PUT", "DELETE"])
    async def init_error_handler(full_path: str):
        return PlainTextResponse(f"Darukaa Initialization Diagnostics:\n{INIT_ERROR}", status_code=500)
else:
    @app.get("/health")
    @app.get("/api/health")
    async def health_check():
        return {
            "status": "healthy",
            "system": "Darukaa.Earth AI Biodiversity Intelligence",
            "indexed_papers_count": len(kb_engine.documents),
            "domains_indexed": kb_engine.get_all_domains()
        }

    @app.post("/api/chat")
    @app.post("/chat")
    async def chat_endpoint(req: ChatRequest):
        try:
            result = conv_engine.process_chat(req)
            return result
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))

    @app.post("/api/analyze")
    @app.post("/analyze")
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
    @app.get("/scenarios")
    async def get_scenarios():
        return EMBEDDED_SCENARIOS

    @app.get("/api/knowledge/search")
    @app.get("/knowledge/search")
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
    @app.get("/knowledge/all")
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
    @app.post("/geo/lookup")
    async def geo_lookup(req: GeoLookupRequest):
        if req.lat is not None and req.lon is not None:
            return geo_resolver.resolve_coordinates(req.lat, req.lon)
        elif req.region_text:
            res = geo_resolver.resolve_region_text(req.region_text)
            if res:
                return res
            return {"error": "Region not recognized. Using default global temperate baseline."}
        raise HTTPException(status_code=400, detail="Must provide lat/lon or region_text")

    @app.get("/", response_class=HTMLResponse)
    @app.get("/index", response_class=HTMLResponse)
    @app.get("/api", response_class=HTMLResponse)
    @app.get("/api/index", response_class=HTMLResponse)
    @app.get("/api/index.py", response_class=HTMLResponse)
    async def serve_index():
        return HTMLResponse(content=INDEX_HTML)

    @app.get("/static/style.css")
    @app.get("/style.css")
    async def serve_css():
        return Response(content=STYLE_CSS, media_type="text/css")

    @app.get("/static/app.js")
    @app.get("/app.js")
    async def serve_js():
        return Response(content=APP_JS, media_type="application/javascript")

    @app.api_route("/{rest_of_path:path}", methods=["GET", "POST", "PUT", "DELETE"])
    async def catch_all_debug(request: Request, rest_of_path: str):
        return JSONResponse({
            "debug": "catch_all_triggered",
            "rest_of_path": rest_of_path,
            "url": str(request.url),
            "path": request.scope.get("path"),
            "raw_path": str(request.scope.get("raw_path")),
            "root_path": request.scope.get("root_path")
        })

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)

