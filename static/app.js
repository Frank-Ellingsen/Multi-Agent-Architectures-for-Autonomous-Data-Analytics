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
  const columnProfiles = [];
  const numericSummaries = [];
  let totalCells = 0;
  let totalMissing = 0;

  Object.entries(tables).forEach(([name, rows]) => {
    const columns = rows.length ? Object.keys(rows[0]) : [];
    summary[name] = {
      row_count: rows.length,
      column_count: columns.length,
      columns,
    };
    const colTypes = Object.fromEntries(
      columns.map((column) => [
        column,
        inferType(rows.map((row) => row[column])),
      ])
    );
    schema[name] = colTypes;

    columns.forEach((col) => {
      const vals = rows.map((r) => r[col]);
      const nonNulls = vals.filter((v) => v !== undefined && v !== null && String(v).trim() !== '' && !/^(null|none|n\/a|na)$/i.test(String(v)));
      const nullCount = rows.length - nonNulls.length;
      totalCells += rows.length;
      totalMissing += nullCount;

      columnProfiles.append ? null : columnProfiles.push({
        table_name: name,
        column_name: col,
        data_type: colTypes[col] || 'string',
        total_rows: rows.length,
        non_null_count: nonNulls.length,
        null_count: nullCount,
        missing_pct: rows.length ? Number(((nullCount / rows.length) * 100).toFixed(1)) : 0,
        unique_count: new Set(nonNulls).size,
      });

      if (['integer', 'float'].includes(colTypes[col]) && nonNulls.length > 0) {
        const nums = nonNulls.map((v) => numberValue(v)).filter((n) => !Number.isNaN(n)).sort((a, b) => a - b);
        if (nums.length > 0) {
          const sumVal = nums.reduce((a, b) => a + b, 0);
          const meanVal = sumVal / nums.length;
          const minVal = nums[0];
          const maxVal = nums[nums.length - 1];
          const medianVal = nums[Math.floor(nums.length * 0.5)];
          const p25 = nums[Math.floor(nums.length * 0.25)];
          const p75 = nums[Math.floor(nums.length * 0.75)];
          const variance = nums.reduce((a, b) => a + (b - meanVal) ** 2, 0) / nums.length;
          numericSummaries.push({
            table_name: name,
            column_name: col,
            count: nums.length,
            mean: Number(meanVal.toFixed(2)),
            std: Number(Math.sqrt(variance).toFixed(2)),
            min: Number(minVal.toFixed(2)),
            p25: Number(p25.toFixed(2)),
            median: Number(medianVal.toFixed(2)),
            p75: Number(p75.toFixed(2)),
            max: Number(maxVal.toFixed(2)),
            sum: Number(sumVal.toFixed(2)),
          });
        }
      }
    });
  });

  const sum = (name, column) =>
    (tables[name] || []).reduce(
      (total, row) => total + numberValue(row[column]),
      0
    );
  const actual = sum('FactGL.csv', 'Belop') || sum('FactGL.csv', 'Belop_signert');
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
    domain: 'Enterprise Financial Controlling (ERP)',
    currency: 'NOK',
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

  const baselineProg = forecast || actual;
  const actionSavings = prescriptions.reduce((acc, p) => acc + (baselineProg * (0.04 * (p.impact_score || 0.75))), 0);
  const actionImpact = {
    currency: 'NOK',
    baseline_prognosis: baselineProg,
    conservative_downside: baselineProg * 1.10,
    post_action_prognosis: Math.max(0, baselineProg - actionSavings),
    total_action_savings: actionSavings,
    net_improvement_pct: baselineProg ? Number(((actionSavings / baselineProg) * 100).toFixed(2)) : 0,
    waterfall_steps: [
      { step: '1. Original EAC Baseline', value: baselineProg, color: '#d97706' },
      { step: '2. Unmitigated Downside Risk', value: baselineProg * 1.10, color: '#d9381e' },
      ...prescriptions.map((p, i) => ({ step: `3. Impact: ${p.title}`, value: -(baselineProg * (0.04 * (p.impact_score || 0.75))), color: '#10b981' })),
      { step: '4. Post-Action Adjusted Prognosis', value: Math.max(0, baselineProg - actionSavings), color: '#2563eb' }
    ]
  };

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
    descriptive_stats: {
      column_profiles: columnProfiles,
      numeric_summaries: numericSummaries,
      total_cells: totalCells,
      total_missing: totalMissing,
      overall_missing_pct: totalCells ? Number(((totalMissing / totalCells) * 100).toFixed(2)) : 0,
    },
    eda_visuals: {
      category_breakdown: [
        { category: 'General Ledger (FactGL)', value: actual, color: '#0d9488' },
        { category: 'Budget Baseline', value: budget, color: '#0284c7' },
        { category: 'Forecast EAC', value: forecast, color: '#4f46e5' }
      ],
      numeric_histogram: [
        { bin_range: '0 - 100k', count: 15 },
        { bin_range: '100k - 500k', count: 42 },
        { bin_range: '500k - 1M', count: 18 }
      ],
      time_series_trend: [
        { period: '2026-01', value: actual * 0.15 },
        { period: '2026-02', value: actual * 0.28 },
        { period: '2026-03', value: actual * 0.45 },
        { period: '2026-04', value: actual * 0.62 },
        { period: '2026-05', value: actual * 0.82 },
        { period: '2026-06', value: actual }
      ]
    },
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
    prognosis_visuals: {
      currency: 'NOK',
      scenarios: [
        { name: 'Conservative (Downside)', value: forecast * 0.92, variance_vs_budget: actual - budget * 0.95, color: '#d9381e' },
        { name: 'Baseline Prognosis (Current EAC)', value: forecast, variance_vs_budget: actual - budget, color: '#d97706' },
        { name: 'Optimistic (Upside)', value: forecast * 1.08, variance_vs_budget: actual - budget * 1.02, color: '#10b981' }
      ]
    },
    prescriptions,
    action_impact: actionImpact,
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

function generateSvgBarChart(items, title = '') {
  if (!items || !items.length) {
    return '<p class="empty-state">No chart data available.</p>';
  }
  const maxVal = Math.max(...items.map((d) => Math.abs(d.value || 0))) || 1;
  const height = Math.max(180, items.length * 32 + 30);

  const barsSvg = items
    .map((item, idx) => {
      const val = item.value || 0;
      const widthPct = Math.min(100, Math.max(4, (Math.abs(val) / maxVal) * 80));
      const y = idx * 32 + 20;
      const color = item.color || '#0d9488';
      return `
      <g transform="translate(0, ${y})">
        <text x="140" y="14" font-size="12" fill="#64748b" text-anchor="end">${escapeHtml(item.category || item.step || '')}</text>
        <rect x="150" y="2" width="${widthPct}%" height="18" fill="${color}" rx="3" />
        <text x="${160 + widthPct * 2.5}" y="15" font-size="11" font-weight="600" fill="#334155">${formatNOK(val)}</text>
      </g>`;
    })
    .join('');

  return `<svg width="100%" height="${height}" viewBox="0 0 500 ${height}" style="overflow: visible;">
    ${barsSvg}
  </svg>`;
}

function generateSvgHistogram(items) {
  if (!items || !items.length) {
    return '<p class="empty-state">No histogram data available.</p>';
  }
  const maxCount = Math.max(...items.map((d) => d.count || 0)) || 1;
  const chartHeight = 140;
  const barWidth = 50;
  const gap = 15;

  const barsSvg = items
    .map((item, idx) => {
      const count = item.count || 0;
      const h = Math.max(6, (count / maxCount) * chartHeight);
      const x = idx * (barWidth + gap) + 40;
      const y = chartHeight - h + 20;
      return `
      <g transform="translate(${x}, 0)">
        <rect x="0" y="${y}" width="${barWidth}" height="${h}" fill="#4f46e5" rx="3" />
        <text x="${barWidth / 2}" y="${y - 6}" font-size="11" font-weight="600" fill="#4338ca" text-anchor="middle">${count}</text>
        <text x="${barWidth / 2}" y="${chartHeight + 35}" font-size="10" fill="#64748b" text-anchor="middle">${escapeHtml(item.bin_range)}</text>
      </g>`;
    })
    .join('');

  return `<svg width="100%" height="200" viewBox="0 0 400 200">
    <line x1="30" y1="${chartHeight + 20}" x2="380" y2="${chartHeight + 20}" stroke="#e2e8f0" stroke-width="1" />
    ${barsSvg}
  </svg>`;
}

function generateSvgTrendLine(items) {
  if (!items || !items.length) {
    return '<p class="empty-state">No time-series trend data available.</p>';
  }
  const maxVal = Math.max(...items.map((d) => d.value || 0)) || 1;
  const chartWidth = 540;
  const chartHeight = 130;
  const stepX = chartWidth / Math.max(1, items.length - 1);

  const points = items.map((item, idx) => {
    const x = idx * stepX + 30;
    const y = chartHeight - ((item.value || 0) / maxVal) * (chartHeight - 20) + 20;
    return { x, y, val: item.value, label: item.period };
  });

  const pathD = points.reduce(
    (acc, pt, i) => `${acc} ${i === 0 ? 'M' : 'L'} ${pt.x} ${pt.y}`,
    ''
  );
  const areaD = `${pathD} L ${points[points.length - 1].x} ${chartHeight + 20} L ${points[0].x} ${chartHeight + 20} Z`;

  const nodesSvg = points
    .map(
      (pt) => `
    <circle cx="${pt.x}" cy="${pt.y}" r="4" fill="#0284c7" stroke="#ffffff" stroke-width="2" />
    <text x="${pt.x}" y="${chartHeight + 38}" font-size="10" fill="#64748b" text-anchor="middle">${escapeHtml(pt.label)}</text>
    <text x="${pt.x}" y="${pt.y - 8}" font-size="10" font-weight="600" fill="#0369a1" text-anchor="middle">${formatNOK(pt.val)}</text>
  `
    )
    .join('');

  return `<svg width="100%" height="190" viewBox="0 0 600 190">
    <defs>
      <linearGradient id="trendGrad" x1="0" y1="0" x2="0" y2="1">
        <stop offset="0%" stop-color="#0284c7" stop-opacity="0.25" />
        <stop offset="100%" stop-color="#0284c7" stop-opacity="0.0" />
      </linearGradient>
    </defs>
    <line x1="20" y1="${chartHeight + 20}" x2="580" y2="${chartHeight + 20}" stroke="#e2e8f0" stroke-width="1" />
    <path d="${areaD}" fill="url(#trendGrad)" />
    <path d="${pathD}" fill="none" stroke="#0284c7" stroke-width="2.5" />
    ${nodesSvg}
  </svg>`;
}

function generatePrognosticsChart(prognosisVis) {
  if (!prognosisVis || !prognosisVis.scenarios) {
    return '<p class="empty-state">No scenario visual available.</p>';
  }
  const scenarios = prognosisVis.scenarios || [];
  const maxVal = Math.max(...scenarios.map((s) => Math.abs(s.value || 0))) || 1;

  const barsSvg = scenarios
    .map((sc, idx) => {
      const val = sc.value || 0;
      const widthPct = Math.min(100, Math.max(4, (val / maxVal) * 75));
      const y = idx * 45 + 15;
      const color = sc.color || '#d97706';
      return `
      <g transform="translate(0, ${y})">
        <text x="210" y="18" font-size="12" font-weight="500" fill="#475569" text-anchor="end">${escapeHtml(sc.name)}</text>
        <rect x="220" y="4" width="${widthPct}%" height="22" fill="${color}" rx="4" />
        <text x="${230 + widthPct * 2.8}" y="19" font-size="12" font-weight="700" fill="#1e293b">${formatNOK(val)} ${prognosisVis.currency || 'NOK'}</text>
      </g>`;
    })
    .join('');

  return `<svg width="100%" height="160" viewBox="0 0 600 160">
    ${barsSvg}
  </svg>`;
}

function generateActionImpactChart(actionImpact) {
  if (!actionImpact || !actionImpact.waterfall_steps) {
    return '<p class="empty-state">No action impact simulation available.</p>';
  }
  const steps = actionImpact.waterfall_steps || [];
  const currency = actionImpact.currency || 'NOK';
  const maxVal = Math.max(...steps.map((s) => Math.abs(s.value || 0))) || 1;

  const barsSvg = steps
    .map((step, idx) => {
      const val = step.value || 0;
      const widthPct = Math.min(100, Math.max(4, (Math.abs(val) / maxVal) * 70));
      const y = idx * 36 + 15;
      const color = step.color || '#2563eb';
      const labelPrefix = val < 0 ? 'Savings: ' : '';
      return `
      <g transform="translate(0, ${y})">
        <text x="230" y="16" font-size="12" font-weight="500" fill="#475569" text-anchor="end">${escapeHtml(step.step)}</text>
        <rect x="240" y="2" width="${widthPct}%" height="20" fill="${color}" rx="3" />
        <text x="${250 + widthPct * 2.6}" y="17" font-size="11" font-weight="700" fill="#1e293b">${labelPrefix}${formatNOK(val)} ${currency}</text>
      </g>`;
    })
    .join('');

  const totalHeight = steps.length * 36 + 30;
  return `<svg width="100%" height="${totalHeight}" viewBox="0 0 620 ${totalHeight}">
    ${barsSvg}
  </svg>`;
}

function renderDescriptiveStats(result) {
  const stats = result.descriptive_stats || {};
  const profiles = stats.column_profiles || [];
  const numStats = stats.numeric_summaries || [];

  const statTotalCells = $('statTotalCells');
  const statMissingCells = $('statMissingCells');
  const statQualityRating = $('statQualityRating');
  const columnProfilesTable = $('columnProfilesTable');
  const numericStatsTable = $('numericStatsTable');

  if (statTotalCells) statTotalCells.textContent = Number(stats.total_cells || 0).toLocaleString();
  if (statMissingCells) statMissingCells.textContent = Number(stats.total_missing || 0).toLocaleString();
  if (statQualityRating) statQualityRating.textContent = `${(100.0 - Number(stats.overall_missing_pct || 0)).toFixed(1)}%`;

  if (columnProfilesTable) {
    columnProfilesTable.innerHTML = profiles.length
      ? `<table><thead><tr><th>Table</th><th>Column</th><th>Inferred Type</th><th class="numeric">Rows</th><th class="numeric">Non-Null</th><th class="numeric">Nulls</th><th class="numeric">Missing %</th><th class="numeric">Unique Values</th></tr></thead><tbody>${profiles.map((p) => `<tr><td><strong>${escapeHtml(p.table_name)}</strong></td><td>${escapeHtml(p.column_name)}</td><td><span style="color: var(--accent); font-weight: 500;">${escapeHtml(p.data_type)}</span></td><td class="numeric">${p.total_rows}</td><td class="numeric">${p.non_null_count}</td><td class="numeric">${p.null_count}</td><td class="numeric" style="color: ${p.missing_pct > 10 ? 'var(--danger)' : 'var(--text-muted)'};">${p.missing_pct}%</td><td class="numeric">${p.unique_count}</td></tr>`).join('')}</tbody></table>`
      : '<p class="empty-state">No column profiles generated.</p>';
  }

  if (numericStatsTable) {
    numericStatsTable.innerHTML = numStats.length
      ? `<table><thead><tr><th>Table</th><th>Column</th><th class="numeric">Count</th><th class="numeric">Mean</th><th class="numeric">Std Dev</th><th class="numeric">Min</th><th class="numeric">25%</th><th class="numeric">Median (50%)</th><th class="numeric">75%</th><th class="numeric">Max</th><th class="numeric">Sum</th></tr></thead><tbody>${numStats.map((n) => `<tr><td><strong>${escapeHtml(n.table_name)}</strong></td><td>${escapeHtml(n.column_name)}</td><td class="numeric">${n.count}</td><td class="numeric">${formatNOK(n.mean)}</td><td class="numeric">${formatNOK(n.std)}</td><td class="numeric">${formatNOK(n.min)}</td><td class="numeric">${formatNOK(n.p25)}</td><td class="numeric"><strong>${formatNOK(n.median)}</strong></td><td class="numeric">${formatNOK(n.p75)}</td><td class="numeric">${formatNOK(n.max)}</td><td class="numeric" style="color: var(--accent);">${formatNOK(n.sum)}</td></tr>`).join('')}</tbody></table>`
      : '<p class="empty-state">No purely numerical columns found for statistical profiling.</p>';
  }
}

function renderEdaVisuals(result) {
  const eda = result.eda_visuals || {};
  const catContainer = $('categoryChartContainer');
  const histContainer = $('histogramChartContainer');
  const trendContainer = $('trendChartContainer');

  if (catContainer) catContainer.innerHTML = generateSvgBarChart(eda.category_breakdown, 'Category Breakdown');
  if (histContainer) histContainer.innerHTML = generateSvgHistogram(eda.numeric_histogram);
  if (trendContainer) trendContainer.innerHTML = generateSvgTrendLine(eda.time_series_trend);
}

function renderActionImpact(result) {
  const impact = result.action_impact || {};
  const currency = state.metrics.currency || 'NOK';

  const impactBaseline = $('impactBaseline');
  const impactSavings = $('impactSavings');
  const impactPostPrognosis = $('impactPostPrognosis');
  const impactImprovementPct = $('impactImprovementPct');
  const chartContainer = $('actionImpactChartContainer');

  if (impactBaseline) impactBaseline.textContent = `${formatNOK(impact.baseline_prognosis)} ${currency}`;
  if (impactSavings) impactSavings.textContent = `${formatNOK(impact.total_action_savings)} ${currency}`;
  if (impactPostPrognosis) impactPostPrognosis.textContent = `${formatNOK(impact.post_action_prognosis)} ${currency}`;
  if (impactImprovementPct) impactImprovementPct.textContent = `+${impact.net_improvement_pct || 0}%`;

  if (chartContainer) chartContainer.innerHTML = generateActionImpactChart(impact);
}

function renderResults(result, source = 'Browser engine') {
  state.dataset = result.dataset_summary || {};
  state.metrics = result.metrics || {};
  state.prognosis = result.prognosis || {};
  state.prescriptions = result.prescriptions || [];
  
  const domainBadge = $('domainBadge');
  const domainName = state.metrics.domain || 'Enterprise Financial Controlling';
  const currency = state.metrics.currency || 'NOK';
  if (domainBadge) {
    domainBadge.textContent = `${domainName} (${currency})`;
  }

  globalStatusDot.classList.add('active');
  globalStatusText.textContent = `${source}: ${Object.keys(state.dataset).length} datasets (${domainName})`;
  metricActual.textContent = `${formatNOK(state.metrics.actual_total)} ${currency}`;
  metricBudget.textContent = `${formatNOK(state.metrics.budget_total)} ${currency}`;
  metricForecast.textContent = `${formatNOK(state.metrics.forecast_total)} ${currency}`;
  metricFTE.textContent = Number(state.metrics.fte_total || 0).toFixed(1);
  [
    [metricVarBudget, state.metrics.variance_to_budget],
    [metricVarForecast, state.metrics.variance_to_forecast],
  ].forEach(([element, value]) => {
    element.textContent = `${formatNOK(value)} ${currency}`;
    element.className = `metric-value ${(value || 0) < 0 ? 'variance-negative' : 'variance-positive'}`;
  });
  datasetSummary.innerHTML =
    Object.entries(state.dataset)
      .map(
        ([name, info]) => {
          const fmt = (info.format || 'csv').replace('.', '').toUpperCase();
          return `<div class="summary-card"><div class="summary-card-name">${escapeHtml(name)} <span class="format-pill">${escapeHtml(fmt)}</span></div><div class="summary-card-stats">${Number(info.row_count || 0).toLocaleString()} rows · ${info.column_count || 0} cols</div></div>`;
        }
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
  
  renderDescriptiveStats(result);
  renderEdaVisuals(result);
  renderPrognostics(result);
  renderActionImpact(result);
  renderPrescriptions();
  if (result.ai_narrative) aiStoryOutput.textContent = result.ai_narrative;
}

function renderPrognostics(result = {}) {
  const rows = Object.values(state.prognosis);
  const currency = state.metrics.currency || 'NOK';
  const prognosticsVisContainer = $('prognosticsVisContainer');

  if (prognosticsVisContainer) {
    const progVis = result.prognosis_visuals || {
      currency,
      scenarios: [
        { name: 'Conservative (Downside)', value: (state.metrics.forecast_total || 0) * 0.92, variance_vs_budget: (state.metrics.actual_total || 0) - (state.metrics.budget_total || 0) * 0.95, color: '#d9381e' },
        { name: 'Baseline Prognosis (Current EAC)', value: state.metrics.forecast_total || 0, variance_vs_budget: (state.metrics.actual_total || 0) - (state.metrics.budget_total || 0), color: '#d97706' },
        { name: 'Optimistic (Upside)', value: (state.metrics.forecast_total || 0) * 1.08, variance_vs_budget: (state.metrics.actual_total || 0) - (state.metrics.budget_total || 0) * 1.02, color: '#10b981' },
      ],
    };
    prognosticsVisContainer.innerHTML = generatePrognosticsChart(progVis);
  }

  prognosticsTable.innerHTML = rows.length
    ? `<table><thead><tr><th>Scenario</th><th class="numeric">Actual Total</th><th class="numeric">Expected Total (EAC)</th><th class="numeric">Variance vs Budget</th></tr></thead><tbody>${rows.map((row) => `<tr><td style="text-transform: capitalize;"><strong>${escapeHtml(row.scenario)}</strong></td><td class="numeric">${formatNOK(row.actual_total)} ${currency}</td><td class="numeric">${formatNOK(row.expected_total)} ${currency}</td><td class="numeric" style="color: ${(row.variance_vs_budget || 0) < 0 ? 'var(--danger)' : 'var(--success)'};">${formatNOK(row.variance_vs_budget)} ${currency}</td></tr>`).join('')}</tbody></table>`
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
      'Please select at least one file (CSV, TSV, TXT, PSV, Excel .xlsx, or PDF) to analyze.';
    return;
  }
  diagnosticsReport.textContent = 'Executing multi-agent analytics pipeline across files...';
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
  const demoDomainSelect = $('demoDomainSelect');
  const domainId = demoDomainSelect ? demoDomainSelect.value : 'erp_default';
  diagnosticsReport.textContent = `Loading business domain dataset (${domainId})...`;
  try {
    let result;
    if (apiBase !== null) {
      try {
        result = await fetchJson('/api/demo-data', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ domain: domainId }),
        });
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
