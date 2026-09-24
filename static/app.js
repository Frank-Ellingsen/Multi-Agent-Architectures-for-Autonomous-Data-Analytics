const state = {
  files: [],
  dataset: {},
  metrics: {},
  prognosis: {},
  prescriptions: [],
  skills: [],
  config: {
    provider: 'gemini',
    apiKey: '',
    model: 'gemini-1.5-flash',
    endpoint: 'http://localhost:11434',
  },
};

const DEFAULT_MODELS = {
  gemini: 'gemini-1.5-flash',
  openai: 'gpt-4o-mini',
  anthropic: 'claude-3-5-sonnet-20241022',
  ollama: 'llama3.2',
};

// Elements
const tabs = document.querySelectorAll('.tab');
const csvInput = document.getElementById('csvFiles');
const runBtn = document.getElementById('runDiagnosticsBtn');
const loadDemoBtn = document.getElementById('loadDemoBtn');
const datasetSummary = document.getElementById('datasetSummary');
const schemaReport = document.getElementById('schemaReport');
const diagnosticsReport = document.getElementById('diagnosticsReport');
const prognosticsTable = document.getElementById('prognosticsTable');
const prescriptionsList = document.getElementById('prescriptionsList');
const aiStoryOutput = document.getElementById('aiStoryOutput');
const generateStoryBtn = document.getElementById('generateStoryBtn');
const storyStatus = document.getElementById('storyStatus');
const skillsList = document.getElementById('skillsList');
const skillSearchInput = document.getElementById('skillSearchInput');

// Metric elements
const metricActual = document.getElementById('metricActual');
const metricBudget = document.getElementById('metricBudget');
const metricForecast = document.getElementById('metricForecast');
const metricVarBudget = document.getElementById('metricVarBudget');
const metricVarForecast = document.getElementById('metricVarForecast');
const metricFTE = document.getElementById('metricFTE');
const globalStatusDot = document.getElementById('globalStatusDot');
const globalStatusText = document.getElementById('globalStatusText');
const sidebarKeyStatus = document.getElementById('sidebarKeyStatus');

// Config Elements
const llmProviderSelect = document.getElementById('llmProvider');
const apiKeyInput = document.getElementById('apiKey');
const llmModelInput = document.getElementById('llmModel');
const llmEndpointInput = document.getElementById('llmEndpoint');
const endpointGroup = document.getElementById('endpointGroup');
const apiKeyGroup = document.getElementById('apiKeyGroup');
const testConnectionBtn = document.getElementById('testConnectionBtn');
const saveKeyBtn = document.getElementById('saveKeyBtn');
const clearKeyBtn = document.getElementById('clearKeyBtn');
const toggleKeyBtn = document.getElementById('toggleKeyVisibility');
const connectionBadge = document.getElementById('connectionBadge');
const configFeedback = document.getElementById('configFeedback');

const apiBase =
  window.location.protocol === 'file:' || (window.location.port !== '8000' && window.location.port !== '')
    ? 'http://127.0.0.1:8000'
    : '';

// --- Navigation Tabs ---
tabs.forEach((tab) => {
  tab.addEventListener('click', () => {
    tabs.forEach((btn) => btn.classList.remove('active'));
    tab.classList.add('active');
    document.querySelectorAll('.panel').forEach((panel) => {
      panel.classList.toggle('active', panel.id === tab.dataset.target);
    });
  });
});

// --- Settings & API Keys Management ---
const loadSavedConfig = () => {
  try {
    const saved = localStorage.getItem('multi_agent_analytics_config');
    if (saved) {
      const parsed = JSON.parse(saved);
      state.config = { ...state.config, ...parsed };
      llmProviderSelect.value = state.config.provider || 'gemini';
      apiKeyInput.value = state.config.apiKey || '';
      llmModelInput.value = state.config.model || DEFAULT_MODELS[state.config.provider] || 'gemini-1.5-flash';
      llmEndpointInput.value = state.config.endpoint || 'http://localhost:11434';
      updateConfigUI();
    }
  } catch (e) {
    console.warn('Failed to load saved config from localStorage', e);
  }
};

const saveConfig = () => {
  state.config.provider = llmProviderSelect.value;
  state.config.apiKey = apiKeyInput.value.trim();
  state.config.model = llmModelInput.value.trim();
  state.config.endpoint = llmEndpointInput.value.trim();

  try {
    localStorage.setItem('multi_agent_analytics_config', JSON.stringify(state.config));
    configFeedback.textContent = 'Settings saved locally.';
    setTimeout(() => { configFeedback.textContent = ''; }, 3000);
  } catch (e) {
    configFeedback.textContent = 'Failed to save to localStorage.';
  }
  updateConfigUI();
};

const clearConfig = () => {
  apiKeyInput.value = '';
  state.config.apiKey = '';
  try {
    localStorage.removeItem('multi_agent_analytics_config');
    configFeedback.textContent = 'Saved key cleared.';
    setTimeout(() => { configFeedback.textContent = ''; }, 3000);
  } catch (e) {
    console.error(e);
  }
  updateConfigUI();
};

const updateConfigUI = () => {
  const provider = llmProviderSelect.value;
  const isOllama = provider === 'ollama';

  endpointGroup.style.display = isOllama ? 'flex' : 'none';
  apiKeyGroup.style.opacity = isOllama ? '0.5' : '1';

  const hasKey = Boolean(apiKeyInput.value.trim()) || isOllama;
  if (hasKey) {
    sidebarKeyStatus.textContent = isOllama ? 'Ollama: Ready' : `${provider.toUpperCase()}: Configured`;
    sidebarKeyStatus.classList.add('configured');
  } else {
    sidebarKeyStatus.textContent = 'API Key: Not Set';
    sidebarKeyStatus.classList.remove('configured');
  }
};

llmProviderSelect.addEventListener('change', () => {
  const provider = llmProviderSelect.value;
  llmModelInput.value = DEFAULT_MODELS[provider] || 'gemini-2.5-flash';
  updateConfigUI();
});

apiKeyInput.addEventListener('input', updateConfigUI);

toggleKeyBtn.addEventListener('click', () => {
  const isPassword = apiKeyInput.type === 'password';
  apiKeyInput.type = isPassword ? 'text' : 'password';
  toggleKeyBtn.textContent = isPassword ? 'Hide' : 'Show';
});

saveKeyBtn.addEventListener('click', saveConfig);
clearKeyBtn.addEventListener('click', clearConfig);

testConnectionBtn.addEventListener('click', async () => {
  saveConfig();
  connectionBadge.className = 'badge warning';
  connectionBadge.textContent = 'Status: Testing...';
  configFeedback.textContent = 'Checking connectivity...';

  try {
    const res = await fetch(`${apiBase}/api/ai/test-key`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        provider: state.config.provider,
        api_key: state.config.apiKey,
        model: state.config.model,
        base_url: state.config.endpoint,
      }),
    });

    const data = await res.json();
    if (res.ok && data.ok) {
      connectionBadge.className = 'badge connected';
      connectionBadge.textContent = `Status: Connected (${data.model})`;
      configFeedback.textContent = data.message || 'Connection verified!';
    } else {
      connectionBadge.className = 'badge error';
      connectionBadge.textContent = 'Status: Failed';
      configFeedback.textContent = data.error || 'Connection failed.';
    }
  } catch (err) {
    connectionBadge.className = 'badge error';
    connectionBadge.textContent = 'Status: Error';
    configFeedback.textContent = `Network error: ${err.message}`;
  }
});

// --- Formatters (Tufte Clean Numbers) ---
const formatNOK = (val) => {
  if (val === undefined || val === null || isNaN(val)) return '-';
  return Number(val).toLocaleString('no-NO', { minimumFractionDigits: 2, maximumFractionDigits: 2 });
};

// --- Render Functions ---
const renderResults = (result) => {
  state.dataset = result.dataset_summary || {};
  state.metrics = result.metrics || {};
  state.prognosis = result.prognosis || {};
  state.prescriptions = result.prescriptions || [];

  // Update Status Indicator
  globalStatusDot.classList.add('active');
  globalStatusText.textContent = `Loaded ${Object.keys(state.dataset).length} datasets`;

  // Render Metrics Strip
  if (state.metrics) {
    metricActual.textContent = formatNOK(state.metrics.actual_total);
    metricBudget.textContent = formatNOK(state.metrics.budget_total);
    metricForecast.textContent = formatNOK(state.metrics.forecast_total);

    const varBudget = state.metrics.variance_to_budget || 0;
    metricVarBudget.textContent = formatNOK(varBudget);
    metricVarBudget.className = `metric-value ${varBudget < 0 ? 'variance-negative' : 'variance-positive'}`;

    const varForecast = state.metrics.variance_to_forecast || 0;
    metricVarForecast.textContent = formatNOK(varForecast);
    metricVarForecast.className = `metric-value ${varForecast < 0 ? 'variance-negative' : 'variance-positive'}`;

    metricFTE.textContent = (state.metrics.fte_total || 0).toFixed(1);
  }

  // Render Dataset Summary
  datasetSummary.innerHTML = Object.entries(state.dataset)
    .map(
      ([name, info]) => `
      <div class="summary-card">
        <div class="summary-card-name">${name}</div>
        <div class="summary-card-stats">${info.row_count.toLocaleString()} rows · ${info.column_count} cols</div>
      </div>
    `
    )
    .join('');

  // Render Schema Summary Table
  const schemas = result.schema_summary || {};
  schemaReport.innerHTML = `
    <table>
      <thead>
        <tr>
          <th>Table Name</th>
          <th>Columns & Inferred Types</th>
        </tr>
      </thead>
      <tbody>
        ${Object.entries(schemas)
          .map(
            ([tbl, cols]) => `
          <tr>
            <td><strong>${tbl}</strong></td>
            <td>${Object.entries(cols).map(([c, t]) => `${c}: <span style="color: var(--accent);">${t}</span>`).join(', ')}</td>
          </tr>
        `
          )
          .join('')}
      </tbody>
    </table>
  `;

  // Render Diagnostics Markdown Report
  diagnosticsReport.textContent = result.report || 'No diagnostic output returned.';

  // Render Prognostics Table
  renderPrognostics();

  // Render Prescriptions List
  renderPrescriptions();

  // Render AI Narrative if returned
  if (result.ai_narrative) {
    aiStoryOutput.textContent = result.ai_narrative;
  }
};

const renderPrognostics = () => {
  const rows = Object.values(state.prognosis || {});
  if (!rows.length) {
    prognosticsTable.innerHTML = '<p class="empty-state">No scenario projections available.</p>';
    return;
  }

  prognosticsTable.innerHTML = `
    <table>
      <thead>
        <tr>
          <th>Scenario</th>
          <th class="numeric">Actual Total</th>
          <th class="numeric">Expected Total (EAC)</th>
          <th class="numeric">Variance vs Budget</th>
        </tr>
      </thead>
      <tbody>
        ${rows
          .map(
            (row) => `
          <tr>
            <td style="text-transform: capitalize;"><strong>${row.scenario}</strong></td>
            <td class="numeric">${formatNOK(row.actual_total)}</td>
            <td class="numeric">${formatNOK(row.expected_total)}</td>
            <td class="numeric" style="color: ${row.variance_vs_budget < 0 ? 'var(--danger)' : 'var(--success)'};">
              ${formatNOK(row.variance_vs_budget)}
            </td>
          </tr>
        `
          )
          .join('')}
      </tbody>
    </table>
  `;
};

const renderPrescriptions = () => {
  const actions = state.prescriptions || [];
  if (!actions.length) {
    prescriptionsList.innerHTML = '<p class="empty-state">No prescriptive actions generated.</p>';
    return;
  }

  prescriptionsList.innerHTML = actions
    .map(
      (item) => `
    <div class="action-card">
      <div class="action-meta">
        <span class="badge">Impact Score: <span class="action-score">${(item.impact_score * 100).toFixed(0)}%</span></span>
      </div>
      <h4>${item.title}</h4>
      <p>${item.description}</p>
      <p style="color: var(--text-main); font-weight: 500;"><strong>Quantified Outcome:</strong> ${item.expected_result}</p>
    </div>
  `
    )
    .join('');
};

// --- Execution Handlers ---
runBtn.addEventListener('click', async () => {
  const files = [...csvInput.files];
  if (!files.length) {
    diagnosticsReport.textContent = 'Please select at least one CSV file to analyze.';
    return;
  }

  const formData = new FormData();
  files.forEach((file) => formData.append('files', file));
  diagnosticsReport.textContent = 'Executing multi-agent analytics pipeline on uploaded datasets...';

  const headers = {};
  if (state.config.apiKey) headers['X-Api-Key'] = state.config.apiKey;
  if (state.config.provider) headers['X-Provider'] = state.config.provider;
  if (state.config.model) headers['X-Model'] = state.config.model;
  if (state.config.endpoint) headers['X-Endpoint'] = state.config.endpoint;

  try {
    const response = await fetch(`${apiBase}/api/analyze`, {
      method: 'POST',
      body: formData,
      headers: headers,
    });
    const result = await response.json();
    if (!response.ok) throw new Error(result.error || 'Analysis failed.');
    renderResults(result);
  } catch (error) {
    diagnosticsReport.textContent = `Analysis error: ${error.message}`;
  }
});

loadDemoBtn.addEventListener('click', async () => {
  diagnosticsReport.textContent = 'Loading built-in demo ERP datasets (FactGL, FactBudget, FactForecast, FactFTE)...';
  try {
    const response = await fetch(`${apiBase}/api/demo-data`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
    });
    const result = await response.json();
    if (!response.ok) throw new Error(result.error || 'Demo load failed.');
    renderResults(result);
  } catch (error) {
    diagnosticsReport.textContent = `Demo load error: ${error.message}`;
  }
});

generateStoryBtn.addEventListener('click', async () => {
  if (!state.metrics || !Object.keys(state.metrics).length) {
    storyStatus.textContent = 'Please run diagnostics or load demo data first before generating an AI story.';
    return;
  }

  saveConfig();
  const provider = state.config.provider;
  const isOllama = provider === 'ollama';
  if (!state.config.apiKey && !isOllama) {
    storyStatus.textContent = `Please enter your ${provider.toUpperCase()} API key in the configuration panel above.`;
    return;
  }

  storyStatus.textContent = `Generating decision narrative via ${provider.toUpperCase()} (${state.config.model})...`;
  aiStoryOutput.textContent = 'Synthesizing executive decision story...';

  try {
    const response = await fetch(`${apiBase}/api/ai/narrative`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        metrics: state.metrics,
        prognosis: state.prognosis,
        prescriptions: state.prescriptions,
        dataset_summary: state.dataset,
        provider: state.config.provider,
        api_key: state.config.apiKey,
        model: state.config.model,
        base_url: state.config.endpoint,
      }),
    });

    const data = await response.json();
    if (!response.ok) throw new Error(data.error || 'Failed to generate narrative.');
    aiStoryOutput.textContent = data.narrative;
    storyStatus.textContent = `Successfully synthesized executive story via ${data.provider} (${data.model}).`;
  } catch (err) {
    storyStatus.textContent = `Generation failed: ${err.message}`;
    aiStoryOutput.textContent = `Unable to generate story: ${err.message}`;
  }
});

// --- Skills Catalog Loader ---
const loadSkillsCatalog = async () => {
  try {
    const res = await fetch(`${apiBase}/api/skills`);
    if (!res.ok) return;
    const data = await res.json();
    state.skills = data.skills || [];
    renderSkillsList(state.skills);
  } catch (e) {
    console.warn('Could not load skills catalog', e);
  }
};

const renderSkillsList = (skillsToRender) => {
  if (!skillsToRender.length) {
    skillsList.innerHTML = '<p class="empty-state">No matching skills found.</p>';
    return;
  }

  skillsList.innerHTML = skillsToRender
    .map(
      (skill) => `
    <div class="skill-card">
      <div class="skill-phase">${skill.phase}</div>
      <div class="skill-title">${skill.id} - ${skill.title}</div>
      <div class="skill-desc">${skill.description}</div>
    </div>
  `
    )
    .join('');
};

skillSearchInput.addEventListener('input', (e) => {
  const query = e.target.value.toLowerCase().trim();
  if (!query) {
    renderSkillsList(state.skills);
    return;
  }
  const filtered = state.skills.filter(
    (s) =>
      s.title.toLowerCase().includes(query) ||
      s.id.toLowerCase().includes(query) ||
      s.description.toLowerCase().includes(query) ||
      s.phase.toLowerCase().includes(query)
  );
  renderSkillsList(filtered);
});

// Initial boot
window.addEventListener('DOMContentLoaded', () => {
  loadSavedConfig();
  loadSkillsCatalog();
});
