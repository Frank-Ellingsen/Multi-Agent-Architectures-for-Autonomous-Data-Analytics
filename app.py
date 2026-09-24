from __future__ import annotations

import json
import os
import tempfile
from pathlib import Path

import streamlit as st

from multi_agent_analytics.ai_agent import generate_executive_narrative, test_llm_connection
from multi_agent_analytics.analytics import compute_key_metrics
from multi_agent_analytics.dataset import load_dataset_summary
from multi_agent_analytics.decision import generate_prescriptions, generate_prognosis
from multi_agent_analytics.relationships import validate_relationships
from multi_agent_analytics.reporting import build_markdown_report
from multi_agent_analytics.schema import summarize_schema
from multi_agent_analytics.workflow import DEFAULT_SKILLS

st.set_page_config(page_title='Multi-Agent Analytics Studio', layout='wide')
st.title('Multi-Agent Analytics Studio')

ROOT = Path(__file__).resolve().parent

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
    use_demo = st.checkbox('Use built-in Demo ERP Dataset', value=False)

uploaded_files = []
if not use_demo:
    uploaded_files = st.file_uploader(
        'Upload analytics CSV files',
        type=['csv'],
        accept_multiple_files=True,
    )
    if not uploaded_files:
        st.info('Upload one or more CSV files or check "Use built-in Demo ERP Dataset" in the sidebar to start.')
        st.stop()

with tempfile.TemporaryDirectory() as temp_dir:
    temp_path = Path(temp_dir)
    if use_demo:
        demo_dir = ROOT / 'test_data'
        for f in demo_dir.glob('*.csv'):
            (temp_path / f.name).write_bytes(f.read_bytes())
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

    if menu == 'Upload & Diagnostics':
        st.subheader('Key Financial Metrics')
        c1, c2, c3, c4 = st.columns(4)
        c1.metric("Actual Total", f"{metrics['actual_total']:,.2f}")
        c2.metric("Budget Total", f"{metrics['budget_total']:,.2f}")
        c3.metric("Forecast Total", f"{metrics['forecast_total']:,.2f}")
        c4.metric(
            "Variance to Budget",
            f"{metrics['variance_to_budget']:,.2f}",
            delta=f"{metrics['variance_to_budget']:,.2f}",
            delta_color="normal"
        )

        st.subheader('Diagnostics Report')
        st.code(report, language='markdown')

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
        st.subheader('Prognostic Scenarios')
        st.dataframe(
            [{
                'scenario': name.capitalize(),
                'actual_total': f"{float(info['actual_total']):,.2f}",
                'expected_total': f"{float(info['expected_total']):,.2f}",
                'variance_vs_budget': f"{float(info['variance_vs_budget']):,.2f}",
            } for name, info in prognosis.items()],
            use_container_width=True,
        )

    elif menu == 'Prescriptions':
        st.subheader('Recommended Actions')
        for item in prescriptions:
            with st.expander(str(item['title'])):
                st.write(item['description'])
                st.write(f"**Quantified Outcome:** {item['expected_result']}")
                st.write(f"**Impact score:** {float(item['impact_score'])*100:.0f}%")

    elif menu == 'AI Decision Story':
        st.subheader('AI Executive Decision Narrative')
        st.caption('Synthesizes an executive story using your configured LLM API key.')
        if st.button('Generate Narrative'):
            with st.spinner(f'Synthesizing decision story via {provider.upper()}...'):
                try:
                    narrative_res = generate_executive_narrative(
                        metrics=metrics,
                        prognosis=prognosis,
                        prescriptions=prescriptions,
                        dataset_summary=dataset_summary,
                        provider=provider,
                        api_key=api_key,
                        model=model,
                        base_url=endpoint,
                    )
                    st.markdown(narrative_res['narrative'])
                except Exception as e:
                    st.error(f"Error generating narrative: {e}")

    elif menu == '30-Skill Catalog':
        st.subheader('Autonomous Analytics Skills Catalog')
        for skill in DEFAULT_SKILLS:
            with st.expander(f"{skill.id} - {skill.title}"):
                st.write(skill.description)
