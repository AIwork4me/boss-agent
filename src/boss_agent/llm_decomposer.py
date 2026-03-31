"""Boss Agent - LLM-powered Task Decomposer (v0.2)."""

from __future__ import annotations

import json
import logging

from boss_agent.decomposer import (
    AgentType,
    SubTask,
    TaskPlan,
    decompose as rule_decompose,
    _generate_id,
    _reset_counter,
)
from boss_agent.llm_client import LLMClient, LLMMessage

logger = logging.getLogger(__name__)

SYSTEM_PROMPT = (
    "You are a task decomposition engine for Boss Agent.\n"
    "Given a user task, break it into subtasks. Output ONLY valid JSON.\n"
    "JSON schema:\n"
    '{"summary": "one-line summary", "subtasks": [{"description": "what to do", '
    '"agent": "coder|researcher|shell|reviewer", "dependencies": []}]}\n'
    "Agent types: coder=coding/debugging, researcher=search/analyze, "
    "shell=system commands, reviewer=code review.\n"
    "Rules: Each subtask atomic. Use dependencies only when needed. "
    "Default shell if unsure. Dependencies should use 1-based indices "
    "referring to the position in the subtasks array (e.g. [1] means "
    "depends on first subtask)."
)

_AGENT_MAP = {
    "coder": AgentType.CODER,
    "researcher": AgentType.RESEARCHER,
    "shell": AgentType.SHELL,
    "reviewer": AgentType.REVIEWER,
}


def _strip_markdown_fences(text):
    """Remove markdown code fences from LLM output."""
    text = text.strip()
    if not text.startswith("```"):
        return text
    lines = text.split("\n")
    start = 0
    for i, line in enumerate(lines):
        stripped = line.strip()
        if stripped.startswith("{"):
            start = i
            break
    else:
        start = 1
    end = len(lines)
    for i in range(len(lines) - 1, -1, -1):
        if lines[i].strip() == "```":
            end = i
            break
    return "\n".join(lines[start:end])


def _parse_response(text, original_input):
    """Parse LLM JSON response into a TaskPlan.

    Remaps 1-based index dependencies to actual generated IDs.
    Falls back to single shell task on any parse failure.
    """
    text = _strip_markdown_fences(text)

    data = json.loads(text)

    raw_subtasks = data.get("subtasks", [])
    if not isinstance(raw_subtasks, list) or not raw_subtasks:
        raise ValueError("subtasks must be a non-empty list")

    # Phase 1: generate IDs and build index-to-ID mapping
    _reset_counter()
    id_list = []
    for _ in raw_subtasks:
        id_list.append(_generate_id())

    # Phase 2: build SubTasks with remapped dependencies
    subtasks = []
    for idx, item in enumerate(raw_subtasks):
        if not isinstance(item, dict):
            continue
        agent_str = item.get("agent", "shell").lower()
        agent = _AGENT_MAP.get(agent_str, AgentType.SHELL)

        # Remap dependencies: accept 1-based indices or string IDs
        raw_deps = item.get("dependencies", [])
        if not isinstance(raw_deps, list):
            raw_deps = []
        resolved_deps = []
        for dep in raw_deps:
            if isinstance(dep, int) and 1 <= dep <= len(id_list):
                resolved_deps.append(id_list[dep - 1])
            elif isinstance(dep, str) and dep in id_list:
                resolved_deps.append(dep)

        subtasks.append(SubTask(
            id=id_list[idx],
            description=item.get("description", original_input),
            agent=agent,
            dependencies=resolved_deps,
        ))

    if not subtasks:
        _reset_counter()
        subtasks = [SubTask(
            id=_generate_id(),
            description=original_input,
            agent=AgentType.SHELL,
        )]

    return TaskPlan(
        original=original_input,
        subtasks=subtasks,
        summary=data.get("summary", original_input),
    )


def decompose_with_llm(user_input, client):
    """Decompose a task using LLM intelligence.

    Falls back to rule-based decomposition if LLM fails.
    """
    messages = [
        LLMMessage(role="system", content=SYSTEM_PROMPT),
        LLMMessage(role="user", content="Decompose this task: " + user_input),
    ]
    response = client.chat(messages, temperature=0.3, max_tokens=1024)
    if not response.success:
        logger.warning("LLM failed (%s), falling back to rule-based", response.error)
        return rule_decompose(user_input)
    try:
        return _parse_response(response.content, user_input)
    except (json.JSONDecodeError, KeyError, TypeError, ValueError) as exc:
        logger.warning("LLM parse error (%s), falling back to rule-based", exc)
        return rule_decompose(user_input)
