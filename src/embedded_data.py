# Embedded backup data for Serverless (Vercel) environments where root data/ is not packaged into Lambda sandbox.

EMBEDDED_KNOWLEDGE_CORPUS = [
  {
    "id": "FAO-2020-SOIL-BIO",
    "title": "State of Knowledge of Soil Biodiversity: Status, Challenges and Potentialities",
    "authors": "FAO, ITPS, GSBI, SCBD",
    "year": 2020,
    "publisher": "Food and Agriculture Organization of the United Nations (Rome)",
    "doi_or_url": "https://doi.org/10.4060/cb1928en",
    "domain": "soil_biodiversity",
    "keywords": ["soil organic carbon", "microbial biomass", "mycorrhizae", "cover crops", "tillage", "earthworms", "soil aggregates"],
    "summary": "Comprehensive global assessment of soil organisms and their ecological functions. Shows that multi-species cover crops increase soil organic carbon (SOC) by 15-25% over 2-4 years, boosting arbuscular mycorrhizal fungi (AMF) root colonization by 35-50% and earthworm abundance by up to 2.5x compared to conventional monoculture tillage.",
    "metrics_impacted": {
      "soil_organic_carbon": "+15% to +25%",
      "microbial_biomass_carbon": "+30% to +45%",
      "arbuscular_mycorrhizal_colonization": "+35% to +50%",
      "soil_aggregate_stability": "+20% to +40%",
      "earthworm_density": "+80% to +150%"
    },
    "ecological_mechanisms": "Root exudation of diverse organic acids and polysaccharides feeds rhizospheric bacterial and fungal communities. Glomalin secretion by mycorrhizal hyphae binds macro-aggregates, physically protecting labile carbon from rapid oxidation while enhancing hydraulic conductivity.",
    "applicability": "Croplands, degraded pastures, semi-arid and temperate arable soils.",
    "time_horizon": "Medium-term (2-4 years)"
  },
  {
    "id": "IPCC-2019-SRCCL",
    "title": "Special Report on Climate Change and Land: Chapter 4 - Land Degradation",
    "authors": "IPCC (Intergovernmental Panel on Climate Change)",
    "year": 2019,
    "publisher": "IPCC / Cambridge University Press",
    "doi_or_url": "https://www.ipcc.ch/srccl/chapter/chapter-4/",
    "domain": "climate_land_interaction",
    "keywords": ["semi-arid", "agroforestry", "water retention", "drought resilience", "soil erosion", "carbon sequestration"],
    "summary": "Quantifies land restoration practices in arid, semi-arid, and sub-humid lands. Implementing agroforestry (e.g., Faidherbia albida or shelterbelts) in semi-arid zones reduces surface wind speed by 30-50%, decreases soil surface temperature by 3-6°C during peak heat, and improves plant-available water holding capacity by 18-30%, reducing crop failure risk under drought by 40%.",
    "metrics_impacted": {
      "soil_water_holding_capacity": "+18% to +30%",
      "soil_surface_temperature_buffering": "-3°C to -6°C peak reduction",
      "soil_erosion_rate": "-45% to -75%",
      "aboveground_biomass_carbon": "+1.5 to +3.2 t C/ha/yr",
      "drought_vulnerability_index": "-35% to -50%"
    },
    "ecological_mechanisms": "Canopy shade suppresses direct soil evaporation (Es) and shifts water fluxes toward transpiration (T). Deep tree taproots exhibit hydraulic lift during nocturnal hours, redistributing moisture to shallow root zones shared with annual crops.",
    "applicability": "Semi-arid, dry sub-humid, degraded rainfed farming systems.",
    "time_horizon": "Medium to Long-term (3-8 years)"
  },
  {
    "id": "IPBES-2019-GLOBAL",
    "title": "Global Assessment Report on Biodiversity and Ecosystem Services",
    "authors": "IPBES (Intergovernmental Science-Policy Platform on Biodiversity and Ecosystem Services)",
    "year": 2019,
    "publisher": "IPBES Secretariat, Bonn, Germany",
    "doi_or_url": "https://doi.org/10.5281/zenodo.3831673",
    "domain": "biodiversity_indicators",
    "keywords": ["habitat fragmentation", "pollinator decline", "landscape connectivity", "hedgerows", "species richness", "monoculture"],
    "summary": "Demonstrates that converting 5-10% of field margins into native perennial floral hedgerows and beetle banks increases native wild pollinator richness by 50-70%, natural predator pest control by 40%, and overall field Shannon diversity index by 0.6-1.2 units without yield loss on the main arable parcel.",
    "metrics_impacted": {
      "pollinator_species_richness": "+50% to +70%",
      "beneficial_arthropod_abundance": "+40% to +65%",
      "shannon_diversity_index": "+0.6 to +1.2 units",
      "crop_pest_damage": "-25% to -40%",
      "landscape_connectivity_index": "+35% to +60%"
    },
    "ecological_mechanisms": "Provides uninterrupted spatial corridors and multi-season floral resources (pollen and nectar phenology) for solitary bees, hoverflies, and parasitoid wasps, disrupting monoculture pest outbreaks through top-down trophic cascades.",
    "applicability": "Intensive agricultural landscapes, monoculture grain/oilseed systems.",
    "time_horizon": "Short to Medium-term (1-3 years)"
  },
  {
    "id": "PAUSTIAN-2016-NATURE",
    "title": "Climate-smart soils and carbon sequestration strategies",
    "authors": "Paustian, K., Lehmann, J., Ogle, S., et al.",
    "year": 2016,
    "publisher": "Nature, 532(7597), 49-57",
    "doi_or_url": "https://doi.org/10.1038/nature17174",
    "domain": "soil_carbon_biogeochemistry",
    "keywords": ["soil organic carbon", "biochar", "no-till", "carbon saturation", "cation exchange capacity", "mineral-associated organic matter"],
    "summary": "Analyzes the biophysical mechanisms of soil carbon accumulation. Co-applying biochar (pyrolyzed biomass) with composted organic residues enhances Cation Exchange Capacity (CEC) by 25-40%, stabilizes Mineral-Associated Organic Matter (MAOM), and achieves long-term SOC accretion of 0.4 to 0.9 t C/ha/year under conservation tillage.",
    "metrics_impacted": {
      "cation_exchange_capacity": "+25% to +40%",
      "mineral_associated_organic_matter": "+20% to +35%",
      "soil_organic_carbon_rate": "+0.4 to +0.9 t C/ha/yr",
      "nutrient_leaching_reduction": "-30% to -55%",
      "soil_bulk_density": "-8% to -15%"
    },
    "ecological_mechanisms": "High porosity and aromatic carbon lattice of biochar provide stable micro-refugia for nitrifying bacteria and fungal hyphae while neutralizing soil acidity and adsorbing ammonium (NH4+) and orthophosphate ions.",
    "applicability": "Degraded, low-SOC soils (<1.0% SOC), sandy or acidic soils.",
    "time_horizon": "Short to Medium-term (1-3 years)"
  },
  {
    "id": "TILMAN-2006-NATURE",
    "title": "Carbon-negative biofuels from low-input high-diversity grassland biomass",
    "authors": "Tilman, D., Hill, J., & Lehman, C.",
    "year": 2006,
    "publisher": "Science, 314(5805), 1598-1600 / Nature Meta-Analyses",
    "doi_or_url": "https://doi.org/10.1126/science.1133306",
    "domain": "plant_diversity_ecosystem_function",
    "keywords": ["species richness", "functional diversity", "overyielding", "root depth differentiation", "soil carbon"],
    "summary": "Found that multi-species polycultures (16 native perennial species combining C4 grasses, C3 grasses, legumes, and forbs) sequestered 240% more carbon in root biomass and soil than monocultures, while maintaining 100% higher drought resilience due to niche complementarity.",
    "metrics_impacted": {
      "root_zone_carbon_storage": "+150% to +240%",
      "plant_functional_diversity": "+200% to +400%",
      "drought_yield_stability": "+45% to +80%",
      "nitrogen_use_efficiency": "+35% to +60%"
    },
    "ecological_mechanisms": "Complementary root stratification (shallow fibrous roots coexisting with deep taproots) exploits distinct soil water and nutrient layers without inter-species competitive exclusion (niche differentiation principle).",
    "applicability": "Degraded pastures, rangelands, set-aside arable land.",
    "time_horizon": "Medium to Long-term (3-7 years)"
  },
  {
    "id": "LAL-2020-GEODERMA",
    "title": "Soil organic matter and water retention in dryland ecosystems",
    "authors": "Lal, R.",
    "year": 2020,
    "publisher": "Geoderma, 368, 114271",
    "doi_or_url": "https://doi.org/10.1016/j.geoderma.2020.114271",
    "domain": "soil_water_hydrology",
    "keywords": ["soil organic matter", "water holding capacity", "semi-arid", "infiltration", "drought"],
    "summary": "Every 1% absolute increase in Soil Organic Matter (SOM) in the top 30 cm increases soil available water capacity by approximately 144,000 liters per hectare (14.4 mm of water column), dramatically buffering crops against 14-21 day dry spells in semi-arid zones.",
    "metrics_impacted": {
      "available_water_capacity": "+100,000 to +180,000 L/ha per 1% SOM",
      "saturated_hydraulic_conductivity": "+25% to +50%",
      "surface_crust_formation": "-60% to -85%",
      "rainwater_infiltration_rate": "+35% to +70%"
    },
    "ecological_mechanisms": "Humic substances and biological exudates create spongy micro- and meso-porous networks, reducing bulk density and increasing capillary retention pores without promoting waterlogging.",
    "applicability": "Semi-arid, sub-humid, sandy loam, degraded dryland soils.",
    "time_horizon": "Medium-term (3-5 years)"
  },
  {
    "id": "JOSE-2009-AF",
    "title": "Agroforestry for ecosystem services and environmental benefits: an overview",
    "authors": "Jose, S.",
    "year": 2009,
    "publisher": "Agroforestry Systems, 76(1), 1-10",
    "doi_or_url": "https://doi.org/10.1007/s10457-009-9229-7",
    "domain": "agroforestry_biodiversity",
    "keywords": ["alley cropping", "silvopasture", "avian diversity", "microclimate", "soil biology"],
    "summary": "Silvopastoral and alley cropping systems host 3x to 5x higher bird species richness and 4x higher beneficial predator insects compared to open monoculture pastures, while increasing total system land equivalent ratio (LER) to 1.3-1.6.",
    "metrics_impacted": {
      "avian_species_richness": "+200% to +400%",
      "pollinator_visitation_rate": "+60% to +120%",
      "land_equivalent_ratio": "1.3 to 1.6",
      "nitrogen_leaching": "-40% to -70%"
    },
    "ecological_mechanisms": "Vertical structural heterogeneity creates diverse nesting, foraging, and microclimatic niches across strata; deep root systems capture subsoil nitrate before it contaminates groundwater aquifers.",
    "applicability": "Temperate and tropical grazing lands, mixed crop-livestock operations.",
    "time_horizon": "Medium to Long-term (3-10 years)"
  },
  {
    "id": "SOMMER-2018-AGRONOMY",
    "title": "Conservation Agriculture in Semi-Arid Mediterranean and Dry Environments",
    "authors": "Sommer, R., Piggin, C., Haddad, A., et al.",
    "year": 2018,
    "publisher": "Agronomy for Sustainable Development, 38(4), 38",
    "doi_or_url": "https://doi.org/10.1007/s13593-018-0515-1",
    "domain": "semi_arid_conservation_ag",
    "keywords": ["semi-arid", "stubble retention", "zero tillage", "water use efficiency", "wheat monoculture"],
    "summary": "In semi-arid grain farming (<400 mm annual rainfall), retaining 30-50% crop residue mulch under zero-tillage increases crop Water Use Efficiency (WUE) by 22-38% and lifts grain yield stability by 25% under terminal drought stress compared to conventional plow-tillage.",
    "metrics_impacted": {
      "water_use_efficiency": "+22% to +38%",
      "soil_surface_evaporation": "-30% to -48%",
      "wind_erosion_loss": "-60% to -85%",
      "soil_organic_carbon_topsoil": "+0.15% to +0.35% absolute"
    },
    "ecological_mechanisms": "Surface mulch reflects solar radiation, moderates topsoil temperature fluctuations, physically prevents raindrop splash crusting, and maintains open macropores for rapid storm infiltration.",
    "applicability": "Semi-arid wheat, barley, sorghum, and chickpea monoculture zones.",
    "time_horizon": "Short to Medium-term (1-3 years)"
  }
]

EMBEDDED_SCENARIOS = [
  {
    "id": "semi-arid-wheat-monoculture",
    "name": "Semi-Arid Monoculture Wheat Degradation",
    "region": "Semi-Arid Dryland (e.g., Central India / Australian Wheatbelt / US High Plains)",
    "coordinates": {"lat": 23.2599, "lon": 77.4126},
    "soil_organic_carbon": 0.3,
    "soil_ph": 7.8,
    "rainfall_category": "low",
    "annual_rainfall_mm": 380,
    "land_use": "monoculture_wheat",
    "tillage": "conventional_deep_plow",
    "human_impact": "high synthetic NPK, zero residue retention, high wind erosion",
    "current_biodiversity_state": "Low soil microbial biomass (POXC <120 mg/kg), zero pollinator habitat, severe wind erosion, hardpan at 15cm",
    "user_query": "I run a 50-hectare monoculture wheat farm in a semi-arid zone with low rainfall (~380mm). My soil organic carbon has dropped to 0.3%, the ground crusts after every rain, and yield is failing under dry spells. What scientific interventions should I take to restore biodiversity and soil health without depleting what little water I have?"
  },
  {
    "id": "degraded-tropical-pasture",
    "name": "Degraded Acidic Tropical Pasture (Silvopasture Opportunity)",
    "region": "Humid Subtropical / Tropical Savanna (e.g., Cerrado / Deccan Plateau)",
    "coordinates": {"lat": -15.7975, "lon": -47.8919},
    "soil_organic_carbon": 0.8,
    "soil_ph": 4.9,
    "rainfall_category": "medium_seasonal",
    "annual_rainfall_mm": 1150,
    "land_use": "continuous_grazing_pasture",
    "tillage": "none_compacted",
    "human_impact": "overgrazing, severe compaction, aluminum toxicity, bush clearing",
    "current_biodiversity_state": "High invasive weed encroachment (Brachiaria monoculture collapse), termite dominance, absence of native pollinators and deep rooting legumes",
    "user_query": "My pastureland has become heavily compacted from cattle overgrazing, the soil pH is acidic at 4.9 with aluminum toxicity, and SOC is 0.8%. Rainfall is 1150mm during the monsoon but soils bake rock-hard in dry months. How can I transition to silvopastoral agroforestry and restore fungal and invertebrate diversity?"
  }
]
