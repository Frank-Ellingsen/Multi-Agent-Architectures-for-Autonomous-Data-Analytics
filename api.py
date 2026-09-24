from __future__ import annotations

import sys
import tempfile
from pathlib import Path

from flask import Flask, jsonify, request, send_from_directory

ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT / 'src'))

from multi_agent_analytics.analytics import compute_key_metrics  # noqa: E402
from multi_agent_analytics.decision import generate_prescriptions, generate_prognosis  # noqa: E402
from multi_agent_analytics.dataset import load_dataset_summary  # noqa: E402
from multi_agent_analytics.relationships import validate_relationships  # noqa: E402
from multi_agent_analytics.reporting import build_markdown_report  # noqa: E402
from multi_agent_analytics.schema import summarize_schema  # noqa: E402

app = Flask(__name__, static_folder='static')


@app.after_request
def add_cors_headers(response):
    response.headers['Access-Control-Allow-Origin'] = '*'
    response.headers['Access-Control-Allow-Headers'] = 'Content-Type'
    response.headers['Access-Control-Allow-Methods'] = 'GET, POST, OPTIONS'
    return response


@app.errorhandler(Exception)
def handle_unexpected_error(error):
    app.logger.exception('Backend analysis failed')
    return jsonify({'error': f'{type(error).__name__}: {error}'}), 500


@app.get('/')
def index():
    return send_from_directory(ROOT, 'index.html')


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

        metrics = compute_key_metrics(data_dir)
        return jsonify({
            'dataset_summary': load_dataset_summary(data_dir),
            'schema_summary': summarize_schema(data_dir),
            'relationship_summary': validate_relationships(data_dir),
            'metrics': metrics,
            'prognosis': generate_prognosis(metrics),
            'prescriptions': generate_prescriptions(metrics),
            'report': build_markdown_report(data_dir),
        })


if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8000, debug=True)
