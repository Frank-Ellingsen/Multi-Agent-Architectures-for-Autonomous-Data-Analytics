from __future__ import annotations

import os
import shutil
import sys
import tempfile
from pathlib import Path
from typing import Any

from flask import Flask, jsonify, request, send_from_directory

ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT / 'src'))

from multi_agent_analytics.ai_agent import (  # noqa: E402
    generate_executive_narrative,
    test_llm_connection,
)
from multi_agent_analytics.analytics import compute_forecast_snapshot, compute_key_metrics  # noqa: E402
from multi_agent_analytics.dataset import SUPPORTED_EXTENSIONS, load_dataset_summary  # noqa: E402
from multi_agent_analytics.decision import generate_prescriptions, generate_prognosis  # noqa: E402
from multi_agent_analytics.relationships import validate_relationships  # noqa: E402
from multi_agent_analytics.reporting import build_markdown_report  # noqa: E402
from multi_agent_analytics.schema import summarize_schema  # noqa: E402
from multi_agent_analytics.workflow import DEFAULT_SKILLS  # noqa: E402

app = Flask(__name__, static_folder='static')

UNSEEN_DATA_DIR = ROOT / 'test_data' / 'unseen_businesses'

DEMO_DOMAINS = {
    'erp_default': {
        'id': 'erp_default',
        'title': 'Enterprise ERP & Financial Controlling',
        'format': 'Star Schema CSV (Semicolon)',
        'description': 'General Ledger (FactGL), Budget, Forecast, and FTE headcount star schema.',
        'files': ['FactGL.csv', 'FactBudget.csv', 'FactForecast.csv', 'FactFTE.csv', 'DimDate.csv', 'DimAccount.csv', 'Relationships.csv'],
    },
    'maritime_defense': {
        'id': 'maritime_defense',
        'title': 'Maritime & Naval Defense Shipbuilding',
        'format': 'Excel Workbook (.xlsx)',
        'description': 'Multi-sheet workbook with WBS Cost Control, EAC/ETC forecasts, composite hull hours, CPI/SPI, and milestone risk reserves.',
        'file': 'maritime_defense_vessel.xlsx',
    },
    'saas_subscription': {
        'id': 'saas_subscription',
        'title': 'Cloud SaaS & Subscription Analytics',
        'format': 'Tab-Separated Values (.tsv)',
        'description': 'B2B subscription customer metrics including MRR, ARR, churn risk score, CAC, LTV, and active seat counts.',
        'file': 'saas_subscription_platform.tsv',
    },
    'nordic_retail': {
        'id': 'nordic_retail',
        'title': 'Nordic Retail & Supply Chain Operations',
        'format': 'European Semicolon CSV (.csv)',
        'description': 'SKU level inventory, procurement costs, monthly turnover, gross margin percentages, and warehouse locations.',
        'file': 'nordic_retail_inventory.csv',
    },
    'offshore_marine': {
        'id': 'offshore_marine',
        'title': 'Offshore Energy & Drilling Fleet Operations',
        'format': 'Pipe-Separated Values (.psv)',
        'description': 'Vessel fleet operating day rates, fuel consumption, downtime hours, maintenance actuals vs budgets, and crew FTEs.',
        'file': 'offshore_marine_drilling.psv',
    },
    'hospital_kpis': {
        'id': 'hospital_kpis',
        'title': 'Regional Healthcare Trust Executive Report',
        'format': 'Structured Document (.pdf)',
        'description': 'Extracted clinical tabular report with hospital department admissions, bed occupancy, budgets, actual spend, and clinical staff FTE.',
        'file': 'hospital_executive_kpis.pdf',
    },
    'consulting': {
        'id': 'consulting',
        'title': 'Professional Consulting & Engineering Advisory',
        'format': 'Delimited Text (.txt)',
        'description': 'Client advisory engagements, billed fees, incurred hours, realization rate percentages, and partner portfolio tracking.',
        'file': 'management_consulting_engagements.txt',
    },
}


@app.before_request
def handle_options_preflight():
    if request.method == 'OPTIONS':
        res = app.make_default_options_response()
        res.headers['Access-Control-Allow-Origin'] = '*'
        res.headers['Access-Control-Allow-Headers'] = '*'
        res.headers['Access-Control-Allow-Methods'] = 'GET, POST, OPTIONS'
        res.headers['Access-Control-Allow-Private-Network'] = 'true'
        return res


@app.after_request
def add_cors_headers(response):
    response.headers['Access-Control-Allow-Origin'] = '*'
    response.headers['Access-Control-Allow-Headers'] = '*'
    response.headers['Access-Control-Allow-Methods'] = 'GET, POST, OPTIONS'
    response.headers['Access-Control-Allow-Private-Network'] = 'true'
    return response


@app.errorhandler(Exception)
def handle_unexpected_error(error):
    app.logger.exception('Backend analysis failed')
    return jsonify({'error': f'{type(error).__name__}: {error}'}), 500


@app.get('/')
def index():
    return send_from_directory(ROOT, 'index.html')


@app.get('/api/health')
def health():
    return jsonify({
        'status': 'healthy',
        'service': 'multi-agent-analytics',
        'version': '0.2.0',
        'skills_count': len(DEFAULT_SKILLS),
        'supported_extensions': list(SUPPORTED_EXTENSIONS),
    })


@app.get('/api/skills')
def get_skills():
    phase_map = {
        '01_': 'Phase I: Ingestion & Inspection',
        '02_': 'Phase I: Ingestion & Inspection',
        '03_': 'Phase I: Ingestion & Inspection',
        '04_': 'Phase I: Ingestion & Inspection',
        '05_': 'Phase II: Schema & Modeling',
        '06_': 'Phase II: Schema & Modeling',
        '07_': 'Phase II: Schema & Modeling',
        '08_': 'Phase II: Schema & Modeling',
        '09_': 'Phase II: Schema & Modeling',
        '10_': 'Phase II: Schema & Modeling',
        '11_': 'Phase III: Diagnostics & Metrics',
        '12_': 'Phase III: Diagnostics & Metrics',
        '13_': 'Phase III: Diagnostics & Metrics',
        '14_': 'Phase III: Diagnostics & Metrics',
        '15_': 'Phase III: Diagnostics & Metrics',
        '16_': 'Phase III: Diagnostics & Metrics',
        '17_': 'Phase IV: Prognostics & Simulation',
        '18_': 'Phase IV: Prognostics & Simulation',
        '19_': 'Phase IV: Prognostics & Simulation',
        '20_': 'Phase IV: Prognostics & Simulation',
        '21_': 'Phase IV: Prognostics & Simulation',
        '22_': 'Phase IV: Prognostics & Simulation',
        '23_': 'Phase V: Prescriptions & Optimization',
        '24_': 'Phase V: Prescriptions & Optimization',
        '25_': 'Phase V: Prescriptions & Optimization',
        '26_': 'Phase V: Prescriptions & Optimization',
        '27_': 'Phase VI: Storytelling & Publishing',
        '28_': 'Phase VI: Storytelling & Publishing',
        '29_': 'Phase VI: Storytelling & Publishing',
        '30_': 'Phase VI: Storytelling & Publishing',
    }

    catalog = []
    for skill in DEFAULT_SKILLS:
        prefix = skill.id[:3]
        phase = phase_map.get(prefix, 'Core Workflow')
        catalog.append({
            'id': skill.id,
            'title': skill.title,
            'description': skill.description,
            'phase': phase,
        })
    return jsonify({'skills': catalog})


@app.get('/api/demo-domains')
def get_demo_domains():
    return jsonify({'domains': list(DEMO_DOMAINS.values())})


def _analyze_directory(data_dir: Path) -> dict[str, Any]:
    metrics = compute_key_metrics(data_dir)
    snapshot = compute_forecast_snapshot(data_dir)
    return {
        'dataset_summary': load_dataset_summary(data_dir),
        'schema_summary': summarize_schema(data_dir),
        'relationship_summary': validate_relationships(data_dir),
        'metrics': metrics,
        'forecast_snapshot': snapshot,
        'prognosis': generate_prognosis(metrics),
        'prescriptions': generate_prescriptions(metrics),
        'report': build_markdown_report(data_dir),
    }


@app.post('/api/analyze')
def analyze():
    uploaded_files = request.files.getlist('files')
    if not uploaded_files:
        return jsonify({'error': 'Upload at least one file (CSV, TSV, TXT, PSV, Excel .xlsx, or PDF).'}), 400

    with tempfile.TemporaryDirectory(prefix='multi-agent-analytics-') as temp_dir:
        data_dir = Path(temp_dir)
        for uploaded in uploaded_files:
            filename = Path(uploaded.filename or '').name
            ext = Path(filename).suffix.lower()
            if not filename or ext not in SUPPORTED_EXTENSIONS:
                return jsonify({
                    'error': f"File '{filename}' has an unsupported format. Supported formats: {', '.join(SUPPORTED_EXTENSIONS)}"
                }), 400
            uploaded.save(data_dir / filename)

        result = _analyze_directory(data_dir)

        # Check if caller supplied credentials for optional on-the-fly narrative
        provider = request.headers.get('X-Provider') or request.form.get('provider')
        api_key = request.headers.get('X-Api-Key') or request.form.get('api_key')
        model = request.headers.get('X-Model') or request.form.get('model')
        endpoint = request.headers.get('X-Endpoint') or request.form.get('endpoint')

        if provider and (api_key or provider.lower() == 'ollama'):
            try:
                ai_result = generate_executive_narrative(
                    metrics=result['metrics'],
                    prognosis=result['prognosis'],
                    prescriptions=result['prescriptions'],
                    dataset_summary=result['dataset_summary'],
                    provider=provider,
                    api_key=api_key or '',
                    model=model,
                    base_url=endpoint,
                )
                result['ai_narrative'] = ai_result['narrative']
            except Exception as e:
                result['ai_narrative_error'] = str(e)

        return jsonify(result)


@app.post('/api/demo-data')
def load_demo():
    payload = request.get_json(silent=True) or {}
    domain_id = payload.get('domain') or request.args.get('domain', 'erp_default')

    if domain_id not in DEMO_DOMAINS or domain_id == 'erp_default':
        demo_dir = ROOT / 'test_data'
        if not demo_dir.exists():
            return jsonify({'error': 'Built-in demo data directory not found.'}), 404
        result = _analyze_directory(demo_dir)
        result['loaded_domain'] = DEMO_DOMAINS['erp_default']
        return jsonify(result)

    # Load specific unseen business domain file
    domain_meta = DEMO_DOMAINS[domain_id]
    target_filename = domain_meta['file']
    source_file = UNSEEN_DATA_DIR / target_filename
    if not source_file.exists():
        return jsonify({'error': f"Mock data file '{target_filename}' not found. Run generator script first."}), 404

    with tempfile.TemporaryDirectory(prefix=f'multi-agent-{domain_id}-') as temp_dir:
        dest_dir = Path(temp_dir)
        shutil.copy2(source_file, dest_dir / target_filename)
        result = _analyze_directory(dest_dir)
        result['loaded_domain'] = domain_meta
        return jsonify(result)


@app.post('/api/ai/test-key')
def api_test_key():
    data = request.get_json(silent=True) or {}
    provider = data.get('provider') or request.headers.get('X-Provider', 'gemini')
    api_key = data.get('api_key') or request.headers.get('X-Api-Key', '')
    model = data.get('model') or request.headers.get('X-Model')
    base_url = data.get('base_url') or request.headers.get('X-Endpoint')

    res = test_llm_connection(
        provider=provider,
        api_key=api_key,
        model=model,
        base_url=base_url,
    )
    status_code = 200 if res.get('ok') else 400
    return jsonify(res), status_code


@app.post('/api/ai/narrative')
def api_generate_narrative():
    data = request.get_json(silent=True) or {}
    metrics = data.get('metrics')
    if not metrics:
        return jsonify({'error': 'Missing metrics in request payload.'}), 400

    prognosis = data.get('prognosis') or generate_prognosis(metrics)
    prescriptions = data.get('prescriptions') or generate_prescriptions(metrics)
    dataset_summary = data.get('dataset_summary', {})

    provider = data.get('provider') or request.headers.get('X-Provider', 'gemini')
    api_key = data.get('api_key') or request.headers.get('X-Api-Key', '')
    model = data.get('model') or request.headers.get('X-Model')
    base_url = data.get('base_url') or request.headers.get('X-Endpoint')

    try:
        story = generate_executive_narrative(
            metrics=metrics,
            prognosis=prognosis,
            prescriptions=prescriptions,
            dataset_summary=dataset_summary,
            provider=provider,
            api_key=api_key,
            model=model,
            base_url=base_url,
        )
        return jsonify(story)
    except Exception as exc:
        return jsonify({'error': str(exc)}), 500


if __name__ == '__main__':
    port = int(os.getenv('PORT', 8000))
    host = os.getenv('HOST', '0.0.0.0')
    app.run(host=host, port=port, debug=True)
