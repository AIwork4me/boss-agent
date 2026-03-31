<div align="center">

# 👑 Boss Agent

### *You speak, Boss dispatches.*

**An AI Agent that orchestrates other AI agents to get things done.**

*Like a CEO — but but AI workers.*

<p align="center">
  <img src="https://img.shields.io/badge/version-0.1.0-blue" alt="v0.1.0" />
  <img src="https://img.shields.io/badge/python-3.10+-green" alt="Python 3.10+" />
  <img src="https://img.shields.io/badge/license-MIT-green" alt="MIT License" />
</p>

<p align="center">
  <em>Empowered by <a href="https://github.com/AIwork4me">Lobster Company</a> 🦞</em>
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

```bash
$ python -m boss_agent "echo step 1, then echo step 2"

  🦞 Boss Agent v0.1.0
  ==================================================

  [Boss] Task received: echo step 1, then echo step 2

  [Boss] Decomposing task...
  [Boss] Plan: 2 subtask(s)
    [T001] [shell       ] echo step 1
    [T002] [shell       ] echo step 2 (after T001)

  [Boss] Executing...
  --------------------------------------------------
  --------------------------------------------------

  [Boss] Results: 2 ok, 0 failed (31ms)

  [T001] OK
    step 1

  [T002] OK
    step 2

  All tasks completed successfully.
```

## Quick Start

```bash
# Clone and run (Python 3.10+)
git clone https://github.com/AIwork4me/boss-agent.git
cd boss-agent

# Single task
python -m boss_agent "echo hello from Boss Agent"

# Compound task (auto-decomposed into serial subtasks)
python -m boss_agent "echo step 1, then echo step 2"
```

*Zero config. No API keys needed for shell mode. For LLM-powered dispatch, install [Claude Code](https://docs.anthropic.com/en/docs/claude-code).*

## How It Works

```
User says one sentence
        ↓
Boss decomposes into subtasks
        ↓
Boss dispatches each subtask to the best agent
  ┌──────────────┬──────────────┬──────────────┐
  │   Coder      │  Researcher  │    Shell       │
  │ Claude Code  │  Web Search  │  Any command  │
  └──────────────┴──────────────┴──────────────┘
        ↓
Boss collects results and delivers
```

> **Inspired by Liu Bang** (刘邦), — Founder of the Han Dynasty: *"I don't fight battles. I find the best people to fight battles for me."* He let generals fight, strategists plan, and ministers govern — each doing what they do best.

## Architecture

```
boss_agent/
├── __main__.py          # CLI entry point
├── decomposer.py        # Task decomposition (Boss's brain)
└── executor.py          # Agent dispatch (Boss's lieutenants)
    ├── ShellExecutor      # Any shell command
    ├── ClaudeCodeExecutor # Coding tasks → Claude Code
    ├── ResearchExecutor   # Web research (v0.2)
    └── ReviewExecutor     # Code review (v0.2)
```

| Component | Role | Analogy |
|-----------|------|---------|
| `decomposer.py` | Understand & split tasks | Boss's brain |
| `ClaudeCodeExecutor` | Execute coding tasks | Han Xin (韩信) — the general |
| `ResearchExecutor` | Gather information | Zhang Liang (张良) — the strategist |
| `ShellExecutor` | Run system commands | Xiao He (萧何) — the administrator |

## Current Status

| Executor | Status | Description |
|----------|--------|-------------|
| ShellExecutor | ✅ Working | Any shell command |
| ClaudeCodeExecutor | 🔜 v0.2 | Calls `claude --print` for coding tasks |
| ResearchExecutor | 🔜 v0.2 | Web search integration |
| ReviewExecutor | 🔜 v0.2 | Code review via Claude Code |

## Roadmap

- [x] **v0.1** — Rule-based decomposition + Shell execution
- [ ] **v0.2** — LLM-powered decomposition + Claude Code integration
- [ ] **v0.3** — Web search integration + Feishu/Slack bot
- [ ] **v0.4** — Parallel execution + Memory system

## Philosophy

Built by [Lobster Company](https://github.com/AIwork4me/lobster-company), guided by:

- **Seek Truth from Facts** — Verify with real users, not assumptions
- **Mass Line** — Build what users actually need
- **Independence** — Core orchestration logic must be self-owned

## Contributing

PRs welcome! Feel free to open an issue or submit a pull request.

## License

[MIT](LICENSE)
