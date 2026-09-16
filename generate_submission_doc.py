import docx
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT, WD_ALIGN_VERTICAL
from docx.oxml import OxmlElement
from docx.oxml.ns import qn
import os

def set_cell_background(cell, fill_hex):
    tcPr = cell._tc.get_or_add_tcPr()
    shd = OxmlElement('w:shd')
    shd.set(qn('w:val'), 'clear')
    shd.set(qn('w:color'), 'auto')
    shd.set(qn('w:fill'), fill_hex)
    tcPr.append(shd)

def create_submission_doc():
    doc = docx.Document()

    # Document Title
    title = doc.add_paragraph()
    title_run = title.add_run("Darukaa.Earth: AI Biodiversity Intelligence Chatbot Challenge")
    title_run.font.size = Pt(22)
    title_run.font.bold = True
    title_run.font.color.rgb = RGBColor(16, 185, 129) # Emerald
    title.alignment = WD_ALIGN_PARAGRAPH.CENTER

    subtitle = doc.add_paragraph()
    sub_run = subtitle.add_run("Technical Submission & Architecture Blueprint")
    sub_run.font.size = Pt(13)
    sub_run.font.italic = True
    sub_run.font.color.rgb = RGBColor(100, 116, 139)
    subtitle.alignment = WD_ALIGN_PARAGRAPH.CENTER

    doc.add_paragraph()

    # 1. Project Links & Metadata Table
    h1 = doc.add_heading("1. Submission Links & Project Metadata", level=1)
    
    meta_table = doc.add_table(rows=5, cols=2)
    meta_table.alignment = WD_TABLE_ALIGNMENT.CENTER
    meta_data = [
        ("Project Name", "Darukaa.Earth AI Biodiversity Intelligence & Ecological Reasoning System"),
        ("GitHub Repository Link", "https://github.com/SaachiSawant/darukaaAI"),
        ("Live Web Application URL", "http://127.0.0.1:8000 (FastAPI Interactive Glassmorphic Scientific Dashboard)"),
        ("Invited Reviewer Accounts", "ankita.dasgupta@darukaa.com, harsh.kumar@darukaa.com, utkarsh.gauniyal@darukaa.com, guneet.mutreja@darukaa.com"),
        ("Core Technology Stack", "Python 3.14, FastAPI, Scikit-learn (Hybrid TF-IDF & Vector RAG), Pydantic v2, HTML5/CSS3/Vanilla JS")
    ]
    for row_idx, (k, v) in enumerate(meta_data):
        row = meta_table.rows[row_idx]
        row.cells[0].paragraphs[0].add_run(k).font.bold = True
        row.cells[1].paragraphs[0].add_run(v)
        set_cell_background(row.cells[0], "F1F5F9")
        set_cell_background(row.cells[1], "FFFFFF")

    doc.add_paragraph()

    # 2. Executive Summary & Problem Solving Approach
    doc.add_heading("2. System Design & Scientific Reasoning Philosophy", level=1)
    doc.add_paragraph(
        "Darukaa.Earth is engineered not as a generic LLM wrapper or simple prompt chatbot, but as an "
        "AI Environmental Scientist. It couples retrievable peer-reviewed scientific literature (FAO, IPCC AR6, IPBES, Nature/Science) "
        "with a mechanistic Multi-Metric Ecological Causal Engine that dynamically models biophysical feedback loops across at least "
        "3 to 5 environmental variables simultaneously."
    )

    doc.add_heading("Core Scientific Differentiators:", level=2)
    p = doc.add_paragraph()
    p.add_run("• Multi-Metric Coupled Reasoning: ").bold = True
    p.add_run("Connects Soil Health (SOC%, pH, bulk density, AMF colonization) ↔ Climatic Regime (Rainfall, ET deficit) ↔ Land-Use Disturbance (monoculture vs. polyculture) ↔ Biodiversity Indicators (microbiome multifunctionality, pollinator richness, trophic web resilience).\n")
    p.add_run("• Grounded Hybrid RAG Knowledge Layer: ").bold = True
    p.add_run("Indexes 16+ curated peer-reviewed studies and global institutional assessments with exact DOI attributions, quantitative metric links, and biophysical mechanism descriptions.\n")
    p.add_run("• Conversational Intelligence & Ambiguity Detection: ").bold = True
    p.add_run("Detects missing parameters in user inputs and asks targeted clarifying questions before or while synthesizing precise recommendations.\n")
    p.add_run("• Quantified Time-Horizon Projections: ").bold = True
    p.add_run("Calculates short-term (0–1 yr), medium-term (2–4 yrs), and long-term (5–10 yrs) improvement ranges with risk/trade-off mitigation strategies.")

    # 3. Architecture & Data Schema
    doc.add_heading("3. Technical Architecture & Database Schema", level=1)
    doc.add_paragraph(
        "The system is organized into modular components adhering to clean architecture principles:"
    )

    arch_table = doc.add_table(rows=6, cols=3)
    arch_table.alignment = WD_TABLE_ALIGNMENT.CENTER
    headers = ["Component", "File Path", "Functional Responsibility"]
    for i, h in enumerate(headers):
        cell = arch_table.rows[0].cells[i]
        cell.paragraphs[0].add_run(h).font.bold = True
        set_cell_background(cell, "E2E8F0")

    arch_rows = [
        ("Hybrid RAG Knowledge Engine", "src/knowledge_engine.py", "Vector + TF-IDF cosine similarity search across indexed peer-reviewed studies (FAO, IPCC, Nature) with DOI citation ranking."),
        ("Multi-Metric Causal Engine", "src/causal_engine.py", "Models biophysical causal chains connecting inputs -> direct mechanisms -> downstream multi-metric biodiversity outcomes."),
        ("Conversational Memory & Clarification", "src/conversation_engine.py", "Stateful multi-turn session tracking, ambiguity/missing variable detection, and structured markdown report synthesis."),
        ("Geo-Spatial Context Resolver", "src/geo_engine.py", "Resolves Lat/Lon coordinates and regional descriptions to Köppen-Geiger climate classification, biomes, and soil baselines."),
        ("FastAPI REST Service & Dashboard", "main.py & static/", "Exposes /api/chat, /api/analyze, /api/knowledge/search, /api/scenarios and serves the glassmorphic environmental UI.")
    ]
    for row_idx, r in enumerate(arch_rows, 1):
        row = arch_table.rows[row_idx]
        for col_idx, text in enumerate(r):
            row.cells[col_idx].paragraphs[0].add_run(text)
            set_cell_background(row.cells[col_idx], "F8FAFC" if row_idx % 2 == 0 else "FFFFFF")

    doc.add_paragraph()

    # 4. Benchmark Scenario Verification (Semi-Arid Wheat Monoculture)
    doc.add_heading("4. Evaluation Benchmark: Semi-Arid Monoculture Wheat", level=1)
    doc.add_paragraph(
        "Input: Soil Organic Carbon = 0.3%, Rainfall = Low (380mm), Crop = Monoculture Wheat, Region = Semi-Arid.\n"
        "System Output Summary:"
    )

    scen_table = doc.add_table(rows=4, cols=3)
    scen_table.alignment = WD_TABLE_ALIGNMENT.CENTER
    s_headers = ["Intervention", "Why It Works (Biophysical Mechanism)", "Quantified Impact & Time Horizon"]
    for i, h in enumerate(s_headers):
        cell = scen_table.rows[0].cells[i]
        cell.paragraphs[0].add_run(h).font.bold = True
        set_cell_background(cell, "E2E8F0")

    scen_rows = [
        ("Multi-Species Legume-Brassica Cover Cropping", "Root exudation feeds arbuscular mycorrhizal fungi (AMF). Residue mulch reduces soil surface evaporation by 30-45% and topsoil heat by 4-6°C.", "SOC +15-25% in 3 yrs; AMF colonization +35-50%; infiltration +40-70% (FAO 2020)."),
        ("Contour Alley Agroforestry (Faidherbia albida)", "Deep tree roots conduct nocturnal hydraulic lift, redistributing moisture to upper crop rhizosphere; windbreak reduces crop ET stress.", "Available Water Capacity +18-30%; Bird/predator richness +200-350%; Drought risk -40% (IPCC 2019)."),
        ("Activated Biochar-Compost Co-Amendment", "Aromatic carbon micro-caves protect soil microbiome from desiccation; increases Cation Exchange Capacity (CEC).", "CEC +25-40%; SOC sequestration +0.4-0.9 t C/ha/yr stable (Paustian et al. Nature 2016).")
    ]
    for row_idx, r in enumerate(scen_rows, 1):
        row = scen_table.rows[row_idx]
        for col_idx, text in enumerate(r):
            row.cells[col_idx].paragraphs[0].add_run(text)
            set_cell_background(row.cells[col_idx], "F8FAFC" if row_idx % 2 == 0 else "FFFFFF")

    doc.add_paragraph()

    # 5. Local Setup & CI/CD
    doc.add_heading("5. Local Setup, Execution & Testing", level=1)
    doc.add_paragraph(
        "1. Install dependencies: pip install -r requirements.txt\n"
        "2. Run automated test suite: python run_tests.py\n"
        "3. Start interactive application server: python main.py (or uvicorn main:app --reload)\n"
        "4. Open browser: http://127.0.0.1:8000"
    )

    doc_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "Darukaa_AI_Biodiversity_Intelligence_Submission.docx")
    doc.save(doc_path)
    print(f"Successfully generated submission document: {doc_path}")

if __name__ == "__main__":
    create_submission_doc()
