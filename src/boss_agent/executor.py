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


class ClaudeCodeExecutor:
    """Claude Code executor - the coding specialist.

    Uses `claude --print` for coding tasks.
    """

    def __init__(self):
        self.claude_path = shutil.which("claude")

    def is_available(self) -> bool:
        return self.claude_path is not None

    def can_handle(self, task: SubTask) -> bool:
        return task.agent == AgentType.CODER

    def execute(self, task: SubTask, context: dict | None = None) -> ExecutionResult:
        if not self.is_available():
            return ExecutionResult(
                task_id=task.id,
                success=False,
                output="",
                error="Claude Code not installed. Install: https://docs.anthropic.com/en/docs/claude-code",
            )

        prompt = task.description
        if context:
            prev_results = []
            for dep_id in task.dependencies:
                if dep_id in context:
                    prev_results.append(f"[{dep_id} result]:\n{context[dep_id]}")
            if prev_results:
                prompt = f"Previous task results:\n{''.join(prev_results)}\n\nNow do: {task.description}"

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
    """Review executor - uses Claude Code for code review, falls back to shell."""

    def __init__(self):
        self._claude = ClaudeCodeExecutor()

    def can_handle(self, task: SubTask) -> bool:
        return task.agent == AgentType.REVIEWER

    def execute(self, task: SubTask, context: dict | None = None) -> ExecutionResult:
        if self._claude.is_available():
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
            return self._claude.execute(review_task, context)

        # Fallback: use shell with a basic check
        return ExecutionResult(
            task_id=task.id,
            success=True,
            output=f"[Review] Claude Code not available. Task: {task.description}",
        )


class BossEngine:
    """Boss execution engine - the dispatch hub.

    Receives a TaskPlan, executes subtasks by dependency order,
    and collects results for downstream tasks.
    """

    def __init__(self):
        self.executors = [
            ShellExecutor(),
            ClaudeCodeExecutor(),
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
