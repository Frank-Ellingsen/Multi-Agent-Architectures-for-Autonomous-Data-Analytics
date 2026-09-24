from multi_agent_analytics.ai_agent import (
    DEFAULT_MODELS,
    check_llm_connection,
    get_default_model,
)


def test_default_model_selection():
    assert get_default_model('gemini') == 'gemini-1.5-flash'
    assert get_default_model('openai') == 'gpt-4o-mini'
    assert get_default_model('anthropic') == 'claude-3-5-sonnet-20241022'
    assert get_default_model('ollama') == 'llama3.2'


def test_connection_without_key_reports_missing_key():
    res = check_llm_connection(provider='gemini', api_key='')
    assert res['ok'] is False
    assert 'Missing API key' in res['error']

    res_openai = check_llm_connection(provider='openai', api_key='')
    assert res_openai['ok'] is False
    assert 'Missing API key' in res_openai['error']
