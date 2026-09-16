import math
from typing import Dict, Any, Optional

class GeoSpatialResolver:
    """
    Resolves geographical coordinates and regional names to ecological biomes,
    Köppen climate classifications, baseline soil characteristics, and climatic vulnerabilities.
    """
    def __init__(self):
        # Known reference regions & coordinates
        self.known_regions = {
            "semi-arid dryland": {
                "koppen_class": "BSh / BSk (Semi-Arid Steppe)",
                "biome": "Drylands & Shrublands",
                "default_rainfall_mm": 380,
                "dominant_soil_order": "Aridisols / Vertisols",
                "primary_vulnerabilities": ["Wind erosion", "High evaporative deficit", "Crusting & hardsetting", "Terminal drought stress"],
                "ecological_priorities": ["Soil armor & mulch", "Deep-rooting legume agroforestry", "Keyline water harvesting"]
            },
            "tropical savanna": {
                "koppen_class": "Aw (Tropical Wet & Dry)",
                "biome": "Tropical & Subtropical Grasslands / Savannas",
                "default_rainfall_mm": 1100,
                "dominant_soil_order": "Oxisols / Ultisols (Acidic)",
                "primary_vulnerabilities": ["Aluminum toxicity", "High phosphorus fixation", "Dry-season moisture stress", "Compaction from grazing"],
                "ecological_priorities": ["Silvopasture integration", "pH buffering / liming", "Mycorrhizal inoculation"]
            },
            "temperate alluvial plain": {
                "koppen_class": "Cfa / Dfa (Humid Subtropical / Continental)",
                "biome": "Temperate Broadleaf & Mixed Forests / Alluvial Basin",
                "default_rainfall_mm": 850,
                "dominant_soil_order": "Inceptisols / Alfisols / Mollisols",
                "primary_vulnerabilities": ["Agricultural nitrate leaching", "Pesticide runoff", "Compaction from heavy machinery", "Pollinator corridor loss"],
                "ecological_priorities": ["Multi-tier riparian buffers", "Cover crop bio-drilling", "Beetle banks & hedgerows"]
            },
            "arid irrigated basin": {
                "koppen_class": "BWh (Hot Arid Desert)",
                "biome": "Deserts & Xeric Shrublands",
                "default_rainfall_mm": 250,
                "dominant_soil_order": "Aridisols / Solonchaks (Saline)",
                "primary_vulnerabilities": ["Secondary salinization", "Sodicity / high exchangeable sodium", "Groundwater drawdown", "Microbial dormancy"],
                "ecological_priorities": ["Halophyte & deep taproot bio-drainage", "Gypsum/organic matter leaching", "Biochar microbial refugia"]
            },
            "mediterranean dry-summer": {
                "koppen_class": "Csa / Csb (Mediterranean Dry Summer)",
                "biome": "Mediterranean Forests, Woodlands & Scrub",
                "default_rainfall_mm": 520,
                "dominant_soil_order": "Alfisoils / Inceptisols",
                "primary_vulnerabilities": ["Summer drought & wildfire risk", "Sheet erosion on slopes", "Soil organic carbon oxidation"],
                "ecological_priorities": ["Contour swales", "Perennial drought-hardy polycultures", "Dehesa / Montado agroforestry"]
            }
        }

    def resolve_coordinates(self, lat: float, lon: float) -> Dict[str, Any]:
        """
        Infers eco-region and climatic baseline from latitude and longitude.
        """
        # Coordinate classification heuristics
        abs_lat = abs(lat)
        
        # Estimate zone
        if abs_lat < 15:
            # Tropical equatorial / savanna
            koppen = "Aw / Af (Tropical Wet / Savanna)"
            biome = "Tropical Humid & Savanna System"
            rainfall = 1200
            soil_order = "Oxisols / Ultisols"
            vulnerabilities = ["High weathering leaching", "Phosphorus fixation", "Rapid organic matter mineralization"]
            priorities = ["Agroforestry shade canopy", "Legume nitrogen fixation", "Perennial cover"]
        elif 15 <= abs_lat <= 32:
            # Subtropical / arid / semi-arid belt
            if lon > 65 and lon < 90 and lat > 18:
                koppen = "BSh / Cwa (Monsoonal Semi-Arid / Subtropical)"
                biome = "Deccan / Indo-Gangetic Transition"
                rainfall = 650
            else:
                koppen = "BSh / BWh (Semi-Arid to Arid)"
                biome = "Subtropical Dryland / Steppe"
                rainfall = 420
            soil_order = "Vertisols / Inceptisols / Aridisols"
            vulnerabilities = ["Erratic monsoon / precipitation variability", "High surface evaporation", "Wind and water erosion"]
            priorities = ["Conservation tillage & residue retention", "Hydraulic lift agroforestry", "Swales / Keyline design"]
        elif 32 < abs_lat <= 50:
            # Temperate zone
            koppen = "Cfa / Cfb / Dfb (Temperate Marine / Continental)"
            biome = "Temperate Cropland & Forest"
            rainfall = 850
            soil_order = "Mollisols / Alfisols"
            vulnerabilities = ["Nutrient runoff to waterways", "Compaction from tillage", "Habitat fragmentation"]
            priorities = ["Multi-species cover crops", "Riparian buffer strips", "Native hedgerows"]
        else:
            # Boreal / Cold
            koppen = "Dfc / ET (Boreal / Sub-polar)"
            biome = "Boreal / Subarctic"
            rainfall = 500
            soil_order = "Spodosols / Gelisols"
            vulnerabilities = ["Short growing season", "Slow organic decomposition", "Permafrost / frost heave"]
            priorities = ["Cold-hardy perennials", "Biochar thermal moderation", "Soil armor"]

        return {
            "resolved_from": "coordinates",
            "lat": lat,
            "lon": lon,
            "koppen_classification": koppen,
            "biome": biome,
            "estimated_baseline_rainfall_mm": rainfall,
            "dominant_soil_order": soil_order,
            "primary_vulnerabilities": vulnerabilities,
            "ecological_priorities": priorities
        }

    def resolve_region_text(self, text: str) -> Optional[Dict[str, Any]]:
        text_lower = text.lower()
        for region_key, data in self.known_regions.items():
            if any(term in text_lower for term in region_key.split()):
                res = data.copy()
                res["resolved_from"] = f"region_keyword: {region_key}"
                return res
        
        # Check specific geographic tokens
        if any(w in text_lower for w in ["semi-arid", "dryland", "steppe", "arid", "low rainfall"]):
            res = self.known_regions["semi-arid dryland"].copy()
            res["resolved_from"] = "matched_token: semi-arid"
            return res
        if any(w in text_lower for w in ["tropical", "savanna", "cerrado", "pasture", "acidic"]):
            res = self.known_regions["tropical savanna"].copy()
            res["resolved_from"] = "matched_token: tropical"
            return res
        if any(w in text_lower for w in ["riparian", "stream", "river", "runoff", "temperate"]):
            res = self.known_regions["temperate alluvial plain"].copy()
            res["resolved_from"] = "matched_token: riparian"
            return res
        if any(w in text_lower for w in ["saline", "salinity", "sodic", "alkaline", "cotton"]):
            res = self.known_regions["arid irrigated basin"].copy()
            res["resolved_from"] = "matched_token: saline"
            return res
        return None
