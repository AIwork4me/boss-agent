"""
Boss Agent - 执行引擎

核心职责：接收拆解好的子任务，分派给对应的最强智能体执行。
刘邦用人之道：每个领域派最强的人去干。
"""

from __future__ import annotations

import subprocess
import shutil
import os
import sys
from dataclasses import dataclass
from typing import Optional

from .decomposer import SubTask, AgentType


@dataclass
class ExecutionResult:
    """执行结果"""
    task_id: str
    success: bool
    output: str
    error: Optional[str] = None
    duration_ms: int = 0


class ShellExecutor:
    """Shell 命令执行器——最基础的执行能力"""
    
    def can_handle(self, task: SubTask) -> bool:
        return task.agent == AgentType.SHELL
    
    def execute(self, task: SubTask, context: dict | None = None) -> ExecutionResult:
        """执行 shell 命令"""
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
    """
    Claude Code 执行器——Boss 手下的韩信
    
    编码领域的最强智能体。Boss 只需要说"干什么"，
    Claude Code 自己知道"怎么干"。
    """
    
    def __init__(self):
        self.claude_path = shutil.which("claude")
    
    def is_available(self) -> bool:
        """检查 Claude Code 是否已安装"""
        return self.claude_path is not None
    
    def can_handle(self, task: SubTask) -> bool:
        return task.agent == AgentType.CODER
    
    def execute(self, task: SubTask, context: dict | None = None) -> ExecutionResult:
        """调用 Claude Code 执行编码任务"""
        if not self.is_available():
            return ExecutionResult(
                task_id=task.id,
                success=False,
                output="",
                error="Claude Code not installed. Install: https://docs.anthropic.com/en/docs/claude-code",
            )
        
        # 构建上下文提示
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
                timeout=300,  # 编码任务给 5 分钟
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
    """
    调研执行器——用 web search 做调研
    
    v0.1: 简单实现，输出提示信息
    v0.2: 接入真实 web search API
    """
    
    def can_handle(self, task: SubTask) -> bool:
        return task.agent == AgentType.RESEARCHER
    
    def execute(self, task: SubTask, context: dict | None = None) -> ExecutionResult:
        # v0.1: 占位实现
        return ExecutionResult(
            task_id=task.id,
            success=True,
            output=f"[Research placeholder] Task: {task.description}\n(Real web search coming in v0.2)",
        )


class ReviewExecutor:
    """
    审查执行器——让 Claude Code 做 code review
    """
    
    def __init__(self):
        self._claude = ClaudeCodeExecutor()
    
    def can_handle(self, task: SubTask) -> bool:
        return task.agent == AgentType.REVIEWER
    
    def execute(self, task: SubTask, context: dict | None = None) -> ExecutionResult:
        if self._claude.is_available():
            # 有 Claude Code，让它做 review
            review_prompt = f"As a code reviewer, please review the following and provide feedback:\n\n{task.description}"
            review_task = SubTask(
                id=task.id,
                description=review_prompt,
                agent=AgentType.CODER,
                dependencies=task.dependencies,
            )
            return self._claude.execute(review_task, context)
        
        # 没有 Claude Code，占位
        return ExecutionResult(
            task_id=task.id,
            success=True,
            output=f"[Review placeholder] Task: {task.description}",
        )


class BossEngine:
    """
    Boss 执行引擎——刘邦的调度中枢
    
    接收 TaskPlan，按依赖顺序执行子任务，收集结果。
    """
    
    def __init__(self):
        self.executors = [
            ShellExecutor(),
            ClaudeCodeExecutor(),
            ResearchExecutor(),
            ReviewExecutor(),
        ]
        self.context: dict[str, str] = {}  # task_id -> result
    
    def _get_executor(self, task: SubTask):
        """找到能处理这个任务的执行器"""
        for executor in self.executors:
            if executor.can_handle(task):
                return executor
        return self.executors[0]  # fallback to shell
    
    def execute_plan(self, plan) -> list[ExecutionResult]:
        """
        执行整个任务计划
        
        按依赖顺序串行执行，把每个子任务的结果传给后续任务。
        """
        results: list[ExecutionResult] = []
        completed_ids: set[str] = set()
        
        for task in plan.subtasks:
            # 检查依赖是否完成
            for dep_id in task.dependencies:
                if dep_id not in completed_ids:
                    results.append(ExecutionResult(
                        task_id=task.id,
                        success=False,
                        output="",
                        error=f"Dependency {dep_id} not completed",
                    ))
                    break
            else:
                # 依赖都完成了，执行
                executor = self._get_executor(task)
                task.status = "running"
                result = executor.execute(task, self.context)
                task.status = "done" if result.success else "failed"
                
                # 记录结果到上下文
                if result.success:
                    self.context[task.id] = result.output
                    completed_ids.add(task.id)
                
                results.append(result)
        
        return results
