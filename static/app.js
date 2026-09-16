// Darukaa.Earth AI Biodiversity Intelligence Frontend Client

let currentSessionId = "session_" + Math.random().toString(36).substring(2, 9);
let benchmarkScenarios = [];

document.addEventListener("DOMContentLoaded", async () => {
  initEventListeners();
  await loadBenchmarkScenarios();
  setupTabNavigation();
  setupParameterSync();
});

function initEventListeners() {
  // Chat form submit
  const chatForm = document.getElementById("chatForm");
  chatForm.addEventListener("submit", handleChatSubmit);

  // Apply parameters button
  document.getElementById("applyParamsBtn").addEventListener("click", handleStructuredSubmit);

  // Geo lookup button
  document.getElementById("geoLookupBtn").addEventListener("click", handleGeoLookup);

  // Reset session
  document.getElementById("resetSessionBtn").addEventListener("click", resetSession);

  // Search Knowledge Modal
  const modal = document.getElementById("knowledgeModal");
  document.getElementById("searchKnowledgeBtn").addEventListener("click", () => {
    modal.classList.remove("hidden");
    searchLiterature("agroforestry soil organic carbon");
  });
  document.getElementById("closeModalBtn").addEventListener("click", () => modal.classList.add("hidden"));
  document.getElementById("modalSearchBtn").addEventListener("click", () => {
    const q = document.getElementById("modalSearchInput").value;
    if (q) searchLiterature(q);
  });
}

function setupTabNavigation() {
  const tabBtns = document.querySelectorAll(".tab-btn");
  tabBtns.forEach(btn => {
    btn.addEventListener("click", () => {
      tabBtns.forEach(b => b.classList.remove("active"));
      document.querySelectorAll(".tab-pane").forEach(p => p.classList.remove("active"));
      
      btn.classList.add("active");
      const targetTab = btn.getAttribute("data-tab");
      const pane = document.getElementById(targetTab);
      if (pane) pane.classList.add("active");
    });
  });
}

function setupParameterSync() {
  const socInput = document.getElementById("socInput");
  const socVal = document.getElementById("socVal");
  socInput.addEventListener("input", (e) => socVal.textContent = `${e.target.value}%`);

  const phInput = document.getElementById("phInput");
  const phVal = document.getElementById("phVal");
  phInput.addEventListener("input", (e) => phVal.textContent = e.target.value);

  const rainInput = document.getElementById("rainInput");
  const rainVal = document.getElementById("rainVal");
  rainInput.addEventListener("input", (e) => rainVal.textContent = `${e.target.value} mm`);
}

async function loadBenchmarkScenarios() {
  try {
    const res = await fetch("/api/scenarios");
    if (res.ok) {
      benchmarkScenarios = await res.json();
      bindScenarioChips();
    }
  } catch (err) {
    console.error("Failed to load scenarios:", err);
  }
}

function bindScenarioChips() {
  const chips = document.querySelectorAll(".chip");
  chips.forEach(chip => {
    chip.addEventListener("click", () => {
      chips.forEach(c => c.classList.remove("active"));
      chip.classList.add("active");
      const scenarioId = chip.getAttribute("data-scenario");
      const scenario = benchmarkScenarios.find(s => s.id === scenarioId);
      if (scenario) {
        // Populate inputs
        document.getElementById("userInput").value = scenario.user_query;
        if (scenario.soil_organic_carbon !== undefined) {
          document.getElementById("socInput").value = scenario.soil_organic_carbon;
          document.getElementById("socVal").textContent = `${scenario.soil_organic_carbon}%`;
        }
        if (scenario.soil_ph !== undefined) {
          document.getElementById("phInput").value = scenario.soil_ph;
          document.getElementById("phVal").textContent = scenario.soil_ph;
        }
        if (scenario.annual_rainfall_mm !== undefined) {
          document.getElementById("rainInput").value = scenario.annual_rainfall_mm;
          document.getElementById("rainVal").textContent = `${scenario.annual_rainfall_mm} mm`;
        }
        if (scenario.land_use) {
          document.getElementById("landUseSelect").value = scenario.land_use;
        }
        if (scenario.coordinates) {
          document.getElementById("latInput").value = scenario.coordinates.lat;
          document.getElementById("lonInput").value = scenario.coordinates.lon;
        }

        // Auto trigger reasoning
        handleChatSubmit(new Event("submit"));
      }
    });
  });
}

async function handleChatSubmit(e) {
  if (e && e.preventDefault) e.preventDefault();
  const inputEl = document.getElementById("userInput");
  const message = inputEl.value.trim();
  if (!message) return;

  // Append user message to chat UI
  appendChatMessage("user", message);
  inputEl.value = "";

  // Prepare structured context from sliders
  const structuredContext = {
    soil_organic_carbon: parseFloat(document.getElementById("socInput").value),
    soil_ph: parseFloat(document.getElementById("phInput").value),
    annual_rainfall_mm: parseFloat(document.getElementById("rainInput").value),
    land_use: document.getElementById("landUseSelect").value
  };

  const lat = parseFloat(document.getElementById("latInput").value);
  const lon = parseFloat(document.getElementById("lonInput").value);
  if (!isNaN(lat) && !isNaN(lon)) {
    structuredContext.coordinates = { lat, lon };
  }

  // Show loading indicator
  const loadingMsgId = appendChatMessage("assistant", "🔬 <em>Analyzing multi-variable causal interactions & querying scientific literature...</em>");

  try {
    const response = await fetch("/api/chat", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        session_id: currentSessionId,
        message: message,
        structured_context: structuredContext
      })
    });

    if (!response.ok) {
      throw new Error(`Server returned status ${response.status}`);
    }

    const data = await response.json();
    removeChatMessage(loadingMsgId);
    
    // Render assistant markdown summary in chat
    appendChatMessage("assistant", formatChatSummary(data));

    // Render deep scientific dashboard
    renderScientificDashboard(data);

    // Handle clarification prompt if needed
    handleClarificationDisplay(data);

  } catch (err) {
    removeChatMessage(loadingMsgId);
    appendChatMessage("assistant", `<span style="color: var(--rose-400)">Error processing request: ${err.message}</span>`);
  }
}

async function handleStructuredSubmit() {
  const structuredContext = {
    soil_organic_carbon: parseFloat(document.getElementById("socInput").value),
    soil_ph: parseFloat(document.getElementById("phInput").value),
    annual_rainfall_mm: parseFloat(document.getElementById("rainInput").value),
    land_use: document.getElementById("landUseSelect").value
  };

  const lat = parseFloat(document.getElementById("latInput").value);
  const lon = parseFloat(document.getElementById("lonInput").value);
  if (!isNaN(lat) && !isNaN(lon)) {
    structuredContext.coordinates = { lat, lon };
  }

  appendChatMessage("user", `⚡ Executing direct multi-metric analysis for: SOC=${structuredContext.soil_organic_carbon}%, pH=${structuredContext.soil_ph}, Rainfall=${structuredContext.annual_rainfall_mm}mm, LandUse=${structuredContext.land_use}`);

  try {
    const response = await fetch("/api/analyze", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(structuredContext)
    });

    if (response.ok) {
      const data = await response.json();
      appendChatMessage("assistant", formatChatSummary(data));
      renderScientificDashboard(data);
      handleClarificationDisplay(data);
    }
  } catch (err) {
    console.error("Analysis failed:", err);
  }
}

async function handleGeoLookup() {
  const lat = parseFloat(document.getElementById("latInput").value);
  const lon = parseFloat(document.getElementById("lonInput").value);
  const badge = document.getElementById("geoResolvedBadge");

  if (isNaN(lat) || isNaN(lon)) {
    alert("Please enter both valid Latitude and Longitude");
    return;
  }

  try {
    const res = await fetch("/api/geo/lookup", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ lat, lon })
    });
    if (res.ok) {
      const geo = await res.json();
      badge.innerHTML = `<strong>Zone:</strong> ${geo.koppen_classification} | <strong>Biome:</strong> ${geo.biome}`;
      badge.classList.remove("hidden");
      if (geo.estimated_baseline_rainfall_mm) {
        document.getElementById("rainInput").value = geo.estimated_baseline_rainfall_mm;
        document.getElementById("rainVal").textContent = `${geo.estimated_baseline_rainfall_mm} mm`;
      }
    }
  } catch (err) {
    console.error("Geo lookup error:", err);
  }
}

function handleClarificationDisplay(data) {
  const box = document.getElementById("clarificationBox");
  const content = document.getElementById("clarificationContent");

  if (data.is_clarification_needed && data.clarification_questions.length > 0) {
    box.classList.remove("hidden");
    content.innerHTML = data.clarification_questions.map(q => `
      <div class="clarification-question">
        <div><strong>${q.question}</strong></div>
        <div style="font-size: 0.73rem; color: var(--text-muted); margin-bottom: 0.2rem;">${q.importance}</div>
        <div class="clarification-options">
          ${(q.suggested_options || []).map(opt => `
            <button class="clarification-opt-btn" onclick="applyClarificationOption('${opt}')">${opt}</button>
          `).join('')}
        </div>
      </div>
    `).join('');
  } else {
    box.classList.add("hidden");
    content.innerHTML = "";
  }
}

window.applyClarificationOption = function(optText) {
  const input = document.getElementById("userInput");
  input.value = `Regarding parameters: ${optText}`;
  handleChatSubmit(new Event("submit"));
};

function renderScientificDashboard(data) {
  // 1. Diagnosis
  document.getElementById("diagnosisText").textContent = data.ecological_diagnosis;
  if (data.scientific_confidence_summary && data.scientific_confidence_summary.overall_scientific_confidence) {
    document.getElementById("confidenceTag").textContent = data.scientific_confidence_summary.overall_scientific_confidence;
  }

  // Geo Details
  const geoBox = document.getElementById("geoDetailsBox");
  if (data.geo_context_resolved) {
    const g = data.geo_context_resolved;
    geoBox.classList.remove("hidden");
    geoBox.innerHTML = `
      <strong>Resolved Climate Zone:</strong> <code>${g.koppen_classification || 'N/A'}</code> | <strong>Biome:</strong> <code>${g.biome || 'N/A'}</code><br>
      <strong>Dominant Soil:</strong> ${g.dominant_soil_order || 'N/A'} | <strong>Key Vulnerability:</strong> ${(g.primary_vulnerabilities || []).join(', ')}
    `;
  } else {
    geoBox.classList.add("hidden");
  }

  // 2. Interactions list
  const interactionList = document.getElementById("interactionList");
  if (data.multi_variable_interactions && data.multi_variable_interactions.length > 0) {
    interactionList.innerHTML = data.multi_variable_interactions.map(item => `<li>${item}</li>`).join('');
  }

  // 3. Quick metrics preview grid
  const previewGrid = document.getElementById("metricsPreviewGrid");
  if (data.projected_metrics && data.projected_metrics.length > 0) {
    previewGrid.innerHTML = data.projected_metrics.slice(0, 4).map(m => `
      <div class="metric-stat-card">
        <span class="metric-stat-title">${m.display_name}</span>
        <span class="metric-stat-val">${m.medium_term_change}</span>
        <span class="metric-stat-sub">Baseline: ${m.baseline_estimate} → 3yr target</span>
      </div>
    `).join('');
  }

  // 4. Causal chain flow
  const causalContainer = document.getElementById("causalChainContainer");
  if (data.causal_chains && data.causal_chains.length > 0) {
    causalContainer.innerHTML = data.causal_chains.map(node => `
      <div class="causal-node-card">
        <div class="causal-node-header">
          <span class="causal-input-badge">Input: ${node.input_variable}</span>
          <span class="causal-bio-badge">Target: ${node.impacted_biodiversity_indicator}</span>
        </div>
        <div class="causal-body-text"><strong>Direct Mechanism:</strong> ${node.direct_mechanism}</div>
        <div class="causal-mech"><strong>Downstream Ecological Impact:</strong> ${node.downstream_impact}</div>
        <div style="font-size: 0.74rem; color: var(--text-muted);"><strong>Scientific Rationale:</strong> ${node.scientific_rationale}</div>
      </div>
    `).join('');
  }

  // 5. Interventions list
  const interventionsContainer = document.getElementById("interventionsContainer");
  if (data.interventions && data.interventions.length > 0) {
    interventionsContainer.innerHTML = data.interventions.map((item, idx) => `
      <div class="intervention-card">
        <div class="intervention-title-row">
          <div class="intervention-title">${idx + 1}. ${item.title}</div>
          <span class="intervention-cat">${item.category}</span>
        </div>
        <div class="intervention-block"><strong>What to do:</strong> ${item.what_to_do}</div>
        <div class="intervention-block"><strong>Why it works (Biophysical Mechanism):</strong> ${item.why_it_works}</div>
        <div class="metric-pills">
          ${item.impacted_metrics.map(m => `<span class="metric-pill">✓ ${m}</span>`).join('')}
        </div>
        <div class="intervention-block" style="font-size: 0.75rem; color: var(--text-secondary); margin-top: 0.3rem;">
          <strong>Time Horizon:</strong> <code>${item.time_horizon}</code> | <strong>Risk Mitigation:</strong> ${item.risks_and_mitigations}
        </div>
        <div style="font-size: 0.75rem; color: var(--emerald-900); font-weight: 600; margin-top: 0.3rem;">
          <strong>Evidence Basis:</strong> ${item.confidence_rating}
        </div>
      </div>
    `).join('');
  }

  // 6. Projections Table
  const tbody = document.getElementById("projectionsTbody");
  if (data.projected_metrics && data.projected_metrics.length > 0) {
    tbody.innerHTML = data.projected_metrics.map(m => `
      <tr>
        <td><strong>${m.display_name}</strong></td>
        <td><span class="badge badge-success">${m.category}</span></td>
        <td><code>${m.baseline_estimate}</code></td>
        <td style="color: #0284c7; font-weight: 700;">${m.short_term_change}</td>
        <td style="color: var(--emerald-700); font-weight: 700;">${m.medium_term_change}</td>
        <td style="color: #4f46e5; font-weight: 700;">${m.long_term_change}</td>
        <td style="font-size: 0.76rem; color: var(--text-dark);">${m.scientific_basis}</td>
      </tr>
    `).join('');
  }

  // 7. Citations list
  const citationsContainer = document.getElementById("citationsContainer");
  if (data.citations && data.citations.length > 0) {
    citationsContainer.innerHTML = data.citations.map(c => `
      <div class="citation-card">
        <div class="citation-header">
          <span class="citation-id">${c.id}</span>
          <span class="badge badge-success">Relevance: ${Math.round(c.relevance_score * 100)}%</span>
        </div>
        <div class="citation-title">${c.title} (${c.year})</div>
        <div class="citation-meta">${c.authors} — <em>${c.publisher}</em></div>
        <div class="citation-finding">${c.relevant_finding}</div>
        <a href="${c.doi_or_url}" target="_blank" rel="noopener noreferrer" class="citation-link">
          🔗 Open DOI / Institutional Report Reference &rarr;
        </a>
      </div>
    `).join('');
  }
}

async function searchLiterature(query) {
  const container = document.getElementById("modalSearchResults");
  container.innerHTML = "<em>Searching 16+ indexed peer-reviewed studies...</em>";
  try {
    const res = await fetch(`/api/knowledge/search?q=${encodeURIComponent(query)}&top_k=5`);
    if (res.ok) {
      const data = await res.json();
      if (data.results.length === 0) {
        container.innerHTML = "No matching research studies found for that query.";
        return;
      }
      container.innerHTML = data.results.map(c => `
        <div class="citation-card">
          <div class="citation-header">
            <span class="citation-id">${c.id}</span>
            <span class="badge badge-accent">Match Score: ${c.relevance_score}</span>
          </div>
          <div class="citation-title">${c.title} (${c.year})</div>
          <div class="citation-meta">${c.authors} — ${c.publisher}</div>
          <div class="citation-finding">${c.relevant_finding}</div>
          <a href="${c.doi_or_url}" target="_blank" rel="noopener noreferrer" class="citation-link">
            Open Publication &rarr;
          </a>
        </div>
      `).join('');
    }
  } catch (err) {
    container.innerHTML = `Error searching literature: ${err.message}`;
  }
}

function formatChatSummary(data) {
  let html = `<p><strong>${data.ecological_diagnosis}</strong></p>`;
  if (data.interventions && data.interventions.length > 0) {
    html += `<p style="margin-top:0.4rem;"><strong>Recommended Scientific Interventions:</strong></p><ul style="padding-left:1.2rem; margin-top:0.2rem;">`;
    data.interventions.forEach(item => {
      html += `<li><strong>${item.title}:</strong> ${item.impacted_metrics.slice(0, 2).join(', ')}</li>`;
    });
    html += `</ul>`;
  }
  html += `<p style="font-size:0.8rem; color:var(--emerald-800); font-weight: 600; margin-top:0.4rem;">📊 <em>Full multi-metric causal graphs, quantitative 10-year projections, and FAO/IPCC citations populated in the right scientific workbench.</em></p>`;
  return html;
}

function appendChatMessage(role, content) {
  const container = document.getElementById("chatMessages");
  const msgId = "msg_" + Math.random().toString(36).substring(2, 9);
  const div = document.createElement("div");
  div.className = `message ${role}-msg`;
  div.id = msgId;

  const avatar = role === "user" ? "🧑‍🌾" : (role === "assistant" ? "🌱" : "ℹ️");
  div.innerHTML = `
    <div class="msg-avatar">${avatar}</div>
    <div class="msg-body">${content}</div>
  `;
  container.appendChild(div);
  container.scrollTop = container.scrollHeight;
  return msgId;
}

function removeChatMessage(id) {
  const el = document.getElementById(id);
  if (el) el.remove();
}

function resetSession() {
  currentSessionId = "session_" + Math.random().toString(36).substring(2, 9);
  const container = document.getElementById("chatMessages");
  container.innerHTML = `
    <div class="message system-msg">
      <div class="msg-avatar">🌱</div>
      <div class="msg-body">
        <strong>New session initialized (${currentSessionId}).</strong>
        <p>Conversational memory reset. Provide ecosystem variables to run fresh multi-metric diagnosis.</p>
      </div>
    </div>
  `;
  document.getElementById("clarificationBox").classList.add("hidden");
}
