"""Boss Agent - Executor tests (v0.2, pytest-style)."""

import sys
import os

if sys.platform == "win32":
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    sys.stderr.reconfigure(encoding="utf-8", errors="replace")

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))

from boss_agent.decomposer import decompose, _reset_counter, AgentType, SubTask
from boss_agent.executor import BossEngine, ShellExecutor


def test_shell_echo():
    ex = ShellExecutor()
    task = SubTask(id="T001", description="echo hello world", agent=AgentType.SHELL, dependencies=[])
    result = ex.execute(task)
    assert result.success, "should succeed"
    assert "hello world" in result.output


def test_shell_fail():
    ex = ShellExecutor()
    task = SubTask(id="T001", description="exit 1", agent=AgentType.SHELL, dependencies=[])
    result = ex.execute(task)
    assert not result.success, "should fail"


def test_engine_single_shell():
    _reset_counter()
    engine = BossEngine()
    plan = decompose("echo hello from boss")
    plan.subtasks[0].agent = AgentType.SHELL
    results = engine.execute_plan(plan)
    assert len(results) == 1
    assert results[0].success
    assert "hello from boss" in results[0].output


def test_engine_serial_tasks():
    _reset_counter()
    engine = BossEngine()
    plan = decompose("echo step1, 然后 echo step2")
    for st in plan.subtasks:
        st.agent = AgentType.SHELL
    results = engine.execute_plan(plan)
    assert len(results) == 2
    assert results[0].success
    assert results[1].success
