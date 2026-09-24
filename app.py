from __future__ import annotations

import json
import tempfile
from pathlib import Path

import streamlit as st

from multi_agent_analytics.analytics import compute_key_metrics
from multi_agent_analytics.dataset import load_dataset_summary
from multi_agent_analytics.decision import generate_prescriptions, generate_prognosis
from multi_agent_analytics.relationships import validate_relationships
from multi_agent_analytics.reporting import build_markdown_report
from multi_agent_analytics.schema import summarize_schema

st.set_page_config(page_title='Multi-Agent Analytics', layout='wide')
st.title('Multi-Agent Analytics Studio')

with st.sidebar:
    st.header('Navigation')
    menu = st.radio('Menu', ['Upload & Diagnostics', 'Prognostics', 'Prescriptions'])

uploaded_files = st.file_uploader(
    'Upload analytics CSV files',
    type=['csv'],
    accept_multiple_files=True,
)

if not uploaded_files:
    st.info('Upload one or more CSV files to start diagnostics.')
    st.stop()

with tempfile.TemporaryDirectory() as temp_dir:
    temp_path = Path(temp_dir)
    for uploaded in uploaded_files:
        destination = temp_path / uploaded.name
        destination.write_bytes(uploaded.getvalue())

    dataset_summary = load_dataset_summary(temp_path)
    schema_summary = summarize_schema(temp_path)
    relationship_summary = validate_relationships(temp_path)
    metrics = compute_key_metrics(temp_path)
    report = build_markdown_report(temp_path)

    if menu == 'Upload & Diagnostics':
        st.subheader('Diagnostics Report')
        st.write(report)

        st.subheader('Dataset Summary')
        st.dataframe(
            [{
                'file': name,
                'rows': info['row_count'],
                'columns': info['column_count'],
            } for name, info in dataset_summary.items()],
            use_container_width=True,
        )

        st.subheader('Relationship Check')
        st.json({
            'relationship_count': relationship_summary['relationship_count'],
            'valid': relationship_summary['valid'],
            'issues': relationship_summary['issues'],
        })

    elif menu == 'Prognostics':
        st.subheader('Prognostics')
        prognosis = generate_prognosis(metrics)
        st.json(prognosis)

        st.dataframe(
            [{
                'scenario': name,
                'actual_total': float(info['actual_total']),
                'expected_total': float(info['expected_total']),
                'variance_vs_budget': float(info['variance_vs_budget']),
            } for name, info in prognosis.items()],
            use_container_width=True,
        )

    elif menu == 'Prescriptions':
        st.subheader('Recommended Actions')
        prescriptions = generate_prescriptions(metrics)
        for item in prescriptions:
            with st.expander(str(item['title'])):
                st.write(item['description'])
                st.write(f"Expected result: {item['expected_result']}")
                st.write(f"Impact score: {item['impact_score']}")

        st.subheader('Expected Result Summary')
        st.json({
            'metrics': metrics,
            'prognosis': generate_prognosis(metrics),
            'prescriptions': prescriptions,
        })
