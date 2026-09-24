from __future__ import annotations

import os
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
from multi_agent_analytics.dataset import load_dataset_summary  # noqa: E402
from multi_agent_analytics.decision import generate_prescriptions, generate_prognosis  # noqa: E402
from multi_agent_analytics.relationships import validate_relationships  # noqa: E402
from multi_agent_analytics.reporting import build_markdown_report  # noqa: E402
from multi_agent_analytics.schema import summarize_schema  # noqa: E402
from multi_agent_analytics.workflow import DEFAULT_SKILLS  # noqa: E402

app = Flask(__name__, static_folder='static')


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
        'version': '0.1.0',
        'skills_count': len(DEFAULT_SKILLS),
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
        return jsonify({'error': 'Upload at least one CSV file.'}), 400

    with tempfile.TemporaryDirectory(prefix='multi-agent-analytics-') as temp_dir:
        data_dir = Path(temp_dir)
        for uploaded in uploaded_files:
            filename = Path(uploaded.filename or '').name
            if not filename or not filename.lower().endswith('.csv'):
                return jsonify({'error': 'Only CSV files are supported.'}), 400
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
    demo_dir = ROOT / 'test_data'
    if not demo_dir.exists():
        return jsonify({'error': 'Built-in demo data directory not found.'}), 404
    result = _analyze_directory(demo_dir)
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
