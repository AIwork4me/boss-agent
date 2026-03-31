"""Boss Agent - LLM Decomposer tests (v0.2)."""

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


def test_parse_with_1based_deps():
    _reset_counter()
    raw = json.dumps({
        "summary": "two steps",
        "subtasks": [
            {"description": "step 1", "agent": "shell", "dependencies": []},
            {"description": "step 2", "agent": "shell", "dependencies": [1]},
        ]
    })
    plan = _parse_response(raw, "two steps")
    assert len(plan.subtasks) == 2
    # Dependency [1] should be remapped to T001
    assert plan.subtasks[0].id in plan.subtasks[1].dependencies
    assert plan.subtasks[0].id == "T001"


def test_parse_with_chain_deps():
    _reset_counter()
    raw = json.dumps({
        "summary": "three steps",
        "subtasks": [
            {"description": "search info", "agent": "researcher", "dependencies": []},
            {"description": "write code", "agent": "coder", "dependencies": [1]},
            {"description": "review code", "agent": "reviewer", "dependencies": [2]},
        ]
    })
    plan = _parse_response(raw, "three steps")
    assert len(plan.subtasks) == 3
    assert plan.subtasks[0].agent == AgentType.RESEARCHER
    assert plan.subtasks[1].agent == AgentType.CODER
    assert plan.subtasks[2].agent == AgentType.REVIEWER
    # Chain: T002 depends on T001, T003 depends on T002
    assert plan.subtasks[0].id in plan.subtasks[1].dependencies
    assert plan.subtasks[1].id in plan.subtasks[2].dependencies


def test_parse_markdown_fenced():
    _reset_counter()
    raw = '```json\n{"summary": "fenced", "subtasks": [{"description": "do thing", "agent": "shell", "dependencies": []}]}\n```'
    plan = _parse_response(raw, "fenced")
    assert len(plan.subtasks) == 1
    assert plan.subtasks[0].description == "do thing"


def test_parse_invalid_json_fallback():
    _reset_counter()
    try:
        plan = _parse_response("this is not json", "fallback test")
        assert False, "Should have raised exception"
    except (json.JSONDecodeError, ValueError):
        pass  # Expected


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
