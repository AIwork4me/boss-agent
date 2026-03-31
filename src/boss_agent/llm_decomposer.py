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
    "Default shell if unsure."
)

_AGENT_MAP = {
    "coder": AgentType.CODER,
    "researcher": AgentType.RESEARCHER,
    "shell": AgentType.SHELL,
    "reviewer": AgentType.REVIEWER,
}


def _parse_response(text, original_input):
    text = text.strip()
    if text.startswith("```"):
        lines = text.split("\n")
        for i, line in enumerate(lines):
            if line.strip().startswith("{"):
                text = "\n".join(lines[i:])
                break
    if text.endswith("```"):
        text = text[:-3]
    data = json.loads(text.strip())
    _reset_counter()
    subtasks = []
    for item in data.get("subtasks", []):
        agent_str = item.get("agent", "shell").lower()
        agent = _AGENT_MAP.get(agent_str, AgentType.SHELL)
        deps = item.get("dependencies", [])
        subtasks.append(SubTask(
            id=_generate_id(),
            description=item.get("description", original_input),
            agent=agent,
            dependencies=deps,
        ))
    if not subtasks:
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
    _reset_counter()
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
    except (json.JSONDecodeError, KeyError, TypeError) as exc:
        logger.warning("LLM parse error (%s), falling back to rule-based", exc)
        return rule_decompose(user_input)
