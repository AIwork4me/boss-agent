<div align="center">

# 👑 Boss Agent
### *你说一句话，Boss 来搞定。*

**一个指挥其他 AI 智能体完成任务的 AI CEO Agent。**

<p align="center">
  <img src="https://img.shields.io/badge/version-0.1.0-blue" alt="v0.1.0" />
  <img src="https://img.shields.io/badge/python-3.10+-green" alt="Python 3.10+" />
  <img src="https://img.shields.io/badge/license-MIT-green" alt="MIT License" />
  <img src="https://img.shields.io/badge/powered%20by-Lobster%20Company-FFD700" alt="Lobster Company" />
</p>

<p align="center">
  🦞 由 <a href="https://github.com/AIwork4me/lobster-company">龙虾公司</a> 出品
</p>

[English](README.md)

---

## 问题

你已经有 Claude Code、Cursor、 ChatGPT、 Copilot, Windsurf、 Perplexity……

结果呢？**认知过载。** 在多个 AI 工具之间频繁切换，会让你的前额叶皮层持续疲劳，降低专注力和决策能力。

The ([研究](https://www.nature.com/articles/nn.2820))

你 不需要更多工具。**你需要一个 Boss.**

## 解决方案
**你说一句话，Boss 搞定一切。**

Boss Agent 把你的需求拆解为子任务，分派给最合适的 AI 智能体执行，收集结果后汇报给你。

```
用户指令
       ↓
Boss 拆解为子任务
       ↓
Boss 分派每个子任务给最合适的 Agent
  ┌──────────────┬──────────────┬──────────────┐
  │  Coder       │  Researcher  │  Shell        │
  │  Claude Code │  Web Search │  Any command │
  └──────────────┴──────────────┴──────────────┘
       ↓
Boss 收集结果并交付
```

> **Inspired by Liu Bang** (刘邦), founder of the Han Dynasty: *"I don't fight battles. I find the best people to fight battles for me." — The founder of the Han Dynasty, managed his empire by letting generals, strategists, and ministers each do what they do best.

## Quick Start
```bash
git clone https://github.com/AIwork4me/boss-agent.git
cd boss-agent

# Run with Python (3.10+)
python -m boss_agent "echo hello from Boss Agent"

# Run a compound task
python -m boss_agent "echo step 1, then echo step 2"
```

*Zero config. No API keys needed for basic mode. For LLM-powered dispatch, install [Claude Code](https://docs.anthropic.com/en/docs/claude-code).*

## How It Works
```
User says one sentence
       ↓
Boss decomposes into subtasks
       ↓
Boss dispatches each subtask to the best agent
  ┌──────────────┬──────────────┬──────────────┐
  │  Coder       │  Researcher  │  Shell        │
  │  Claude Code │  Web Search │  Any command │
  └──────────────┴──────────────┴──────────────┘
       ↓
Boss collects results and delivers
```
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
| `ShellExecutor` | Run system commands | Xiao He (萧何) - the administrator |
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
PRs welcome! See [CONTRIBUTING.md](docs/CONTRIBUTING.md).
## License
[MIT](LICENSE)
