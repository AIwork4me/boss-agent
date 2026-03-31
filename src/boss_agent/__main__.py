"""
Boss Agent - CLI Entry Point

Usage:
  python -m boss_agent "你的任务描述"

Example:
  python -m boss_agent "echo hello world"
  python -m boss_agent "echo step1, 然后 echo step2"
"""

import sys
import time

if sys.platform == "win32":
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    sys.stderr.reconfigure(encoding="utf-8", errors="replace")

from boss_agent.decomposer import decompose, AgentType
from boss_agent.executor import BossEngine


def main():
    if len(sys.argv) < 2:
        print("Boss Agent v0.1.0")
        print()
        print("Usage:")
        print('  python -m boss_agent "your task description"')
        print()
        print("Examples:")
        print('  python -m boss_agent "echo hello world"')
        print('  python -m boss_agent "echo step1, then echo step2"')
        print('  python -m boss_agent "dir, then echo done"')
        sys.exit(0)

    user_input = " ".join(sys.argv[1:])

    print()
    print("=" * 50)
    print("  Boss Agent v0.1.0")
    print("=" * 50)
    print()
    print(f"  [Boss] Task received: {user_input}")
    print()

    # Step 1: Decompose
    print("  [Boss] Decomposing task...")
    plan = decompose(user_input)

    print(f"  [Boss] Plan: {len(plan.subtasks)} subtask(s)")
    for task in plan.subtasks:
        deps = f" (after {', '.join(task.dependencies)})" if task.dependencies else ""
        print(f"    [{task.id}] [{task.agent.value:12s}] {task.description}{deps}")
    print()

    # Step 2: Execute
    print("  [Boss] Executing...")
    print("-" * 50)

    # Override: for v0.1, treat all tasks as shell commands
    # (LLM-powered agents coming in v0.2)
    for task in plan.subtasks:
        task.agent = AgentType.SHELL

    engine = BossEngine()
    start_time = time.time()
    results = engine.execute_plan(plan)
    total_ms = int((time.time() - start_time) * 1000)

    print("-" * 50)
    print()

    # Step 3: Report
    success_count = sum(1 for r in results if r.success)
    fail_count = len(results) - success_count

    print(f"  [Boss] Results: {success_count} ok, {fail_count} failed ({total_ms}ms)")
    print()

    for result in results:
        status = "OK" if result.success else "FAIL"
        print(f"  [{result.task_id}] {status}")
        if result.output and result.output.strip():
            # Show first 500 chars of output
            output = result.output.strip()[:500]
            for line in output.split("\n"):
                print(f"    {line}")
        if result.error:
            print(f"    ERROR: {result.error[:200]}")
        print()

    # Final summary
    if fail_count == 0:
        print("  All tasks completed successfully.")
    else:
        print(f"  WARNING: {fail_count} task(s) failed.")
    print()


if __name__ == "__main__":
    main()
