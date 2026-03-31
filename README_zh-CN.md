<div align="center">

# 👔 Boss Agent

### *你说 it, Boss gets it done.*
### *你说 it, Boss 来干。 —— 一句 AI CEO Agent that orchestrates other AI agents to complete tasks.*

*受龙虾公司 (Lobster Company) 启发， by the management philosophy of 毛泽东 + Sima Guang (Zizhi Tongjian).*

*用实践验证真理，by用户验证。*

*

<p align="center">
  <img src="https://img.shields.io/badge/version-0.1.0-blue" alt="v0.1.0" />
  <img src="https://img.shields.io/badge/python-3.10+-green" alt="Python 3.10+" />
  <img src="https://img.shields.io/badge/license-MIT-green" alt="MIT License" />
  <img src="https://img.shields.io/badge/powered%20by-lobster%20Company-FFD700" alt="Lobster Company" />
</p>

<p align="center">
  🦞 Empowered by <a href="https://github.com/AIwork4me/lobster-company">Lobster Company</a>
</p>

---

## 问题

Already have Claude Code, Cursor, ChatGPT, Copilot, Windsurf, Perplexity... 

Result? **Cognitive overload.** Task switching between AI tools makes your prefrontal cortex fatigued, reducing your ability to focus and make decisions.

 ([Research](https://www.nature.com/articles/nn.2820))

)

**You don't need more tools. You need a Boss.**

## Solution
**You speak, Boss dispatches.** Boss decomposes your task into subtasks, dispatches each to the best AI agent, and collects the results.

```
user_input
  ↓
Boss (decompose + prioritize)
  ├── Subtask 1 → Best Agent (e.g., Claude Code for coding)
  ├── Subtask 2 → Web Search for research
  └── SubTask 3 → Code Review for review
  ↓
Boss (aggregate results)
  ↓
Final output
```

| Step | Output |
|:-------|:-------|
|:-----|:-----|:---------|:-------|
| 1 | Decompose | `boss "写一份分析报告并提交PR"` | Shell | 18ms | ✅ All passed |
| 2 | Execute | `boss "调研GitHub Trending规律并写报告"` | Research | ~1s | ✅ Done |
| 3 | Execute | `boss "设计PR审查流程"` | Claude Code | ~30s | ✅ Done |

| 4 | Report | `boss "部署到生产环境"` | Shell | 3s | ✅ Done |

## Quick Start

```bash
# Install
pip install boss-agent

# Or
uv tool install boss-agent

# Run
boss "write a Python web scraper that submits each page to Markdown"
boss "analyze GitHub Trending patterns and write a report, then submit a PR"
boss "implement a PR review pipeline and deploy to production"
```
## Architecture
```
                    ┌──────────────────────┐
                    │     Boss Agent          │
                    │  (Task Decomposer)      │
                    └──────────┬───────────┘
                               │
        ┌──────────┐      ┌──────────┐
        │            │      │            │
  ┌─────┴─────┘  ┌─────┴─────┘
  │ Claude Code │    │ Web Search │
  │  (Coder)    │    │(Researcher) │
  └─────┴─────┘  └─────┴─────┘
        │            │
  ┌─────┴─────┘
  │ Shell      │
  │(Executor)  │
  └─────┴─────┘
```

## The刘邦 Mode
Boss follows the management philosophy of Liu Bang, founder of the Han Dynasty:

> "I am not good at fighting, But I excel at finding the best people for each task." — Liu Bang

| Domain | Best Agent | Why |
|--------|-----------|-----|
| Coding | Claude Code | The best AI coder |
| Research | Perplexity/Web Search | The best AI researcher |
| Code Review | Claude Code | The best AI reviewer |
| System Ops | Shell | The most reliable |
| Design | Midjourney/DALL-E | Coming soon |
| Testing | Leike Agent | Coming soon |

## Contributing
PRs welcome! See [CONTRIBUTING.md](CONTRIBUTING.md).

## License
MIT
