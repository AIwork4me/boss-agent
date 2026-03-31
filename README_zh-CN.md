<div align="center">

# 👑 Boss Agent

### *你说一句话，Boss 来搞定。*

**一个指挥其他 AI 智能体完成任务的 AI CEO Agent。**

<p align="center">
  <img src="https://img.shields.io/badge/version-0.2.0-blue" alt="v0.2.0" />
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

你不需要更多工具。**你需要一个 Boss。**

## 解决方案

**你说一句话，Boss 搞定一切。**

Boss Agent 把你的需求拆解为子任务，分派给最合适的 AI 智能体执行，收集结果后汇报给你。

就像一个 CEO 管团队——只不过这个 CEO 永远不休息。

## 演示

```bash
$ python -m boss_agent "echo hello from Boss Agent"

==================================================
  Boss Agent v0.2.0
==================================================

  [Boss] 收到任务: echo hello from Boss Agent

  [Boss] 拆解中 (规则模式)...
  [Boss] 计划: 1 个子任务
    [T001] [shell       ] echo hello from Boss Agent

  [Boss] 执行中...
  --------------------------------------------------
  --------------------------------------------------

  [Boss] 结果: 1 成功, 0 失败 (24ms)

  [T001] 成功
    hello from Boss Agent

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

*零配置。基础模式不需要 API Key。*

## LLM 模式（v0.2.0）

Boss Agent v0.2.0 支持 **LLM 驱动的智能任务拆解**。不再依赖规则引擎，而是用 LLM 理解自然语言指令并智能拆解。

```bash
# 设置环境变量启用 LLM 模式
export BOSS_LLM_API_KEY="your-api-key"
export BOSS_LLM_BASE_URL="https://api.openai.com/v1"  # 或任何 OpenAI 兼容 API
export BOSS_LLM_MODEL="gpt-4o-mini"

# 用 LLM 拆解任务
python -m boss_agent "调研 AI Agent 框架并写一份对比报告"
```

设置了 `BOSS_LLM_API_KEY` 后自动启用 LLM 模式。没有 API Key 时自动回退到规则模式——零配置即可上手。

## 工作原理

```
用户说一句话
        |
        v
Boss 拆解为子任务（LLM 或规则引擎）
        |
        v
Boss 分派每个子任务给最合适的智能体
  +--------------+--------------+--------------+
  |  编码器       |  调研员       |  Shell        |
  |  Claude Code |  Web Search  |  任意命令     |
  +--------------+--------------+--------------+
        |
        v
Boss 收集结果并交付
```

> **灵感来自刘邦**——汉朝开国皇帝：*"我不擅长打仗，但我擅长找到最合适的人来打仗。* 将军打仗、谋士出策、丞相治国——各司其职。

## 架构

```
boss_agent/
  __main__.py          # CLI 入口
  decomposer.py        # 规则引擎拆解（Boss 的大脑）
  llm_decomposer.py    # LLM 智能拆解（v0.2 新增）
  llm_client.py        # OpenAI 兼容客户端（v0.2 新增）
  executor.py          # 智能体分派（Boss 的武将）
    ShellExecutor      # 任意 Shell 命令
    ClaudeCodeExecutor # 编码任务（v0.3）
    ResearchExecutor   # Web 调研（v0.3）
    ReviewExecutor     # 代码审查（v0.3）
```

| 组件 | 角色 | 类比 |
|------|------|------|
| `decomposer.py` | 规则拆解 | Boss 的直觉 |
| `llm_decomposer.py` | 智能拆解 | Boss 的深思熟虑 |
| `ShellExecutor` | 运行系统命令 | 萧何——丞相 |
| `ClaudeCodeExecutor` | 执行编码任务 | 韩信——大将军 |

## 当前状态

| 执行器 | 状态 | 说明 |
|--------|------|------|
| ShellExecutor | ✅ 可用 | 任意 Shell 命令 |
| LLM 拆解器 | ✅ 可用 | OpenAI 兼容，自动降级 |
| ClaudeCodeExecutor | 🔜 v0.3 | 调用 Claude Code 执行编码任务 |
| ResearchExecutor | 🔜 v0.3 | Web 搜索集成 |
| ReviewExecutor | 🔜 v0.3 | 代码审查 |

## 路线图

- [x] **v0.1** — 规则引擎拆解 + Shell 执行
- [x] **v0.2** — LLM 智能拆解 + 优雅降级
- [ ] **v0.3** — Claude Code 集成 + Web 搜索
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
