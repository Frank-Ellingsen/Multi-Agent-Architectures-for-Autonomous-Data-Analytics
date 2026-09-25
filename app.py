from __future__ import annotations

import json
import os
import shutil
import tempfile
from pathlib import Path

import streamlit as st

from multi_agent_analytics.ai_agent import generate_executive_narrative, test_llm_connection
from multi_agent_analytics.analytics import compute_key_metrics
from multi_agent_analytics.dataset import SUPPORTED_EXTENSIONS, load_dataset_summary
from multi_agent_analytics.decision import generate_prescriptions, generate_prognosis
from multi_agent_analytics.relationships import validate_relationships
from multi_agent_analytics.reporting import build_markdown_report
from multi_agent_analytics.schema import summarize_schema
from multi_agent_analytics.workflow import DEFAULT_SKILLS

st.set_page_config(page_title='Multi-Agent Analytics Studio', layout='wide')
st.title('Multi-Agent Analytics Studio')

ROOT = Path(__file__).resolve().parent
UNSEEN_DATA_DIR = ROOT / 'test_data' / 'unseen_businesses'

DEMO_CHOICES = {
    'Built-in Demo ERP (Star Schema CSV)': 'erp_default',
    'Maritime Defense Shipbuilding (Excel .xlsx)': 'maritime_defense_vessel.xlsx',
    'Cloud SaaS & Subscription (Tab .tsv)': 'saas_subscription_platform.tsv',
    'Nordic Retail & Margin (Semicolon .csv)': 'nordic_retail_inventory.csv',
    'Offshore Drilling Operations (Pipe .psv)': 'offshore_marine_drilling.psv',
    'Hospital Clinical Performance (PDF Document .pdf)': 'hospital_executive_kpis.pdf',
    'Consulting Engagements (Text .txt)': 'management_consulting_engagements.txt',
}

with st.sidebar:
    st.header('Navigation')
    menu = st.radio(
        'Menu',
        ['Upload & Diagnostics', 'Prognostics', 'Prescriptions', 'AI Decision Story', '30-Skill Catalog']
    )

    st.markdown('---')
    st.subheader('Model & API Settings')
    provider = st.selectbox('LLM Provider', ['gemini', 'openai', 'anthropic', 'ollama'], index=0)
    api_key = st.text_input(
        'API Key',
        type='password',
        value=os.getenv(f"{provider.upper()}_API_KEY", ""),
        help="Input your LLM API Key. For Ollama, leave blank."
    )
    model = st.text_input(
        'Model Name',
        value='gemini-2.5-flash' if provider == 'gemini' else ('gpt-4o-mini' if provider == 'openai' else ('claude-3-5-sonnet-20241022' if provider == 'anthropic' else 'llama3.2'))
    )
    endpoint = ""
    if provider == 'ollama':
        endpoint = st.text_input('Ollama Endpoint', value='http://localhost:11434')

    if st.button('Test Connection'):
        with st.spinner('Testing LLM connectivity...'):
            res = test_llm_connection(provider, api_key, model, endpoint)
            if res.get('ok'):
                st.success(res.get('message', 'Connected!'))
            else:
                st.error(res.get('error', 'Connection failed.'))

    st.markdown('---')
    st.subheader('Demo Datasets (Multi-Business)')
    use_demo = st.checkbox('Load Pre-built Business Dataset', value=False)
    selected_demo = 'erp_default'
    if use_demo:
        demo_label = st.selectbox('Select Business & Format', list(DEMO_CHOICES.keys()))
        selected_demo = DEMO_CHOICES[demo_label]

uploaded_files = []
if not use_demo:
    allowed_types = [ext.lstrip('.') for ext in SUPPORTED_EXTENSIONS]
    uploaded_files = st.file_uploader(
        'Upload analytics files (Excel, TSV, Semicolon CSV, Pipe PSV, PDF, TXT)',
        type=allowed_types,
        accept_multiple_files=True,
    )
    if not uploaded_files:
        st.info('Upload one or more files (CSV, TSV, TXT, PSV, Excel .xlsx, or PDF) or check "Load Pre-built Business Dataset" in the sidebar to start.')
        st.stop()

with tempfile.TemporaryDirectory() as temp_dir:
    temp_path = Path(temp_dir)
    if use_demo:
        if selected_demo == 'erp_default':
            demo_dir = ROOT / 'test_data'
            for f in demo_dir.glob('*.csv'):
                (temp_path / f.name).write_bytes(f.read_bytes())
        else:
            source_file = UNSEEN_DATA_DIR / selected_demo
            if source_file.exists():
                shutil.copy2(source_file, temp_path / selected_demo)
    else:
        for uploaded in uploaded_files:
            destination = temp_path / uploaded.name
            destination.write_bytes(uploaded.getvalue())

    dataset_summary = load_dataset_summary(temp_path)
    schema_summary = summarize_schema(temp_path)
    relationship_summary = validate_relationships(temp_path)
    metrics = compute_key_metrics(temp_path)
    report = build_markdown_report(temp_path)
    prognosis = generate_prognosis(metrics)
    prescriptions = generate_prescriptions(metrics)

    domain = metrics.get('domain', 'Enterprise Financial Controlling')
    currency = metrics.get('currency', 'NOK')

    if menu == 'Upload & Diagnostics':
        st.caption(f"Recognized Business Domain: **{domain}** | Currency: **{currency}**")
        st.subheader('Key Financial & Operational Metrics')
        c1, c2, c3, c4 = st.columns(4)
        c1.metric("Actual / Primary Total", f"{metrics['actual_total']:,.2f} {currency}")
        c2.metric("Budget / Baseline Total", f"{metrics['budget_total']:,.2f} {currency}")
        c3.metric("Forecast / EAC Total", f"{metrics['forecast_total']:,.2f} {currency}")
        c4.metric(
            "Variance to Budget",
            f"{metrics['variance_to_budget']:,.2f} {currency}",
            delta=f"{metrics['variance_to_budget']:,.2f}",
            delta_color="normal"
        )

        st.subheader('Diagnostics & Executive Report')
        st.markdown(report)

        st.subheader('Dataset Footprint & Extracted Entities')
        summary_rows = []
        for name, info in dataset_summary.items():
            if name.endswith('.csv') and any(k == name[:-4] for k in dataset_summary):
                continue
            summary_rows.append({
                'table_or_file': name,
                'rows': info['row_count'],
                'columns': info['column_count'],
                'format': info.get('format', 'unknown'),
                'source': info.get('source_file', name),
            })
        st.dataframe(summary_rows, use_container_width=True)

        st.subheader('Inferred Schema & Data Types')
        st.json(schema_summary)

    elif menu == 'Prognostics':
        st.subheader(f'Prognostic Scenarios - {domain}')
        st.dataframe([
            {'scenario': name.capitalize(), 'actual': f"{data['actual_total']:,.2f}", 'expected': f"{data['expected_total']:,.2f}", 'variance_vs_budget': f"{data['variance_vs_budget']:,.2f}"}
            for name, data in prognosis.items()
        ], use_container_width=True)

    elif menu == 'Prescriptions':
        st.subheader(f'Prescriptive Action Portfolio - {domain}')
        for action in prescriptions:
            with st.expander(f"⭐ {action['title']} (Impact Score: {action['impact_score']})", expanded=True):
                st.write(action['description'])
                st.info(f"Expected Business Outcome: {action['expected_result']}")

    elif menu == 'AI Decision Story':
        st.subheader('Autonomous AI Executive Decision Narrative')
        if st.button('Generate Executive Decision Story'):
            with st.spinner('Synthesizing executive intelligence across multi-agent phases...'):
                try:
                    res = generate_executive_narrative(
                        metrics=metrics,
                        prognosis=prognosis,
                        prescriptions=prescriptions,
                        dataset_summary=dataset_summary,
                        provider=provider,
                        api_key=api_key,
                        model=model,
                        base_url=endpoint,
                    )
                    st.markdown(res.get('narrative', ''))
                except Exception as e:
                    st.error(f"Failed to generate story: {e}")

    elif menu == '30-Skill Catalog':
        st.subheader('Autonomous Analytics 30-Skill Operational Catalog')
        for skill in DEFAULT_SKILLS:
            st.markdown(f"**{skill.id} - {skill.title}**: {skill.description}")
