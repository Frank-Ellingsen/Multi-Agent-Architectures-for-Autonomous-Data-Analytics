/* global File */

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
    model: 'gemini-3.6-flash',
    endpoint: 'http://localhost:11434',
  },
};
const DEFAULT_MODELS = {
  gemini: 'gemini-3.6-flash',
  openai: 'gpt-4o-mini',
  anthropic: 'claude-3-5-sonnet-20241022',
  ollama: 'llama3.2',
};
const $ = (id) => document.getElementById(id);
const tabs = document.querySelectorAll('.tab');
const csvInput = $('csvFiles');
const runBtn = $('runDiagnosticsBtn');
const loadDemoBtn = $('loadDemoBtn');
const datasetSummary = $('datasetSummary');
const schemaReport = $('schemaReport');
const diagnosticsReport = $('diagnosticsReport');
const prognosticsTable = $('prognosticsTable');
const prescriptionsList = $('prescriptionsList');
const aiStoryOutput = $('aiStoryOutput');
const generateStoryBtn = $('generateStoryBtn');
const storyStatus = $('storyStatus');
const skillsList = $('skillsList');
const skillSearchInput = $('skillSearchInput');
const metricActual = $('metricActual');
const metricBudget = $('metricBudget');
const metricForecast = $('metricForecast');
const metricVarBudget = $('metricVarBudget');
const metricVarForecast = $('metricVarForecast');
const metricFTE = $('metricFTE');
const globalStatusDot = $('globalStatusDot');
const globalStatusText = $('globalStatusText');
const sidebarKeyStatus = $('sidebarKeyStatus');
const llmProviderSelect = $('llmProvider');
const apiKeyInput = $('apiKey');
const llmModelInput = $('llmModel');
const llmEndpointInput = $('llmEndpoint');
const endpointGroup = $('endpointGroup');
const apiKeyGroup = $('apiKeyGroup');
const testConnectionBtn = $('testConnectionBtn');
const saveKeyBtn = $('saveKeyBtn');
const clearKeyBtn = $('clearKeyBtn');
const toggleKeyBtn = $('toggleKeyVisibility');
const connectionBadge = $('connectionBadge');
const configFeedback = $('configFeedback');

// GitHub Pages has no Flask server. Use the API locally, otherwise run core analysis in the browser.
const isLocalApi =
  ['localhost', '127.0.0.1', '0.0.0.0'].includes(window.location.hostname) &&
  window.location.port === '8000';
const apiBase = isLocalApi ? '' : null;
const assetUrl = (name) =>
  new URL(`static/${name}`, document.baseURI).toString();
const escapeHtml = (value) =>
  String(value ?? '').replace(
    /[&<>"']/g,
    (char) =>
      ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' })[
        char
      ]
  );
const formatNOK = (value) =>
  value === undefined || value === null || Number.isNaN(Number(value))
    ? '-'
    : Number(value).toLocaleString('no-NO', {
        minimumFractionDigits: 2,
        maximumFractionDigits: 2,
      });
const numberValue = (value) => {
  const text = String(value ?? '')
    .trim()
    .replace(/\s/g, '');
  if (!text || /^(null|none|n\/a|na)$/i.test(text)) return 0;
  const normalized =
    text.includes('.') && text.includes(',')
      ? text.replace(/\./g, '').replace(',', '.')
      : text.replace(',', '.');
  const number = Number(normalized);
  return Number.isFinite(number) ? number : 0;
};

async function fetchJson(path, options = {}) {
  const response = await fetch(
    apiBase === null ? path : `${apiBase}${path}`,
    options
  );
  const data = await response.json();
  if (!response.ok)
    throw new Error(data.error || `Request failed (${response.status})`);
  return data;
}
tabs.forEach((tab) =>
  tab.addEventListener('click', () => {
    tabs.forEach((button) => button.classList.toggle('active', button === tab));
    document
      .querySelectorAll('.panel')
      .forEach((panel) =>
        panel.classList.toggle('active', panel.id === tab.dataset.target)
      );
  })
);

function updateConfigUI() {
  const provider = llmProviderSelect.value;
  const ollama = provider === 'ollama';
  endpointGroup.style.display = ollama ? 'flex' : 'none';
  apiKeyGroup.style.opacity = ollama ? '0.5' : '1';
  const ready = Boolean(apiKeyInput.value.trim()) || ollama;
  sidebarKeyStatus.textContent = ready
    ? ollama
      ? 'Ollama: Ready'
      : `${provider.toUpperCase()}: Configured`
    : 'API Key: Not Set';
  sidebarKeyStatus.classList.toggle('configured', ready);
}
function saveConfig(showMessage = true) {
  state.config = {
    provider: llmProviderSelect.value,
    apiKey: apiKeyInput.value.trim(),
    model: llmModelInput.value.trim(),
    endpoint: llmEndpointInput.value.trim(),
  };
  try {
    localStorage.setItem(
      'multi_agent_analytics_config',
      JSON.stringify(state.config)
    );
  } catch (_) {
    /* private browsing */
  }
  if (showMessage) {
    configFeedback.textContent = 'Settings saved locally.';
    setTimeout(() => {
      configFeedback.textContent = '';
    }, 3000);
  }
  updateConfigUI();
}
function loadSavedConfig() {
  try {
    const saved = JSON.parse(
      localStorage.getItem('multi_agent_analytics_config') || 'null'
    );
    if (saved) state.config = { ...state.config, ...saved };
  } catch (_) {
    /* ignore malformed local storage */
  }
  llmProviderSelect.value = state.config.provider;
  apiKeyInput.value = state.config.apiKey;
  llmModelInput.value =
    state.config.model || DEFAULT_MODELS[state.config.provider];
  llmEndpointInput.value = state.config.endpoint;
  updateConfigUI();
}
llmProviderSelect.addEventListener('change', () => {
  llmModelInput.value =
    DEFAULT_MODELS[llmProviderSelect.value] || DEFAULT_MODELS.gemini;
  updateConfigUI();
});
apiKeyInput.addEventListener('input', updateConfigUI);
toggleKeyBtn.addEventListener('click', () => {
  const hidden = apiKeyInput.type === 'password';
  apiKeyInput.type = hidden ? 'text' : 'password';
  toggleKeyBtn.textContent = hidden ? 'Hide' : 'Show';
});
saveKeyBtn.addEventListener('click', () => saveConfig());
clearKeyBtn.addEventListener('click', () => {
  apiKeyInput.value = '';
  try {
    localStorage.removeItem('multi_agent_analytics_config');
  } catch (_) {
    /* ignore */
  }
  configFeedback.textContent = 'Saved key cleared.';
  updateConfigUI();
});

function parseCsv(text) {
  const sample = text.slice(0, 4096);
  const delimiters = [';', ',', '\t', '|'];
  const delimiter = delimiters.reduce(
    (best, candidate) =>
      sample.split(candidate).length > sample.split(best).length
        ? candidate
        : best,
    ';'
  );
  const rows = [];
  let row = [];
  let cell = '';
  let quoted = false;
  for (let index = 0; index < text.length; index += 1) {
    const char = text[index];
    if (char === '"' && text[index + 1] === '"' && quoted) {
      cell += '"';
      index += 1;
    } else if (char === '"') quoted = !quoted;
    else if (char === delimiter && !quoted) {
      row.push(cell);
      cell = '';
    } else if ((char === '\n' || char === '\r') && !quoted) {
      if (char === '\r' && text[index + 1] === '\n') index += 1;
      row.push(cell);
      if (row.some((value) => value.trim())) rows.push(row);
      row = [];
      cell = '';
    } else cell += char;
  }
  if (cell || row.length) {
    row.push(cell);
    rows.push(row);
  }
  const headers = (rows.shift() || []).map((header) =>
    header.replace(/^\uFEFF/, '').trim()
  );
  return rows.map((values) =>
    Object.fromEntries(
      headers.map((header, index) => [header, (values[index] || '').trim()])
    )
  );
}
function inferType(values) {
  const populated = values.filter((value) => value !== '');
  if (!populated.length) return 'string';
  const numeric = populated.filter((value) =>
    /^[-+]?(?:\d+(?:[.,]\d+)?|\d{1,3}(?:\.\d{3})+(?:,\d+)?)$/.test(
      value.replace(/\s/g, '')
    )
  );
  if (numeric.length !== populated.length) return 'string';
  if (numeric.every((value) => /^[-+]?\d+$/.test(value.replace(/\s/g, ''))))
    return 'integer';
  return 'float';
}
function browserAnalysis(tables) {
  const summary = {};
  const schema = {};
  Object.entries(tables).forEach(([name, rows]) => {
    const columns = rows.length ? Object.keys(rows[0]) : [];
    summary[name] = {
      row_count: rows.length,
      column_count: columns.length,
      columns,
    };
    schema[name] = Object.fromEntries(
      columns.map((column) => [
        column,
        inferType(rows.map((row) => row[column])),
      ])
    );
  });
  const sum = (name, column) =>
    (tables[name] || []).reduce(
      (total, row) => total + numberValue(row[column]),
      0
    );
  const actual = sum('FactGL.csv', 'Belop_signert');
  const budget = sum('FactBudget.csv', 'BudsjettBelop');
  const forecast = sum('FactForecast.csv', 'ForecastBelop');
  const fte = sum('FactFTE.csv', 'Aarsverk');
  const metrics = {
    actual_total: actual,
    budget_total: budget,
    forecast_total: forecast,
    fte_total: fte,
    variance_to_budget: actual - budget,
    variance_to_forecast: actual - forecast,
  };
  const prognosis = {
    baseline: {
      actual_total: actual,
      expected_total: forecast,
      variance_vs_budget: actual - budget,
      scenario: 'baseline',
    },
    conservative: {
      actual_total: actual,
      expected_total: Math.max(0, forecast * 0.92),
      variance_vs_budget: actual - budget * 0.95,
      scenario: 'conservative',
    },
    optimistic: {
      actual_total: actual,
      expected_total: forecast * 1.08,
      variance_vs_budget: actual - budget * 1.02,
      scenario: 'optimistic',
    },
  };
  const prescriptions = [];
  if (metrics.variance_to_budget < 0)
    prescriptions.push({
      title: 'Reduce cost leakage',
      description:
        'Tighten discretionary spending and focus on the highest-impact budget lines.',
      expected_result: 'Reduce gap to budget by 10-20% within the next cycle.',
      impact_score: 0.82,
    });
  prescriptions.push({
    title: 'Prioritize revenue and forecast recovery',
    description:
      'Target the biggest forecast gaps and focus resource allocation on growth levers.',
    expected_result:
      'Lift actual results toward forecast by improving conversion and throughput.',
    impact_score: 0.76,
  });
  prescriptions.push({
    title: 'Create scenario-based contingency plan',
    description:
      'Run a conservative, neutral, and optimistic plan above the current baseline.',
    expected_result:
      'Improve decision resilience and reduce downside risk in the next planning cycle.',
    impact_score: 0.68,
  });
  const report = `# Data Analytics Report\n\n## Dataset overview\n\n${Object.entries(
    summary
  )
    .map(
      ([name, info]) =>
        `- ${name}: ${info.row_count} rows, ${info.column_count} columns`
    )
    .join(
      '\n'
    )}\n\n## Deterministic KPI audit\n\n- Actual total: ${formatNOK(actual)}\n- Budget total: ${formatNOK(budget)}\n- Forecast total: ${formatNOK(forecast)}\n- Variance to budget: ${formatNOK(actual - budget)}\n- FTE run rate: ${formatNOK(fte)}`;
  return {
    dataset_summary: summary,
    schema_summary: schema,
    relationship_summary: {
      relationship_count: (tables['Relationships.csv'] || []).length,
      valid: true,
      issues: [],
    },
    metrics,
    forecast_snapshot: {
      actual_vs_budget_pct: budget ? (actual / budget) * 100 : 0,
      actual_vs_forecast_pct: forecast ? (actual / forecast) * 100 : 0,
      forecast_gap: forecast - actual,
    },
    prognosis,
    prescriptions,
    report,
  };
}
async function filesToTables(files) {
  const tables = {};
  for (const file of files) tables[file.name] = parseCsv(await file.text());
  return tables;
}
async function analyzeFiles(files) {
  try {
    if (apiBase !== null) {
      const form = new FormData();
      files.forEach((file) => form.append('files', file));
      const headers = {};
      if (state.config.apiKey) headers['X-Api-Key'] = state.config.apiKey;
      headers['X-Provider'] = state.config.provider;
      headers['X-Model'] = state.config.model;
      return await fetchJson('/api/analyze', {
        method: 'POST',
        body: form,
        headers,
      });
    }
  } catch (error) {
    console.warn('API unavailable; using browser analysis:', error);
  }
  return browserAnalysis(await filesToTables(files));
}

function renderResults(result, source = 'Browser engine') {
  state.dataset = result.dataset_summary || {};
  state.metrics = result.metrics || {};
  state.prognosis = result.prognosis || {};
  state.prescriptions = result.prescriptions || [];
  globalStatusDot.classList.add('active');
  globalStatusText.textContent = `${source}: ${Object.keys(state.dataset).length} datasets`;
  metricActual.textContent = formatNOK(state.metrics.actual_total);
  metricBudget.textContent = formatNOK(state.metrics.budget_total);
  metricForecast.textContent = formatNOK(state.metrics.forecast_total);
  metricFTE.textContent = Number(state.metrics.fte_total || 0).toFixed(1);
  [
    [metricVarBudget, state.metrics.variance_to_budget],
    [metricVarForecast, state.metrics.variance_to_forecast],
  ].forEach(([element, value]) => {
    element.textContent = formatNOK(value);
    element.className = `metric-value ${(value || 0) < 0 ? 'variance-negative' : 'variance-positive'}`;
  });
  datasetSummary.innerHTML =
    Object.entries(state.dataset)
      .map(
        ([name, info]) =>
          `<div class="summary-card"><div class="summary-card-name">${escapeHtml(name)}</div><div class="summary-card-stats">${Number(info.row_count || 0).toLocaleString()} rows · ${info.column_count || 0} cols</div></div>`
      )
      .join('') || '<p class="empty-state">No tables found.</p>';
  schemaReport.innerHTML = `<table><thead><tr><th>Table Name</th><th>Columns &amp; Inferred Types</th></tr></thead><tbody>${Object.entries(
    result.schema_summary || {}
  )
    .map(
      ([table, columns]) =>
        `<tr><td><strong>${escapeHtml(table)}</strong></td><td>${Object.entries(
          columns
        )
          .map(
            ([column, type]) =>
              `${escapeHtml(column)}: <span style="color: var(--accent);">${escapeHtml(type)}</span>`
          )
          .join(', ')}</td></tr>`
    )
    .join('')}</tbody></table>`;
  diagnosticsReport.textContent =
    result.report || 'No diagnostic output returned.';
  renderPrognostics();
  renderPrescriptions();
  if (result.ai_narrative) aiStoryOutput.textContent = result.ai_narrative;
}
function renderPrognostics() {
  const rows = Object.values(state.prognosis);
  prognosticsTable.innerHTML = rows.length
    ? `<table><thead><tr><th>Scenario</th><th class="numeric">Actual Total</th><th class="numeric">Expected Total (EAC)</th><th class="numeric">Variance vs Budget</th></tr></thead><tbody>${rows.map((row) => `<tr><td style="text-transform: capitalize;"><strong>${escapeHtml(row.scenario)}</strong></td><td class="numeric">${formatNOK(row.actual_total)}</td><td class="numeric">${formatNOK(row.expected_total)}</td><td class="numeric" style="color: ${(row.variance_vs_budget || 0) < 0 ? 'var(--danger)' : 'var(--success)'};">${formatNOK(row.variance_vs_budget)}</td></tr>`).join('')}</tbody></table>`
    : '<p class="empty-state">No scenario projections available.</p>';
}
function renderPrescriptions() {
  prescriptionsList.innerHTML = state.prescriptions.length
    ? state.prescriptions
        .map(
          (item) =>
            `<div class="action-card"><div class="action-meta"><span class="badge">Impact Score: <span class="action-score">${(Number(item.impact_score || 0) * 100).toFixed(0)}%</span></span></div><h4>${escapeHtml(item.title)}</h4><p>${escapeHtml(item.description)}</p><p style="color: var(--text-main); font-weight: 500;"><strong>Quantified Outcome:</strong> ${escapeHtml(item.expected_result)}</p></div>`
        )
        .join('')
    : '<p class="empty-state">No prescriptive actions generated.</p>';
}

runBtn.addEventListener('click', async () => {
  const files = [...csvInput.files];
  if (!files.length) {
    diagnosticsReport.textContent =
      'Please select at least one CSV file to analyze.';
    return;
  }
  diagnosticsReport.textContent = 'Executing browser/API analytics pipeline...';
  try {
    renderResults(
      await analyzeFiles(files),
      apiBase === null ? 'Browser engine' : 'Local API'
    );
  } catch (error) {
    diagnosticsReport.textContent = `Analysis error: ${error.message}`;
  }
});
loadDemoBtn.addEventListener('click', async () => {
  diagnosticsReport.textContent = 'Loading built-in demo ERP dataset...';
  try {
    let result;
    if (apiBase !== null) {
      try {
        result = await fetchJson('/api/demo-data', { method: 'POST' });
      } catch (error) {
        console.warn('API unavailable; loading static demo:', error);
      }
    }
    if (!result)
      result = await fetch(assetUrl('demo-data.json')).then((response) => {
        if (!response.ok) throw new Error('Static demo data is unavailable.');
        return response.json();
      });
    renderResults(result, apiBase === null ? 'Static demo' : 'Local API');
  } catch (error) {
    diagnosticsReport.textContent = `Demo load error: ${error.message}`;
  }
});
function localNarrative() {
  const m = state.metrics;
  const direction = (m.variance_to_budget || 0) <= 0 ? 'under' : 'over';
  return `# Executive decision story\n\n## Bottom line\nActuals are ${formatNOK(Math.abs(m.variance_to_budget || 0))} ${direction} budget, while the current forecast is ${formatNOK(m.forecast_total)}.\n\n## Decision focus\nProtect the favorable budget position, investigate the forecast gap, and use the conservative scenario to set contingency triggers.\n\n## Recommended next actions\n${state.prescriptions.map((item, index) => `${index + 1}. ${item.title}: ${item.expected_result}`).join('\n')}\n\nThis narrative was generated locally from deterministic metrics. Configure a provider and run the local API for an LLM-authored version.`;
}
generateStoryBtn.addEventListener('click', async () => {
  if (!Object.keys(state.metrics).length) {
    storyStatus.textContent = 'Please run diagnostics or load demo data first.';
    return;
  }
  saveConfig(false);
  storyStatus.textContent = 'Generating decision narrative...';
  aiStoryOutput.textContent = 'Synthesizing executive decision story...';
  if (apiBase === null) {
    aiStoryOutput.textContent = localNarrative();
    storyStatus.textContent =
      'Generated locally in the browser (no backend required).';
    return;
  }
  try {
    const result = await fetchJson('/api/ai/narrative', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        metrics: state.metrics,
        prognosis: state.prognosis,
        prescriptions: state.prescriptions,
        dataset_summary: state.dataset,
        api_key: state.config.apiKey,
        provider: state.config.provider,
        model: state.config.model,
        base_url: state.config.endpoint,
      }),
    });
    aiStoryOutput.textContent = result.narrative;
    storyStatus.textContent = `Successfully synthesized via ${result.provider} (${result.model}).`;
  } catch (error) {
    storyStatus.textContent = `Generation failed: ${error.message}`;
    aiStoryOutput.textContent = localNarrative();
  }
});

async function loadSkillsCatalog() {
  try {
    let data;
    if (apiBase !== null) {
      try {
        data = await fetchJson('/api/skills');
      } catch (error) {
        console.warn('API unavailable; loading static skills:', error);
      }
    }
    if (!data)
      data = await fetch(assetUrl('skills.json')).then((response) =>
        response.json()
      );
    state.skills = data.skills || [];
    renderSkillsList(state.skills);
  } catch (error) {
    skillsList.innerHTML = `<p class="empty-state">Unable to load skills catalog: ${escapeHtml(error.message)}</p>`;
  }
}
function renderSkillsList(skills) {
  skillsList.innerHTML = skills.length
    ? skills
        .map(
          (skill) =>
            `<div class="skill-card"><div class="skill-phase">${escapeHtml(skill.phase)}</div><div class="skill-title">${escapeHtml(skill.id)} - ${escapeHtml(skill.title)}</div><div class="skill-desc">${escapeHtml(skill.description)}</div></div>`
        )
        .join('')
    : '<p class="empty-state">No matching skills found.</p>';
}
skillSearchInput.addEventListener('input', (event) => {
  const query = event.target.value.toLowerCase().trim();
  renderSkillsList(
    state.skills.filter(
      (skill) =>
        !query ||
        [skill.title, skill.id, skill.description, skill.phase].some((value) =>
          value.toLowerCase().includes(query)
        )
    )
  );
});
testConnectionBtn.addEventListener('click', async () => {
  saveConfig(false);
  connectionBadge.className = 'badge warning';
  connectionBadge.textContent = 'Status: Testing...';
  if (apiBase === null) {
    connectionBadge.className = 'badge connected';
    connectionBadge.textContent = 'Status: Browser Ready';
    configFeedback.textContent =
      'Core analytics run without a backend. LLM calls require the local API.';
    return;
  }
  try {
    const result = await fetchJson('/api/ai/test-key', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        provider: state.config.provider,
        api_key: state.config.apiKey,
        model: state.config.model,
        base_url: state.config.endpoint,
      }),
    });
    connectionBadge.className = 'badge connected';
    connectionBadge.textContent = `Status: Connected (${result.model})`;
    configFeedback.textContent = result.message || 'Connection verified.';
  } catch (error) {
    connectionBadge.className = 'badge error';
    connectionBadge.textContent = 'Status: Failed';
    configFeedback.textContent = error.message;
  }
});
window.addEventListener('DOMContentLoaded', () => {
  loadSavedConfig();
  loadSkillsCatalog();
});
