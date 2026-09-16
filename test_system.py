import unittest
import json
import os
from src.knowledge_engine import HybridKnowledgeEngine
from src.causal_engine import MultiMetricCausalEngine
from src.geo_engine import GeoSpatialResolver
from src.conversation_engine import ConversationIntelligenceEngine
from src.models import ChatRequest, StructuredContext, GeoCoordinates

class TestDarukaaBiodiversityIntelligence(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.kb = HybridKnowledgeEngine()
        cls.causal = MultiMetricCausalEngine(cls.kb)
        cls.geo = GeoSpatialResolver()
        cls.conv = ConversationIntelligenceEngine(cls.kb, cls.causal, cls.geo)

    def test_01_knowledge_retrieval(self):
        """Test RAG hybrid retrieval matches relevant peer-reviewed studies"""
        query = "soil organic carbon cover crops mycorrhizae"
        results = self.kb.retrieve(query, top_k=3)
        self.assertGreaterEqual(len(results), 1)
        self.assertTrue(any("FAO" in r.id or "PAUSTIAN" in r.id or "BLANCO" in r.id for r in results))
        self.assertGreater(results[0].relevance_score, 0.0)
        print(f"\n[PASS] RAG Knowledge Retrieval: Found '{results[0].title}' (Score: {results[0].relevance_score})")

    def test_02_ambiguity_clarification_detection(self):
        """Test missing variable detection when sparse prompt is supplied"""
        sparse_req = ChatRequest(
            session_id="test_sparse_session",
            message="Biodiversity is declining on my land"
        )
        res = self.conv.process_chat(sparse_req)
        self.assertTrue(res.is_clarification_needed)
        self.assertGreater(len(res.clarification_questions), 0)
        
        # Verify clarification questions cover key variables
        q_fields = [q.field_name for q in res.clarification_questions]
        self.assertTrue("soil_organic_carbon" in q_fields or "rainfall_pattern" in q_fields or "land_use" in q_fields)
        print(f"[PASS] Ambiguity Clarification: Generated {len(res.clarification_questions)} clarifying questions.")

    def test_03_multi_metric_causal_reasoning_semi_arid_wheat(self):
        """Test the hackathon benchmark: 0.3% SOC, low rainfall, monoculture wheat, semi-arid"""
        req = ChatRequest(
            session_id="test_semi_arid_wheat",
            message="Input: Soil organic carbon: 0.3%, Rainfall: low (380mm), Crop: monoculture wheat, Region: semi-arid",
            structured_context=StructuredContext(
                soil_organic_carbon=0.3,
                rainfall_category="low",
                annual_rainfall_mm=380,
                land_use="monoculture_wheat",
                region="semi-arid"
            )
        )
        res = self.conv.process_chat(req)
        
        # Verify multi-metric interactions (at least 3 variables connected)
        self.assertGreaterEqual(len(res.causal_chains), 1)
        self.assertGreaterEqual(len(res.interventions), 2)
        
        # Verify interventions include agroforestry, cover cropping, or biochar
        intervention_titles = " ".join([i.title for i in res.interventions]).lower()
        self.assertTrue("agroforestry" in intervention_titles or "cover crop" in intervention_titles or "biochar" in intervention_titles)
        
        # Verify quantitative projections have time horizons
        self.assertGreaterEqual(len(res.projected_metrics), 3)
        for metric in res.projected_metrics:
            self.assertTrue(metric.short_term_change)
            self.assertTrue(metric.medium_term_change)
            self.assertTrue(metric.long_term_change)
        
        # Verify citations from FAO/IPCC
        citation_ids = [c.id for c in res.citations]
        self.assertTrue(any("FAO" in cid or "IPCC" in cid or "LAL" in cid for cid in citation_ids))
        print(f"[PASS] Multi-Metric Reasoning: Synthesized {len(res.interventions)} interventions and {len(res.projected_metrics)} quantitative metrics with FAO/IPCC citations.")

    def test_04_geospatial_resolution(self):
        """Test coordinate resolution to Köppen climate zone and biome"""
        # Central India coordinates (23.26 N, 77.41 E)
        geo_res = self.geo.resolve_coordinates(23.2599, 77.4126)
        self.assertIn("BSh", geo_res["koppen_classification"])
        self.assertIn("dominant_soil_order", geo_res)
        self.assertGreater(len(geo_res["primary_vulnerabilities"]), 0)
        print(f"[PASS] Geo-Spatial Resolution: Resolved (23.26, 77.41) -> {geo_res['koppen_classification']} | {geo_res['biome']}")

    def test_05_multi_turn_memory(self):
        """Test multi-turn context accumulation across conversation turns"""
        sid = "test_multiturn_session"
        
        # Turn 1: User gives partial info
        req1 = ChatRequest(session_id=sid, message="My farm is suffering from severe drought in a semi-arid zone with 350mm rainfall.")
        res1 = self.conv.process_chat(req1)
        
        # Turn 2: User provides missing SOC and crop type
        req2 = ChatRequest(session_id=sid, message="My soil organic carbon was tested at 0.35% and I have been monocropping wheat with heavy plow tillage.")
        res2 = self.conv.process_chat(req2)
        
        # Verify that accumulated context retained rainfall from turn 1 and SOC from turn 2
        acc_ctx = self.conv.sessions[sid]["accumulated_context"]
        self.assertEqual(acc_ctx.annual_rainfall_mm, 350.0)
        self.assertEqual(acc_ctx.soil_organic_carbon, 0.35)
        self.assertEqual(acc_ctx.crop_type, "wheat")
        print(f"[PASS] Multi-Turn Memory: Accumulated variables across turns (Rainfall={acc_ctx.annual_rainfall_mm}mm, SOC={acc_ctx.soil_organic_carbon}%, Crop={acc_ctx.crop_type})")

if __name__ == "__main__":
    unittest.main()
