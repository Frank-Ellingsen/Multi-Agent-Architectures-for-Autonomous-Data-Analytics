# Multi-Agent Architectures for Autonomous Data Analytics

A modular, production-ready framework for multi-agent autonomous data analytics, financial controlling, and project forecasting. This architecture converts raw enterprise data (general ledgers, budget workbooks, forecast submissions, project registers, timesheets) into decision-ready executive intelligence through a chain of 30 specialized operational skills.

---

## Architecture & Workflow Overview

The analytics workflow progresses across 6 distinct phases:

```text
Phase I: Ingestion & Inspection (Skills 01–04)
   └── Inspect source footprints, parse delimited files & spreadsheets, extract qualitative document facts.
Phase II: Schema & Modeling (Skills 05–10)
   └── Infer physical schema, validate foreign keys, audit data quality, normalize, build star schema, execute DuckDB SQL.
Phase III: Diagnostics & Metrics (Skills 11–16)
   └── Calculate KPIs (Actual, Budget, Forecast, EAC, ETC, FTE), analyze variance bridges, detect anomalies, apply status RAG.
Phase IV: Prognostics & Simulation (Skills 17–22)
   └── Engineer time-series features, backtest forecasting models, simulate scenarios (P10/P50/P90), run Monte Carlo & Tornado sensitivity.
Phase V: Prescriptions & Optimization (Skills 23–26)
   └── Formulate candidate actions, score portfolios across ROI and risk, reconcile new pro-forma balance, index evidence vouchers.
Phase VI: Storytelling & Publishing (Skills 27–30)
   └── Select Tufte data-ink visuals, build executive BLUF narrative, independent validator audit gate, publish accessible HTML reports.
```

For the complete catalog of specifications, see [skills/README.md](skills/README.md).

---

## Key Features

- **30 Modular Skill Specifications:** Standardized operational contracts with typed YAML inputs, outputs, domain rules, guardrails, and definitions of done.
- **Local-First Analytical SQL:** High-speed in-memory analytics using **DuckDB** (with SQLite fallback) executing queries directly over raw CSV files.
- **Multi-Provider LLM Integration:** Autonomous executive decision story generation supporting:
  - **Google Gemini** (`gemini-3.6-flash`, `gemini-2.5-pro`)
  - **OpenAI** (`gpt-4o`, `gpt-4o-mini`)
  - **Anthropic Claude** (`claude-3-5-sonnet-20241022`)
  - **Local Ollama / LM Studio** (Local-first, privacy-preserving, zero external API keys or cloud dependencies needed)
- **Tufte Data-Ink UI:** Clean, clutter-free web studio with no vertical gridlines, right-aligned tabular numbers, direct labeling, and muted palettes with active variance alerts.
- **In-Browser API Key Management:** Users can input, test, securely persist (`localStorage`), and switch API keys directly from the Web interface.
- **Full Containerization:** Turnkey Docker and Docker Compose environment with non-root security, health checks, and volume mounts.
- **Deterministic Governance:** Red-Amber-Green (RAG) thresholds and accounting reconciliations are strictly enforced by deterministic logic, eliminating LLM hallucination.

---

## Quick Start: Running with Docker (Recommended)

To run the complete environment without installing Python packages locally:

### 1. Clone & Configure Environment
```bash
git clone https://github.com/Frank-Ellingsen/Multi-Agent-Architectures-for-Autonomous-Data-Analytics.git
cd Multi-Agent-Architectures-for-Autonomous-Data-Analytics

# Optional: copy and set your LLM API keys in .env
cp .env.example .env
```

### 2. Launch Services with Docker Compose
```bash
docker compose up --build
```

- **Web Studio & REST API:** Open [http://localhost:8000](http://localhost:8000)
- **Streamlit Studio:** Open [http://localhost:8501](http://localhost:8501)

### 3. Alternative: Run Single Container
```bash
docker build -t multi-agent-analytics .
docker run -p 8000:8000 -e GEMINI_API_KEY="your-key" multi-agent-analytics
```

---

## Quick Start: Running Locally (Native Python)

Requires **Python 3.10+**.

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Start the Web Studio & API
```bash
python api.py
```
Open [http://localhost:8000](http://localhost:8000) in your browser.

### 3. Start the Streamlit Analytics Studio (Optional)
```bash
streamlit run app.py
```
Open [http://localhost:8501](http://localhost:8501) in your browser.

---

## Configuring API Keys in the Web Studio

Users can configure API keys directly in the top panel of `index.html`:

1. Open [http://localhost:8000](http://localhost:8000).
2. In the **Model & API Key Configuration** card:
   - Select your provider: **Google Gemini**, **OpenAI**, **Anthropic Claude**, or **Local Ollama**.
   - Input your API key (masked with an optional Show/Hide toggle).
   - Click **Test Connection** to verify endpoint reachability.
   - Click **Save Settings** to persist your key securely in your browser's `localStorage`.
3. Click **Load Demo ERP Dataset** to immediately analyze the built-in 15-table test dataset.
4. Go to **AI Executive Story** and click **Generate Decision Story** to synthesize an autonomous executive decision briefing!

---

## Verified Benchmark on Sample ERP Dataset (`test_data`)

The repository includes a comprehensive 15-table real-world dataset in `test_data/`. You can evaluate the entire pipeline with:

```bash
python scripts/evaluate_dataset.py
```

### Benchmark Summary:
* **Ingestion Footprint**: 15 tables, **127,162 total rows** (semicolon-delimited, UTF-8).
* **Referential Integrity**: 22 star-schema relationships checked via `Relationships.csv` $\rightarrow$ **100% valid with 0 orphan keys**.
* **Financial Controlling KPIs**:
  * **Actual Spend (`FactGL`)**: `10,617,128.19 NOK`
  * **Approved Budget (`FactBudget`)**: `10,747,732.82 NOK`
  * **Latest Forecast (`FactForecast`)**: `145,015,843.77 NOK`
  * **Variance to Budget**: `-130,604.63 NOK` (**Favorable: 1.22% under budget**)
  * **Total Labor Run-Rate**: `15,390.2 FTE` across 12 monthly accounting periods.
* **Prognostic Scenarios**:
  * **Baseline EAC**: `145,015,843.77 NOK` (Variance vs Budget: `-130,604.63 NOK`)
  * **Conservative EAC**: `133,414,576.27 NOK` (Variance vs Budget: `+406,782.01 NOK` overrun risk)
  * **Optimistic EAC**: `156,617,111.27 NOK` (Variance vs Budget: `-345,559.29 NOK`)

---

## REST API Reference

The backend exposes a modular Flask REST API on port `8000`:

| Endpoint | Method | Description |
| :--- | :--- | :--- |
| `GET /` | `GET` | Serves the interactive Web Studio interface |
| `GET /api/health` | `GET` | Health check endpoint returning service status, version, and skill count |
| `GET /api/skills` | `GET` | Returns catalog of all 30 skills organized by phase with descriptions |
| `POST /api/analyze` | `POST` | Ingests uploaded CSV files, validates relationships, computes KPIs, and generates prognostics |
| `POST /api/demo-data` | `POST` | Instantaneously executes full analysis over the built-in `test_data` dataset |
| `POST /api/ai/test-key` | `POST` | Tests API key authentication and network connectivity for Gemini, OpenAI, Claude, or Ollama |
| `POST /api/ai/narrative` | `POST` | Generates a Tufte-compliant executive decision story using the configured LLM provider |

---

## Command Line Interface (CLI)

You can run stages of the workflow directly from the command line:

```bash
# Print workflow skills in sequence
python -m multi_agent_analytics --start 1 --end 5

# Generate markdown report for a dataset
python -m multi_agent_analytics --data-dir test_data --report
```

---

## Validation & Testing

Run the test suite and verify the 30-skill catalog:

```bash
# Validate skill files
python scripts/validate_skills.py

# Run all 18 automated tests
python -m pytest -v
```

---

## Repository Structure

```text
.
├── Dockerfile                  # Production container definition (Python 3.11-slim, non-root)
├── docker-compose.yml          # Web Studio (8000) and Streamlit (8501) compose definition
├── .dockerignore               # Container build ignore rules
├── .env.example                # Environment variables template
├── requirements.txt            # Locked Python dependencies
├── pyproject.toml              # Build system and project metadata
├── index.html                  # Web Studio interface with API key configuration controls
├── static/
│   ├── app.js                  # Frontend client logic, API key storage & live chart rendering
│   └── styles.css              # Edward Tufte Data-Ink compliant stylesheet
├── api.py                      # Flask REST API backend (/api/analyze, /api/ai/*, /api/skills)
├── app.py                      # Streamlit Analytics Studio alternative UI
├── src/
│   └── multi_agent_analytics/
│       ├── ai_agent.py         # Multi-provider LLM client (Gemini, OpenAI, Anthropic, Ollama)
│       ├── sql_engine.py       # Analytical SQL query engine with DuckDB & SQLite
│       ├── analytics.py        # Financial controlling & KPI calculation functions
│       ├── dataset.py          # Delimiter detection and tabular dataset summaries
│       ├── decision.py         # Scenario prognosis and prescriptive action generators
│       ├── relationships.py    # Star-schema referential integrity validator
│       ├── reporting.py        # Markdown diagnostic report builder
│       ├── schema.py           # Physical schema & column type inference
│       └── workflow.py         # 30-skill workflow definitions and runner
├── scripts/
│   ├── evaluate_dataset.py     # Standalone dataset evaluation and DuckDB drilldown runner
│   └── validate_skills.py     # Skill catalog validation script
├── skills/                     # The 30 modular autonomous skill specifications
│   ├── 01_inspect_source.md ... 30_publish_reports.md
│   ├── reporting-expert-SKILL.md
│   └── project-finance-ai-reporting-expert-skill/
├── test_data/                  # Built-in demo ERP dataset (FactGL, FactBudget, FactForecast, etc.)
└── tests/                      # Automated test suite (18 unit and integration tests)
```

---

## License

This project is licensed under the MIT License. See [LICENSE](LICENSE).
