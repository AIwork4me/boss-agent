"""Boss Agent - LLM Client tests (v0.2, pytest-style)."""

import sys
import os
import json

if sys.platform == "win32":
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    sys.stderr.reconfigure(encoding="utf-8", errors="replace")

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))

from boss_agent.llm_client import LLMClient, LLMConfig, LLMMessage, LLMResponse


def test_llm_config_defaults():
    config = LLMConfig()
    assert config.api_key == ""
    assert config.base_url == "https://api.openai.com/v1"
    assert config.model == "gpt-4o-mini"
    assert config.temperature == 0.3


def test_llm_config_from_env(monkeypatch):
    monkeypatch.setenv("BOSS_LLM_API_KEY", "test-key-123")
    monkeypatch.setenv("BOSS_LLM_BASE_URL", "https://api.example.com/v1")
    monkeypatch.setenv("BOSS_LLM_MODEL", "test-model")
    config = LLMClient._load_config()
    assert config.api_key == "test-key-123"
    assert config.base_url == "https://api.example.com/v1"
    assert config.model == "test-model"


def test_llm_not_available_without_key():
    client = LLMClient(LLMConfig(api_key=""))
    assert not client.is_available


def test_llm_available_with_key():
    client = LLMClient(LLMConfig(api_key="sk-test-key"))
    assert client.is_available


def test_llm_chat_without_key():
    client = LLMClient(LLMConfig(api_key=""))
    response = client.chat([LLMMessage(role="user", content="hello")])
    assert not response.success
    assert "no API key" in response.error
