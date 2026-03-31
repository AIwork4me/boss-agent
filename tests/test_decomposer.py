"""Boss Agent - Decomposer tests (v0.2, pytest-style)."""

import sys
import os

if sys.platform == "win32":
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    sys.stderr.reconfigure(encoding="utf-8", errors="replace")

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))

from boss_agent.decomposer import decompose, _reset_counter


def test_single_task():
    _reset_counter()
    plan = decompose("echo hello")
    assert len(plan.subtasks) == 1
    assert plan.subtasks[0].description == "echo hello"


def test_single_coder():
    _reset_counter()
    plan = decompose("implement a fibonacci function")
    assert len(plan.subtasks) == 1
    assert plan.subtasks[0].agent.value == "coder"


def test_single_researcher():
    _reset_counter()
    plan = decompose("research the latest AI trends")
    assert len(plan.subtasks) == 1
    assert plan.subtasks[0].agent.value == "researcher"


def test_compound_two():
    _reset_counter()
    plan = decompose("echo step 1, then echo step 2")
    assert len(plan.subtasks) == 2
    assert len(plan.subtasks[0].dependencies) == 0
    assert plan.subtasks[0].id in plan.subtasks[1].dependencies


def test_compound_three():
    _reset_counter()
    plan = decompose("echo a, then echo b, then echo c")
    assert len(plan.subtasks) == 3
    assert len(plan.subtasks[0].dependencies) == 0


def test_original_preserved():
    _reset_counter()
    input_text = "research the market and write a report"
    plan = decompose(input_text)
    assert plan.original == input_text
