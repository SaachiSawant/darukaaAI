from typing import List, Dict, Any, Optional
from pydantic import BaseModel, Field

class GeoCoordinates(BaseModel):
    lat: float
    lon: float

class StructuredContext(BaseModel):
    soil_organic_carbon: Optional[float] = Field(default=None, description="Soil Organic Carbon percentage (SOC %)")
    soil_ph: Optional[float] = Field(default=None, description="Soil pH level (0-14)")
    annual_rainfall_mm: Optional[float] = Field(default=None, description="Annual rainfall in mm")
    rainfall_category: Optional[str] = Field(default=None, description="Rainfall pattern: low, seasonal, moderate, high, arid")
    land_use: Optional[str] = Field(default=None, description="Land use type (e.g. monoculture_wheat, pasture, degraded_forest, orchard)")
    crop_type: Optional[str] = Field(default=None, description="Current or target crops")
    region: Optional[str] = Field(default=None, description="Geographical region or biome")
    coordinates: Optional[GeoCoordinates] = Field(default=None, description="Latitude and Longitude")
    tillage_practice: Optional[str] = Field(default=None, description="Tillage intensity (e.g. conventional_tillage, reduced, no_till)")
    degradation_level: Optional[str] = Field(default=None, description="Level of land degradation (low, moderate, severe, critical)")
    primary_goal: Optional[str] = Field(default=None, description="Primary landowner goal (e.g., carbon_sequestration, pollinator_boost, water_retention, yield_resilience)")

class ChatRequest(BaseModel):
    session_id: Optional[str] = Field(default="default_session", description="Session identifier for multi-turn conversations")
    message: str = Field(..., description="User message or query")
    structured_context: Optional[StructuredContext] = Field(default=None, description="Optional structured metrics provided alongside the message")

class ClarificationQuestion(BaseModel):
    field_name: str
    question: str
    importance: str
    suggested_options: Optional[List[str]] = None

class MetricImpact(BaseModel):
    metric_name: str
    display_name: str
    category: str  # soil, climate, biodiversity, water, carbon
    baseline_estimate: str
    short_term_change: str   # 0 - 1 year
    medium_term_change: str  # 2 - 4 years
    long_term_change: str    # 5 - 10 years
    unit: str
    confidence_level: str    # High, Moderate, Projected
    scientific_basis: str

class ScientificCitation(BaseModel):
    id: str
    title: str
    authors: str
    year: int
    publisher: str
    doi_or_url: str
    relevant_finding: str
    relevance_score: float

class CausalChainNode(BaseModel):
    input_variable: str
    direct_mechanism: str
    downstream_impact: str
    impacted_biodiversity_indicator: str
    scientific_rationale: str

class ScientificIntervention(BaseModel):
    id: str
    title: str
    category: str
    what_to_do: str
    why_it_works: str
    impacted_metrics: List[str]
    time_horizon: str
    evidence_citations: List[ScientificCitation]
    risks_and_mitigations: str
    confidence_rating: str

class EcologicalAnalysisResult(BaseModel):
    session_id: str
    query_intent: str
    is_clarification_needed: bool
    missing_variables: List[str]
    clarification_questions: List[ClarificationQuestion]
    ecological_diagnosis: str
    multi_variable_interactions: List[str]
    causal_chains: List[CausalChainNode]
    interventions: List[ScientificIntervention]
    projected_metrics: List[MetricImpact]
    citations: List[ScientificCitation]
    geo_context_resolved: Optional[Dict[str, Any]] = None
    scientific_confidence_summary: Dict[str, Any]
    markdown_report: str
