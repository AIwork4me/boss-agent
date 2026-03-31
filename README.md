<div align="center">

# 👑 Boss Agent

### *You speak, Boss dispatches.*

**An AI Agent that orchestrates other AI agents to get things done.**

*Like a CEO — but for AI workers.*

<p align="center">
  <img src="https://img.shields.io/badge/version-0.2.0-blue" alt="v0.2.0" />
  <img src="https://img.shields.io/badge/python-3.10+-green" alt="Python 3.10+" />
  <img src="https://img.shields.io/badge/license-MIT-green" alt="MIT License" />
</p>

<p align="center">
  <em>Built by <a href="https://github.com/AIwork4me">Lobster Company</a> 🦞</em>
</p>

[中文版](README_zh-CN.md)

---

## The Problem

You already have Claude Code, Cursor, ChatGPT, Copilot, Windsurf, Perplexity...

The result? **Cognitive overload.** Task switching between AI agents exhausts your prefrontal cortex. More tools = more fatigue.

You don't need another tool. **You need a Boss.**

## The Solution

**One agent to rule them all.**

You tell Boss Agent what you want done. It decomposes your request into subtasks, dispatches each to the best AI agent for the job, collects the results, and reports back.

It's like a CEO managing a team — except this CEO never sleeps.

## Demo

```bash
$ python -m boss_agent "echo hello from Boss Agent"

==================================================
  Boss Agent v0.2.0
==================================================

  [Boss] Task received: echo hello from Boss Agent

  [Boss] Decomposing (rule-based mode)...
  [Boss] Plan: 1 subtask(s)
    [T001] [shell       ] echo hello from Boss Agent

  [Boss] Executing...
  --------------------------------------------------
  --------------------------------------------------

  [Boss] Results: 1 ok, 0 failed (24ms)

  [T001] OK
    hello from Boss Agent

  All tasks completed successfully.
```

## Quick Start

```bash
# Clone the repo (requires Python 3.10+)
git clone https://github.com/AIwork4me/boss-agent.git
cd boss-agent

# Install dependencies (pick one)
pip install -e .          # standard pip
uv pip install -e .       # or uv (faster)

# Run your first task
python -m boss_agent "echo hello from Boss Agent"

# Compound task (auto-decomposed into serial subtasks)
python -m boss_agent "echo step 1, then echo step 2"
```

No API keys needed for shell mode. For LLM-powered decomposition, see below.

## LLM Mode (v0.2.0)

Boss Agent v0.2.0 supports **LLM-powered task decomposition**. Instead of rule-based splitting, it uses an LLM to intelligently understand and break down your request.

```bash
# Set environment variables for LLM mode
export BOSS_LLM_API_KEY="your-api-key"
export BOSS_LLM_BASE_URL="https://api.openai.com/v1"  # or any OpenAI-compatible API
export BOSS_LLM_MODEL="gpt-4o-mini"

# Run with LLM-powered decomposition
python -m boss_agent "Research AI agent frameworks and write a comparison report"
```

Boss Agent automatically uses LLM mode when `BOSS_LLM_API_KEY` is set. Otherwise it falls back to rule-based mode.

## How It Works

```
User says one sentence
        |
        v
Boss decomposes into subtasks
(LLM-powered or rule-based)
        |
        v
Boss dispatches each subtask to the best agent
  +--------------+--------------+
  |   Shell      |  (more soon) |
  | Any command  |  Coder, etc. |
  +--------------+--------------+
        |
        v
Boss collects results and delivers
```

> **Inspired by Liu Bang** (刘邦), founder of the Han Dynasty, who famously said he could not fight battles, plan strategy, or govern as well as his top generals, strategists, and ministers — but he could find the best person for each job and let them do it.

## Architecture

```
boss_agent/
  __main__.py          # CLI entry point
  decomposer.py        # Rule-based task decomposition
  llm_decomposer.py    # LLM-powered decomposition (v0.2)
  llm_client.py        # OpenAI-compatible API client (v0.2)
  executor.py          # Agent dispatch
    ShellExecutor        # Any shell command [working]
    ClaudeCodeExecutor   # Coding via Claude Code [v0.3]
    ResearchExecutor     # Web research [v0.3]
    ReviewExecutor       # Code review [v0.3]
```

## Current Status

| Component | Status | Description |
|-----------|--------|-------------|
| ShellExecutor | ✅ Working | Any shell command |
| LLM Decomposer | ✅ Working | OpenAI-compatible, auto-fallback |
| ClaudeCodeExecutor | 🔜 v0.3 | Coding tasks via Claude Code |
| ResearchExecutor | 🔜 v0.3 | Web search integration |
| ReviewExecutor | 🔜 v0.3 | Code review |

## Roadmap

- [x] **v0.1** — Rule-based decomposition + Shell execution
- [x] **v0.2** — LLM-powered decomposition + graceful fallback
- [ ] **v0.3** — Claude Code integration + Web search
- [ ] **v0.4** — Parallel execution + Memory system

## Philosophy

Built by [Lobster Company](https://github.com/AIwork4me/lobster-company), guided by:

- **Seek Truth from Facts** — Verify with real users, not assumptions
- **Mass Line** — Build what users actually need
- **Independence** — Core orchestration logic must be self-owned

## Contributing

PRs welcome! Please:
- Run tests before submitting: `pytest tests/ -v`
- Keep PRs focused and small
- Open an issue to discuss major changes first

## License

[MIT](LICENSE)
