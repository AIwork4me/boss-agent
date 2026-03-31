"""
Boss Agent - 任务拆解器

核心职责：接收用户的一句话，拆解成可执行的子任务列表。
这是 Boss 的唯一核心能力——刘邦不需要自己打仗，但他要知道派谁去打什么仗。
"""

from __future__ import annotations

import re
from dataclasses import dataclass, field
from enum import Enum
from typing import Optional


class AgentType(Enum):
    """子代理类型——每个领域用最强的人"""
    CODER = "coder"           # 编码：Claude Code
    RESEARCHER = "researcher" # 调研：Web Search / Perplexity
    SHELL = "shell"           # 系统命令：Shell
    REVIEWER = "reviewer"     # 审查：Code Review Agent


@dataclass
class SubTask:
    """子任务"""
    id: str
    description: str
    agent: AgentType
    dependencies: list[str] = field(default_factory=list)
    status: str = "pending"   # pending / running / done / failed
    result: Optional[str] = None


@dataclass
class TaskPlan:
    """任务计划"""
    original: str
    subtasks: list[SubTask]
    summary: str


# 任务计数器
_task_counter = 0


def _reset_counter() -> None:
    global _task_counter
    _task_counter = 0


def _generate_id() -> str:
    global _task_counter
    _task_counter += 1
    return f"T{_task_counter:03d}"


def _classify_agent(task_description: str) -> AgentType:
    """分析任务类型，决定派给哪个 Agent——刘邦用人之道"""
    lower = task_description.lower()
    
    # 编码类
    code_patterns = r"写|实现|开发|创建|修复|重构|代码|函数|模块|测试|部署|implement|code|build|fix|refactor|deploy|write|create"
    if re.search(code_patterns, lower):
        return AgentType.CODER
    
    # 调研类
    research_patterns = r"调研|搜索|查找|分析|研究|了解|搜索|search|research|find|investigate|analyze|study"
    if re.search(research_patterns, lower):
        return AgentType.RESEARCHER
    
    # 审查类
    review_patterns = r"审查|检查|review|验证|verify|检查|audit"
    if re.search(review_patterns, lower):
        return AgentType.REVIEWER
    
    # 默认 shell
    return AgentType.SHELL


def decompose(user_input: str) -> TaskPlan:
    """
    核心函数：拆解用户指令为子任务列表
    
    当前版本使用规则引擎拆解（v0.1）
    后续版本接入 LLM 做智能拆解（v0.2）
    """
    _reset_counter()
    input_text = user_input.strip()
    
    # 判断是否是复合任务
    compound_pattern = r"并且|然后|之后|接着|同时|还有|以及|[,;，；]"
    is_compound = bool(re.search(compound_pattern, input_text))
    
    if not is_compound:
        # 单一任务，不拆解
        agent = _classify_agent(input_text)
        subtask = SubTask(
            id=_generate_id(),
            description=input_text,
            agent=agent,
            dependencies=[],
            status="pending",
        )
        return TaskPlan(
            original=input_text,
            subtasks=[subtask],
            summary=f"单一任务，派给 {agent.value} 执行。",
        )
    
    # 复合任务：按分隔符拆分
    parts = [p.strip() for p in re.split(compound_pattern, input_text) if p.strip()]
    
    subtasks: list[SubTask] = []
    prev_id: Optional[str] = None
    
    for part in parts:
        agent = _classify_agent(part)
        task_id = _generate_id()
        deps = [prev_id] if prev_id else []
        subtasks.append(SubTask(
            id=task_id,
            description=part,
            agent=agent,
            dependencies=deps,
            status="pending",
        ))
        prev_id = task_id
    
    lines = [f"  {st.id}: [{st.agent.value}] {st.description}" for st in subtasks]
    summary = f"拆解为 {len(subtasks)} 个子任务：\n" + "\n".join(lines)
    
    return TaskPlan(
        original=input_text,
        subtasks=subtasks,
        summary=summary,
    )
