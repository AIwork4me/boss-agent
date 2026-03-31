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

你已经有 Claude Code、Cursor、ChatGPT、Copilot、Windsurf、Perplexity……

结果呢？**认知过载。** 在多个 AI 工具之间频繁切换，会让你的前额叶皮层持续疲劳，降低专注力和决策能力。

> ([研究来源](https://www.nature.com/articles/nn.2820))

你不需要更多工具。**你需要一个 Boss。**

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
  │  Coder       │  Researcher  │  Shell       │
  │  Claude Code │  Web Search │  Any command │
  └──────────────┴──────────────┴──────────────┘
  ↓
Boss 收集结果并交付
```

> **灵感来自刘邦**："我不擅长打仗，但我擅长找到最合适的人来打仗。" —— 汉朝开国皇帝，让将军、谋士、丞相各司其职。

## 快速开始

```bash
# 克隆并运行
git clone https://github.com/AIwork4me/boss-agent.git
cd boss-agent

# 用 Python 运行（3.10+）
python -m boss_agent "echo hello from Boss Agent"

# 运行复合任务
python -m boss_agent "echo step 1, 然后 echo step 2"
```

*零配置。基础模式不需要 API Key。如需 LLM 驱动的任务分派，请安装 [Claude Code](https://docs.anthropic.com/en/docs/claude-code)。*

## 刘邦模式

Boss Agent 遵循刘邦的管理哲学：

> "我不擅长打仗，但我擅长找到最合适的人来打仗。" —— 刘邦

| 领域 | 最强 Agent | 为什么 |
|------|-----------|------|
| 编码 | Claude Code | 最强的 AI 编码工具 |
| 调研 | Perplexity/Web Search | 最强的 AI 搜索工具 |
| 代码审查 | Claude Code | 最强的 AI 审查工具 |
| 系统运维 | Shell | 最可靠的执行方式 |
| 设计 | Midjourney/DALL-E | 即将支持 |
| 测试 | Leike Agent | 即将支持 |

## 架构

```
boss_agent/
├── __main__.py          # CLI 入口
├── decomposer.py        # 任务拆解（Boss 的大脑）
└── executor.py          # Agent 分派（Boss 的武将）
    ├── ShellExecutor      # 任何 Shell 命令
    ├── ClaudeCodeExecutor # 编码任务 → Claude Code
    ├── ResearchExecutor   # Web 调研（v0.2）
    └── ReviewExecutor     # 代码审查（v0.2）
```

| 组件 | 角色 | 类比 |
|------|------|------|
| `decomposer.py` | 理解并拆解任务 | Boss 的大脑 |
| `ClaudeCodeExecutor` | 执行编码任务 | 韩信 —— 大将军 |
| `ResearchExecutor` | 收集信息 | 张良 —— 谋士 |
| `ShellExecutor` | 运行系统命令 | 萧何 —— 丞相 |

## 路线图

- [x] **v0.1** — 规则引擎拆解 + Shell 执行
- [ ] **v0.2** — LLM 驱动拆解 + Claude Code 集成
- [ ] **v0.3** — Web 搜索集成 + 飞书/Slack 机器人
- [ ] **v0.4** — 并行执行 + 记忆系统

## 哲学

由 [龙虾公司](https://github.com/AIwork4me/lobster-company) 出品，遵循：

- **实事求是** — 用真实用户验证，不靠假设
- **群众路线** — 做用户真正需要的东西
- **独立自主** — 核心编排逻辑必须自主掌控

## 贡献
欢迎 PR！详见 [CONTRIBUTING.md](docs/CONTRIBUTING.md)。

## 许可证
[MIT](LICENSE)
