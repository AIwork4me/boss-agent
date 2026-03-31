"""
Boss Agent - Executor Tests
"""

import sys
import os

if sys.platform == "win32":
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    sys.stderr.reconfigure(encoding="utf-8", errors="replace")

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))

from boss_agent.decomposer import decompose, _reset_counter, AgentType, SubTask
from boss_agent.executor import BossEngine, ShellExecutor

passed = 0
failed = 0


def test(name, fn):
    global passed, failed
    _reset_counter()
    try:
        fn()
        print(f"  OK {name}")
        passed += 1
    except AssertionError as e:
        print(f"  FAIL {name}: {e}")
        failed += 1


def assert_eq(actual, expected, msg=""):
    if actual != expected:
        raise AssertionError(f"{msg}: expected {expected!r}, got {actual!r}")


def assert_true(condition, msg=""):
    if not condition:
        raise AssertionError(msg)


print("\n[Boss Agent] Executor Tests\n")


# ShellExecutor unit tests

def test_shell_echo():
    ex = ShellExecutor()
    task = SubTask(id="T001", description="echo hello world", agent=AgentType.SHELL, dependencies=[])
    result = ex.execute(task)
    assert_true(result.success, "should succeed")
    assert_true("hello world" in result.output, f"output should contain 'hello world', got: {result.output}")

test("shell executor: echo command", test_shell_echo)


def test_shell_fail():
    ex = ShellExecutor()
    task = SubTask(id="T001", description="exit 1", agent=AgentType.SHELL, dependencies=[])
    result = ex.execute(task)
    assert_true(not result.success, "should fail")

test("shell executor: failing command", test_shell_fail)


# BossEngine integration tests

def test_engine_single_shell():
    engine = BossEngine()
    plan = decompose("echo hello from boss")
    # Override agent type to shell for this test
    plan.subtasks[0].agent = AgentType.SHELL
    
    results = engine.execute_plan(plan)
    assert_eq(len(results), 1, "result count")
    assert_true(results[0].success, "should succeed")
    assert_true("hello from boss" in results[0].output, f"got: {results[0].output}")

test("engine: single shell task", test_engine_single_shell)


def test_engine_serial_tasks():
    engine = BossEngine()
    plan = decompose("echo step1, 然后 echo step2")
    # Override both to shell
    for st in plan.subtasks:
        st.agent = AgentType.SHELL
        st.description = f"echo {st.description}"
    
    results = engine.execute_plan(plan)
    assert_eq(len(results), 2, "result count")
    assert_true(results[0].success, "first should succeed")
    assert_true(results[1].success, "second should succeed")

test("engine: serial shell tasks", test_engine_serial_tasks)


def _test_claude_code():
    import shutil
    has_claude = shutil.which("claude") is not None
    if has_claude:
        print(f"    (claude found at {shutil.which('claude')})")
    else:
        print("    (claude not found - ClaudeCodeExecutor will be skipped)")
    assert_true(True, "detection check")

test("detect: Claude Code availability", _test_claude_code)


# Results
print(f"\n{'='*40}")
print(f"Passed: {passed} | Failed: {failed}")
if failed == 0:
    print("All tests passed!")
else:
    print("Some tests failed!")
    sys.exit(1)
