import pathlib

content = r'''"""Boss Agent - LLM Decomposer tests (v0.2)."""

import sys
import os
import json

if sys.platform == "win32":
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    sys.stderr.reconfigure(encoding="utf-8", errors="replace")

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))

from boss_agent.decomposer import AgentType, _reset_counter
from boss_agent.llm_decomposer import _parse_response, decompose_with_llm
from boss_agent.llm_client import LLMResponse


class MockClient:
    def __init__(self, responses):
        self.responses = responses
        self._idx = 0

    @property
    def is_available(self):
        return True

    def chat(self, messages, **kwargs):
        if self._idx >= len(self.responses):
            return LLMResponse(content="", success=False, error="no more mock responses")
        resp = self.responses[self._idx]
        self._idx += 1
        return resp


def test_parse_simple_json():
    _reset_counter()
    raw = json.dumps({
        "summary": "echo hello",
        "subtasks": [{"description": "echo hello", "agent": "shell", "dependencies": []}]
    })
    plan = _parse_response(raw, "echo hello")
    assert len(plan.subtasks) == 1
    assert plan.subtasks[0].description == "echo hello"
    assert plan.subtasks[0].agent == AgentType.SHELL


def test_parse_multiple_subtasks():
    _reset_counter()
    raw = json.dumps({
        "summary": "multi step task",
        "subtasks": [
            {"description": "search for info", "agent": "researcher", "dependencies": []},
            {"description": "write a report", "agent": "coder", "dependencies": ["T001"]},
        ]
    })
    plan = _parse_response(raw, "search and write")
    assert len(plan.subtasks) == 2
    assert plan.subtasks[0].agent == AgentType.RESEARCHER
    assert plan.subtasks[1].agent == AgentType.CODER


def test_parse_markdown_fenced_json():
    _reset_counter()
    raw = '```json\n{"summary": "fenced", "subtasks": [{"description": "do thing", "agent": "shell", "dependencies": []}]}\n```'
    plan = _parse_response(raw, "fenced")
    assert len(plan.subtasks) == 1
    assert plan.subtasks[0].description == "do thing"


def test_parse_invalid_json_fallback():
    _reset_counter()
    raw = "this is not json"
    plan = _parse_response(raw, "fallback test")
    assert len(plan.subtasks) == 1
    assert plan.subtasks[0].description == "fallback test"
    assert plan.subtasks[0].agent == AgentType.SHELL


def test_decompose_llm_success():
    _reset_counter()
    mock = MockClient([
        LLMResponse(
            content=json.dumps({
                "summary": "single echo",
                "subtasks": [{"description": "echo hello", "agent": "shell", "dependencies": []}]
            }),
            success=True,
        ),
    ])
    plan = decompose_with_llm("echo hello", mock)
    assert len(plan.subtasks) == 1
    assert plan.subtasks[0].description == "echo hello"


def test_decompose_llm_failure_fallback():
    _reset_counter()
    mock = MockClient([
        LLMResponse(content="", success=False, error="API error"),
    ])
    plan = decompose_with_llm("echo hello", mock)
    assert len(plan.subtasks) >= 1


def test_decompose_llm_parse_error_fallback():
    _reset_counter()
    mock = MockClient([
        LLMResponse(content="not json at all", success=True),
    ])
    plan = decompose_with_llm("echo hello", mock)
    assert len(plan.subtasks) >= 1
'''

pathlib.Path(r'C:\Users\Tinkerclaw\.openclaw-autoclaw\workspace\boss-agent\tests\test_llm_decomposer.py').write_text(content, encoding='utf-8')
print("OK")
