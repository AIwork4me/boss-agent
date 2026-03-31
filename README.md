<div align="center">

# 👑 Boss Agent

### *You speak, Boss dispatches.*

**An AI Agent that orchestrates other AI agents to get things done.**

*Like a CEO — but the AI workers.*

<p align="center">
  <img src="https://img.shields.io/badge/version-0.1.0-blue" alt="v0.1.0" />
  <img src="https://img.shields.io/badge/python-3.10+-green" alt="Python 3.10+" />
  <img src="https://img.shields.io/badge/license-MIT-green" alt="MIT License" />
  <img src="https://img.shields.io/badge/stars-0-brightgreen" alt="Stars" />
</p>

<p align="center">
  <em>YouEmpowered by <a href="https://github.com/AIwork4me">Lobster Company</a> 🦞</em>
</p>

---

## The Problem

You already have Claude Code, Cursor, ChatGPT, Copilot, Windsurf, Perplexity...

You result? **Cognitive overload.** Task switching between AI agents exhausts your prefrontal cortex. You more tools = more fatigue.

 You don't need another tool. **You need a Boss.**

## The Solution
**One agent to rule them all.**

You tell Boss Agent what you want done. It decomposes your request into subtasks, dispatches each to the best AI agent for the job, collects the results, and reports back.

 It's the a CEO managing a team — except this CEO never sleeps.

```
$ boss "Research GitHub trending patterns and write a report"

  🦞 Boss Agent v0.1.0
  ==================================================
  
  [Boss] Task received: Research GitHub trending patterns and write a report
  
  [Boss] Decomposing task...
  [Boss] Plan: 2 subtask(s)
    [T001] [researcher  ] Research GitHub trending patterns
    [T002] [coder      ] Write a report (after T001)
  
  [Boss] Executing...
  --------------------------------------------------
  --------------------------------------------------
  
  [Boss] Results: 2 ok, 0 failed (12ms)
  
  [T001] OK
    [report.md saved to ./output]
  [T002] OK
    Report complete.
  
  All tasks completed successfully.
```

*Like a CEO, Boss Agent doesn't do the work — it dispatches the right agent for the job.*

## Quick Start

```bash
# Clone and run
git clone https://github.com/AIwork4me/boss-agent.git
cd boss-agent

# Run with Python (3.10+)
python -m boss_agent "echo hello from Boss Agent"

# Run a compound task
python -m boss_agent "echo step 1, then echo step 2"
```

*Zero config. No API keys needed for the basic mode. For LLM-powered dispatch, install [Claude Code](https://docs.anthropic.com/en/docs/claude-code).*

```

## How It Works

```
User says one sentence
       ↓
Boss decomposes into subtasks
       ↓
Boss dispatches each subtask to the best agent
  ┌──────────────┬──────────────┬──────────────┐
  │  Coder      │  Researcher  │  Shell        │
  │  Claude Code│  Web Search│  Any command │
  └──────────────┴──────────────┴──────────────┘
       ↓
Boss collects results and delivers
```
> **Inspired by Liu Bang** (刘邦): "I don't fight battles. I fight people to fight battles for me." — The founder of the Han Dynasty, managed his empire by letting generals, strategists, and ministers each do what they do best.

## Architecture
```
boss_agent/
├── __main__.py    # CLI entry point
├── decomposer.py  # Task decomposition (Boss's brain)
├── executor.py    # Agent dispatch (Boss's lieutenants)
    ├── ShellExecutor      # Any shell command
    ├── ClaudeCodeExecutor # Coding tasks (the "Han Xin")
    ├── ResearchExecutor   # Web research (v0.2: real API)
    └── ReviewExecutor     # Code review
```

## Roadmap
- [x] v0.1 — Rule-based decomposition + Shell execution
- [ ] v0.2 — LLM-powered decomposition + Claude Code integration
- [ ] v0.3 — Web search integration + Feishu/Slack bot
- [ ] v0.4 — Parallel execution + Memory system

## Philosophy
Boss Agent is built by [Lobster Company](https://github.com/AIwork4me/lobster-company), guided by the management philosophy of Mao Zedong + Sima Guang (Zizhi Tongjian).

- **Seek Truth from Facts** — Verify with real users, not assumptions
- **Mass Line** — Build what users actually need
- **Independence** — Core orchestration logic must be self-owned

## Contributing
PRs welcome! See [CONTRIBUTING.md](CONTRIBUTING.md).

## License
MIT
