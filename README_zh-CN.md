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

> 参考：[任务切换的认知成本](https://www.nature.com/articles/nn.2820)

你不需要更多工具。**你需要一个 Boss。**

## 解决方案

**你说一句话，Boss 搞定一切。**

Boss Agent 把你的需求拆解为子任务，分派给最合适的 AI 智能体执行，收集结果后汇报给你。

就像一个 CEO 猟团队——只不过这个 CEO 永远不休息。

```bash
$ python -m boss_agent "echo step 1, 然后 echo step 2"

  🦞 Boss Agent v0.1.0
  ==================================================

  [Boss] 收到任务: echo step 1, 然后 echo step 2

  [Boss] 拆解任务...
  [Boss] 计划: 2 个子任务
    [T001] [shell       ] echo step 1
    [T002] [shell       ] echo step 2 (依赖 T001)

  [Boss] 执行中...
  --------------------------------------------------
  --------------------------------------------------

  [Boss] 结果: 2 成功, 0 失败 (31ms)

  [T001] 成功
    step 1

  [T002] 失败
    step 2

  全部任务完成。
```

## 快速开始

```bash
# 克隆并运行（Python 3.10+）
git clone https://github.com/AIwork4me/boss-agent.git
cd boss-agent

# 单一任务
python -m boss_agent "echo hello from Boss Agent"

# 复合任务（自动拆解为串行子任务）
python -m boss_agent "echo step 1, 然后 echo step 2"
```

*零配置。基础模式不需要 API Key。如需 LLM 驱动的任务分派，请安装 [Claude Code](https://docs.anthropic.com/en/docs/claude-code)。*

## 工作原理

```
用户说一句话
        ↓
Boss 拆解为子任务
        ↓
Boss 分派每个子任务给最合适的智能体
  ┌──────────────┬──────────────┬──────────────┐
  │  编码器       │  调研员       │  Shell        │
  │  Claude Code │  Web Search │  任意命令 │
  └──────────────┴──────────────┴──────────────┘
        ↓
Boss 收集结果并交付
```

> **灵感来自刘邦**——汉朝开国皇帝：*"我不擅长打仗，但我擅长找到最合适的人来打仗。"* 将军打仗、谋士出策、丞相治国——各司其职。

## 架构

```
boss_agent/
├── __main__.py          # CLI 入口
├── decomposer.py        # 任务拆解（Boss 的大脑）
└── executor.py          # 智能体分派（Boss 的武将）
    ├── ShellExecutor      # 任意 Shell 命令
    ├── ClaudeCodeExecutor # 编码任务 → Claude Code
    ├── ResearchExecutor   # Web 调研（v0.2）
    └── ReviewExecutor     # 代码审查（v0.2）
```

| 组件 | 角色 | 类比 |
|------|------|------|
| `decomposer.py` | 理解并拆解任务 | Boss 的大脑 |
| `ClaudeCodeExecutor` | 执行编码任务 | 韩信——大将军 |
| `ResearchExecutor` | 收集信息 | 张良——谋士 |
| `ShellExecutor` | 运行系统命令 | 萧何——丞相 |

## 当前状态

| 执行器 | 状态 | 说明 |
|--------|------|------|
| ShellExecutor | ✅ 可用 | 任意 Shell 命令 |
| ClaudeCodeExecutor | 🔜 v0.2 | 调用 `claude --print` 执行编码任务 |
| ResearchExecutor | 🔜 v0.2 | Web 搜索集成 |
| ReviewExecutor | 🔜 v0.2 | 通过 Claude Code 做代码审查 |

## 路线图

- [x] **v0.1** — 规则引擎拆解 + Shell 执行
- [ ] **v0.2** — LLM 驱动拆解 + Claude Code 集成
- [ ] **v0.3** — Web 搜索集成 + 飞书/Slack 机器人
- [ ] **v0.4** — 并行执行 + 记忆系统

## 理念

由 [龙虾公司](https://github.com/AIwork4me/lobster-company) 出品，遵循：

- **实事求是** — 用真实用户验证，不靠假设
- **群众路线** — 做用户真正需要的东西
- **独立自主** — 核心编排逻辑必须自主掌控

## 贡献

欢迎 PR！随时可以提 Issue 或提交 Pull Request。

## 许可证

[MIT](LICENSE)
