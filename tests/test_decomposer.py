"""
Boss Agent - 任务拆解器测试
"""

import sys
import os

# Windows 编码修复
if sys.platform == "win32":
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    sys.stderr.reconfigure(encoding="utf-8", errors="replace")

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))

from boss_agent.decomposer import decompose, _reset_counter

passed = 0
failed = 0


def test(name: str, fn):
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


# ========== Tests ==========

print("\n[Boss Agent] Decomposer Tests\n")


def test_single_coder():
    plan = decompose("写一个任务调度器")
    assert_eq(len(plan.subtasks), 1, "subtask count")
    assert_eq(plan.subtasks[0].agent.value, "coder", "agent type")
    assert_eq(len(plan.subtasks[0].dependencies), 0, "no deps")

test("single coding task -> coder", test_single_coder)


def test_single_researcher():
    plan = decompose("调研 GitHub Trending 的规律")
    assert_eq(len(plan.subtasks), 1, "subtask count")
    assert_eq(plan.subtasks[0].agent.value, "researcher", "agent type")

test("single research task -> researcher", test_single_researcher)


def test_compound_two():
    plan = decompose("调研 GitHub Trending 的规律，然后写一份分析报告")
    assert_eq(len(plan.subtasks), 2, "subtask count")
    assert_eq(plan.subtasks[0].agent.value, "researcher", "first agent")
    assert_eq(plan.subtasks[1].agent.value, "coder", "second agent")
    assert_true("T001" in plan.subtasks[1].dependencies, "second depends on first")

test("compound: research + code -> 2 serial subtasks", test_compound_two)


def test_compound_three():
    plan = decompose("调研竞品分析，然后实现一个原型，并且写测试")
    assert_eq(len(plan.subtasks), 3, "subtask count")
    assert_eq(len(plan.subtasks[0].dependencies), 0, "first has no deps")
    assert_true("T001" in plan.subtasks[1].dependencies, "second depends on first")
    assert_true("T002" in plan.subtasks[2].dependencies, "third depends on second")

test("compound: 3 steps -> 3 serial subtasks", test_compound_three)


def test_original_preserved():
    input_text = "帮我调研市场然后写报告"
    plan = decompose(input_text)
    assert_eq(plan.original, input_text, "original input")

test("original input preserved", test_original_preserved)


# Results
print(f"\n{'='*40}")
print(f"Passed: {passed} | Failed: {failed}")
if failed == 0:
    print("All tests passed!")
else:
    print("Some tests failed!")
    sys.exit(1)
