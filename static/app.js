const state = {
  files: [],
  dataset: {},
  metrics: {},
};

const tabs = document.querySelectorAll('.tab');
tabs.forEach((tab) => {
  tab.addEventListener('click', () => {
    tabs.forEach((btn) => btn.classList.remove('active'));
    tab.classList.add('active');
    document.querySelectorAll('.panel').forEach((panel) => {
      panel.classList.toggle('active', panel.id === tab.dataset.target);
    });
  });
});

const csvInput = document.getElementById('csvFiles');
const runBtn = document.getElementById('runDiagnosticsBtn');
const datasetSummary = document.getElementById('datasetSummary');
const diagnosticsReport = document.getElementById('diagnosticsReport');
const prognosticsTable = document.getElementById('prognosticsTable');
const prescriptionsList = document.getElementById('prescriptionsList');
const apiBase =
  window.location.protocol === 'file:' || window.location.port !== '8000'
    ? 'http://127.0.0.1:8000'
    : '';

const parseCSV = (text, delimiter = ';') => {
  const lines = text.split(/\r?\n/).filter((line) => line.trim().length > 0);
  if (!lines.length) return [];

  const rows = lines.map((line) => {
    const values = [];
    let current = '';
    let inQuotes = false;

    for (let i = 0; i < line.length; i += 1) {
      const char = line[i];
      if (char === '"') {
        if (inQuotes && line[i + 1] === '"') {
          current += '"';
          i += 1;
        } else {
          inQuotes = !inQuotes;
        }
      } else if (char === delimiter && !inQuotes) {
        values.push(current);
        current = '';
      } else {
        current += char;
      }
    }
    values.push(current);
    return values;
  });

  return rows;
};

const parseNumber = (value) => {
  if (value === null || value === undefined) return 0;
  const text = String(value).trim();
  if (!text || ['null', 'none', 'n/a', 'na'].includes(text.toLowerCase()))
    return 0;

  let cleaned = text.replace(/\s/g, '');
  if (cleaned.includes('.') && cleaned.includes(',')) {
    cleaned = cleaned.replace(/\./g, '').replace(',', '.');
  } else if (cleaned.includes(',')) {
    cleaned = cleaned.replace(',', '.');
  }

  const numeric = Number(cleaned);
  return Number.isFinite(numeric) ? numeric : 0;
};

const sumColumn = (rows, columnName) => {
  if (!rows.length) return 0;
  const headers = rows[0];
  const index = headers.indexOf(columnName);
  if (index === -1) return 0;

  let total = 0;
  for (let i = 1; i < rows.length; i += 1) {
    total += parseNumber(rows[i][index]);
  }
  return total;
};

const renderResults = (result) => {
  state.dataset = result.dataset_summary;
  state.metrics = result.metrics;

  datasetSummary.innerHTML = Object.entries(state.dataset)
    .map(
      ([name, info]) => `
      <div class="metric-box">
        <span class="metric-label">${name}</span>
        <div class="metric-value">${info.row_count} rows</div>
        <div class="metric-label">${info.column_count} columns</div>
      </div>
    `
    )
    .join('');
  diagnosticsReport.textContent = result.report;
  state.prognosis = result.prognosis;
  state.prescriptions = result.prescriptions;
  renderPrognostics();
  renderPrescriptions();
};

const renderPrognostics = () => {
  const { actual_total, budget_total, forecast_total } = state.metrics;
  const baseline = {
    scenario: 'Baseline',
    actual_total: actual_total,
    expected_total: forecast_total,
    variance_vs_budget: actual_total - budget_total,
  };

  const conservative = {
    scenario: 'Conservative',
    actual_total: actual_total,
    expected_total: Math.max(0, forecast_total * 0.92),
    variance_vs_budget: actual_total - budget_total * 0.95,
  };

  const optimistic = {
    scenario: 'Optimistic',
    actual_total: actual_total,
    expected_total: forecast_total * 1.08,
    variance_vs_budget: actual_total - budget_total * 1.02,
  };

  const rows = Object.values(
    state.prognosis || { baseline, conservative, optimistic }
  );
  prognosticsTable.innerHTML = `
    <table>
      <thead>
        <tr>
          <th>Scenario</th>
          <th>Actual total</th>
          <th>Expected total</th>
          <th>Variance vs budget</th>
        </tr>
      </thead>
      <tbody>
        ${rows
          .map(
            (row) => `
          <tr>
            <td>${row.scenario}</td>
            <td>${row.actual_total.toFixed(2)}</td>
            <td>${row.expected_total.toFixed(2)}</td>
            <td>${row.variance_vs_budget.toFixed(2)}</td>
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

  prescriptionsList.innerHTML = actions
    .map(
      (item) => `
    <div class="action-card">
      <span class="badge">Recommended action</span>
      <h4>${item.title}</h4>
      <p>${item.description}</p>
      <p><strong>Expected result:</strong> ${item.expected_result}</p>
      <p><strong>Impact score:</strong> ${item.impact_score}</p>
    </div>
  `
    )
    .join('');
};

runBtn.addEventListener('click', () => {
  const files = [...csvInput.files];
  if (!files.length) {
    diagnosticsReport.textContent = 'Please upload at least one CSV file.';
    return;
  }

  const formData = new FormData();
  files.forEach((file) => formData.append('files', file));
  diagnosticsReport.textContent = 'Running backend diagnostics...';

  fetch(`${apiBase}/api/analyze`, { method: 'POST', body: formData })
    .then(async (response) => {
      const contentType = response.headers.get('content-type') || '';
      const body = contentType.includes('application/json')
        ? await response.json()
        : { error: (await response.text()).slice(0, 500) };
      const result = body;
      if (!response.ok) throw new Error(result.error || 'Analysis failed.');
      return result;
    })
    .then(renderResults)
    .catch((error) => {
      diagnosticsReport.textContent = `Unable to run backend analysis: ${error.message}`;
    });
});

window.addEventListener('DOMContentLoaded', () => {
  diagnosticsReport.textContent =
    'Upload CSV files to generate diagnostics, prognostics, and action recommendations.';
  prognosticsTable.innerHTML =
    '<p>Upload files to see prognostic scenarios.</p>';
  prescriptionsList.innerHTML =
    '<p>Upload files to see recommended actions.</p>';
});
