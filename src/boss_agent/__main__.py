"""
Boss Agent - CLI Entry Point (v0.2)

Usage:
  python -m boss_agent "your task description"
  python -m boss_agent --llm   # use LLM-powered decomposition

Environment variables:
  BOSS_LLM_API_KEY   - API key for LLM provider (required for LLM mode)
  BOSS_LLM_BASE_URL   - Base URL for LLM provider (default: OpenAI API)
  BOSS_LLM_MODEL    - Model name (default: gpt-4o1-mini)
"""

import sys
import time

if sys.platform == "win32":
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    sys.stderr.reconfigure(encoding="utf-8", errors="replace")

from boss_agent.decomposer import decompose, AgentType
from boss_agent.llm_decomposer import decompose_with_llm
from boss_agent.llm_client import LLMClient, LLMConfig
from boss_agent.executor import BossEngine


def _get_llm_config():
    import os
    api_key = os.environ.get("BOSS_LLM_API_KEY", "")
    if not api_key:
        return None
    base_url = os.environ.get("BOSS_LLM_BASE_URL", "https://api.openai.com/v1")
    model = os.environ.get("BOSS_LLM_MODEL", "gpt-4.1-mini")
    return LLMConfig(
        api_key=api_key,
        base_url=base_url,
        model=model,
    )


def main():
    if len(sys.argv) < 2:
        print("Boss Agent v0.2.0")
        print()
        print("Usage:")
        print('  python -m boss_agent "your task description"')
        print()
        print("Environment variables for LLM mode:")
        print("  BOSS_LLM_API_KEY  - API key for LLM provider")
        print("  BOSS_LLM_BASE_URL - Base URL (default: OpenAI API)")
        print("  BOSS_LLM_MODEL    - Model name (default: gpt-4.1-mini)")
        print()
        print("Without BOSS_LLM_API_KEY, runs in rule-based mode (v0.1).")
        sys.exit(0)

    user_input = " ".join(sys.argv[1:])

    print()
    print("=" * 50)
    print("  Boss Agent v0.2.0")
    print("=" * 50)
    print()
    print(f"  [Boss] Task received: {user_input}")
    print()

    # Step 1: Decompose
    llm_config = _get_llm_config()

    if llm_config:
        print("  [Boss] Decomposing (LLM mode)...")
        client = LLMClient(llm_config)
        plan = decompose_with_llm(user_input, client)
    else:
        print("  [Boss] Decomposing (rule-based mode)...")
        plan = decompose(user_input)

    print(f"  [Boss] Plan: {len(plan.subtasks)} subtask(s)")
    for task in plan.subtasks:
        deps = f" (after {', '.join(task.dependencies)})" if task.dependencies else ""
        print(f"    [{task.id}] [{task.agent.value:12s}] {task.description}{deps}")
    print()

    # Step 2: Execute
    print("  [Boss] Executing...")
    print("-" * 50)

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
            output = result.output.strip()[:500]
            for line in output.split("\n"):
                print(f"    {line}")
        if result.error:
            print(f"    ERROR: {result.error[:200]}")
        print()

    if fail_count == 0:
        print("  All tasks completed successfully.")
    else:
        print(f"  WARNING: {fail_count} task(s) failed.")
    print()


if __name__ == "__main__":
    main()
