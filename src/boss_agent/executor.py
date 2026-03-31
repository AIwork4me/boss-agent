"""Boss Agent - Execution Engine

Core responsibility: receive decomposed subtasks, dispatch to the best agent.

Liu Bang's philosophy: send the strongest person for each domain.
"""

from __future__ import annotations

import json
import subprocess
import shutil
import urllib.request
import urllib.parse
import urllib.error
import os
import sys
from dataclasses import dataclass
from typing import Optional

from .decomposer import SubTask, AgentType


@dataclass
class ExecutionResult:
    task_id: str
    success: bool
    output: str
    error: Optional[str] = None
    duration_ms: int = 0


class ShellExecutor:
    """Shell command executor - the most basic execution capability."""

    def can_handle(self, task: SubTask) -> bool:
        return task.agent == AgentType.SHELL

    def execute(self, task: SubTask, context: dict | None = None) -> ExecutionResult:
        try:
            result = subprocess.run(
                task.description,
                shell=True,
                capture_output=True,
                text=True,
                timeout=120,
                encoding="utf-8",
                errors="replace",
            )
            return ExecutionResult(
                task_id=task.id,
                success=result.returncode == 0,
                output=result.stdout[-2000:] if len(result.stdout) > 2000 else result.stdout,
                error=result.stderr[-1000:] if result.stderr else None,
            )
        except subprocess.TimeoutExpired:
            return ExecutionResult(
                task_id=task.id,
                success=False,
                output="",
                error="Command timed out (120s)",
            )
        except Exception as e:
            return ExecutionResult(
                task_id=task.id,
                success=False,
                output="",
                error=str(e),
            )


class CoderExecutor:
    """Coding executor - uses LLM API for code generation.

    Falls back to Claude Code CLI if available, then to shell.
    Priority: LLM API > Claude Code CLI > shell fallback.
    """

    def __init__(self):
        self.claude_path = shutil.which("claude")
        self._llm_client = None

    def _get_llm_client(self):
        """Lazy-init LLM client from environment variables."""
        if self._llm_client is not None:
            return self._llm_client

        from .llm_client import LLMClient, LLMConfig
        import os

        api_key = os.environ.get("BOSS_LLM_API_KEY", "")
        if not api_key:
            self._llm_client = False  # sentinel: tried but not available
            return None

        config = LLMConfig(
            api_key=api_key,
            base_url=os.environ.get("BOSS_LLM_BASE_URL", "https://api.openai.com/v1"),
            model=os.environ.get("BOSS_LLM_MODEL", "gpt-4.1-mini"),
        )
        self._llm_client = LLMClient(config)
        return self._llm_client

    def can_handle(self, task: SubTask) -> bool:
        return task.agent == AgentType.CODER

    def execute(self, task: SubTask, context: dict | None = None) -> ExecutionResult:
        # Build prompt with context from previous tasks
        prompt = self._build_prompt(task, context)

        # Strategy 1: LLM API (zero local deps, works everywhere)
        client = self._get_llm_client()
        if client:
            return self._execute_via_llm(task, client, prompt)

        # Strategy 2: Claude Code CLI (if installed locally)
        if self.claude_path:
            return self._execute_via_cli(task, prompt)

        # Strategy 3: Shell fallback (best effort)
        return self._execute_via_shell(task, prompt)

    def _build_prompt(self, task: SubTask, context: dict | None) -> str:
        prompt = (
            "You are a coding assistant. Generate code to complete this task.\n"
            "Output ONLY the code, no explanations unless asked.\n\n"
            f"Task: {task.description}"
        )
        if context:
            prev = []
            for dep_id in task.dependencies:
                if dep_id in context:
                    prev.append(f"[{dep_id}]:\n{context[dep_id]}")
            if prev:
                prompt = (
                    "You are a coding assistant. Previous task results:\n"
                    + "\n".join(prev)
                    + f"\n\nNow complete this task: {task.description}\n"
                    "Output ONLY the code."
                )
        return prompt

    def _execute_via_llm(self, task, client, prompt):
        from .llm_client import LLMMessage
        messages = [
            LLMMessage(role="system", content="You are an expert coding assistant. Output clean, working code."),
            LLMMessage(role="user", content=prompt),
        ]
        response = client.chat(messages, temperature=0.2, max_tokens=4096)
        if response.success:
            return ExecutionResult(
                task_id=task.id,
                success=True,
                output=response.output if hasattr(response, 'output') else response.content,
            )
        return ExecutionResult(
            task_id=task.id,
            success=False,
            output="",
            error=f"LLM API error: {response.error}",
        )

    def _execute_via_cli(self, task, prompt):
        try:
            result = subprocess.run(
                [self.claude_path, "--print", prompt],
                capture_output=True,
                text=True,
                timeout=300,
                encoding="utf-8",
                errors="replace",
            )
            return ExecutionResult(
                task_id=task.id,
                success=result.returncode == 0,
                output=result.stdout[-4000:] if len(result.stdout) > 4000 else result.stdout,
                error=result.stderr[-1000:] if result.stderr else None,
            )
        except subprocess.TimeoutExpired:
            return ExecutionResult(
                task_id=task.id,
                success=False,
                output="",
                error="Claude Code timed out (300s)",
            )
        except Exception as e:
            return ExecutionResult(
                task_id=task.id,
                success=False,
                output="",
                error=str(e),
            )

    def _execute_via_shell(self, task, prompt):
        """Shell fallback: try to run the task description as a command."""
        return ExecutionResult(
            task_id=task.id,
            success=False,
            output="",
            error="No LLM API key or Claude Code available. Set BOSS_LLM_API_KEY to enable coding tasks.",
        )


class ResearchExecutor:
    """Research executor - web search via DuckDuckGo Instant Answer API.

    No API key required. Uses DuckDuckGo's free instant answer endpoint.
    """

    def can_handle(self, task: SubTask) -> bool:
        return task.agent == AgentType.RESEARCHER

    def execute(self, task: SubTask, context: dict | None = None) -> ExecutionResult:
        query = task.description.strip()

        # Try DuckDuckGo Instant Answer API (no key needed)
        try:
            results = self._search_duckduckgo(query)
            if results:
                return ExecutionResult(
                    task_id=task.id,
                    success=True,
                    output=results,
                )
        except Exception:
            pass

        # Fallback: try a simple web fetch
        try:
            results = self._search_via_fetch(query)
            if results:
                return ExecutionResult(
                    task_id=task.id,
                    success=True,
                    output=results,
                )
        except Exception as e:
            return ExecutionResult(
                task_id=task.id,
                success=False,
                output="",
                error=f"Research failed: {e}",
            )

        return ExecutionResult(
            task_id=task.id,
            success=False,
            output="",
            error="No search results found",
        )

    def _search_duckduckgo(self, query: str) -> str:
        """Search via DuckDuckGo Instant Answer API (free, no key)."""
        params = urllib.parse.urlencode({
            "q": query,
            "format": "json",
            "no_html": 1,
            "skip_disambig": 1,
        })
        url = f"https://api.duckduckgo.com/?{params}"

        req = urllib.request.Request(url, headers={"User-Agent": "BossAgent/0.3"})
        with urllib.request.urlopen(req, timeout=15) as resp:
            data = json.loads(resp.read().decode("utf-8"))

        sections = []

        # Abstract
        abstract = data.get("AbstractText", "")
        if abstract:
            source = data.get("AbstractSource", "")
            sections.append(f"Summary: {abstract}")
            if source:
                sections.append(f"Source: {source}")

        # Related topics
        related = data.get("RelatedTopics", [])
        for i, topic in enumerate(related[:5]):
            if isinstance(topic, dict) and "Text" in topic:
                sections.append(f"- {topic['Text']}")
                if topic.get("FirstURL"):
                    sections.append(f"  Link: {topic['FirstURL']}")

        # Infobox
        infobox = data.get("Infobox", {})
        if infobox and "content" in infobox:
            for item in infobox["content"][:5]:
                label = item.get("label", "")
                value = item.get("value", "")
                if label and value:
                    sections.append(f"- {label}: {value}")

        if not sections:
            return ""

        header = f"Research results for: {query}\n{'=' * 40}"
        return f"{header}\n\n" + "\n".join(sections)

    def _search_via_fetch(self, query: str) -> str:
        """Fallback: fetch DuckDuckGo HTML and extract snippets."""
        params = urllib.parse.urlencode({"q": query})
        url = f"https://html.duckduckgo.com/html/?{params}"

        req = urllib.request.Request(url, headers={
            "User-Agent": "Mozilla/5.0 (compatible; BossAgent/0.3)"
        })
        with urllib.request.urlopen(req, timeout=15) as resp:
            html = resp.read().decode("utf-8", errors="replace")

        # Extract result snippets (simple regex)
        import re
        snippets = re.findall(r'class="result__snippet"[^>]*>(.*?)</a>', html, re.DOTALL)
        clean = []
        for s in snippets[:5]:
            text = re.sub(r"<[^>]+>", "", s).strip()
            if text:
                clean.append(f"- {text}")

        if not clean:
            return ""

        return f"Search results for: {query}\n{'=' * 40}\n\n" + "\n".join(clean)


class ReviewExecutor:
    """Review executor - uses CoderExecutor for code review."""

    def __init__(self):
        self._coder = CoderExecutor()

    def can_handle(self, task: SubTask) -> bool:
        return task.agent == AgentType.REVIEWER

    def execute(self, task: SubTask, context: dict | None = None) -> ExecutionResult:
        review_prompt = (
            f"As a senior code reviewer, review the following and provide "
            f"specific, actionable feedback:\n\n{task.description}"
        )
        review_task = SubTask(
            id=task.id,
            description=review_prompt,
            agent=AgentType.CODER,
            dependencies=task.dependencies,
        )
        return self._coder.execute(review_task, context)


class BossEngine:
    """Boss execution engine - the dispatch hub.

    Receives a TaskPlan, executes subtasks by dependency order,
    and collects results for downstream tasks.
    """

    def __init__(self):
        self.executors = [
            ShellExecutor(),
            CoderExecutor(),
            ResearchExecutor(),
            ReviewExecutor(),
        ]
        self.context: dict[str, str] = {}

    def _get_executor(self, task: SubTask):
        """Find the right executor for this task."""
        for executor in self.executors:
            if executor.can_handle(task):
                return executor
        return self.executors[0]  # fallback to shell

    def execute_plan(self, plan) -> list[ExecutionResult]:
        """Execute the entire task plan in dependency order."""
        results: list[ExecutionResult] = []
        completed_ids: set[str] = set()

        for task in plan.subtasks:
            # Check dependencies
            deps_ok = True
            for dep_id in task.dependencies:
                if dep_id not in completed_ids:
                    results.append(ExecutionResult(
                        task_id=task.id,
                        success=False,
                        output="",
                        error=f"Dependency {dep_id} not completed",
                    ))
                    deps_ok = False
                    break

            if not deps_ok:
                continue

            # Execute
            executor = self._get_executor(task)
            result = executor.execute(task, self.context)

            if result.success:
                self.context[task.id] = result.output
                completed_ids.add(task.id)

            results.append(result)

        return results
