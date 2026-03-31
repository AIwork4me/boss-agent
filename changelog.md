# Changelog

All notable changes to Boss Agent will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.2.0] - 2026-03-31

### Added
- LLM-powered task decomposition via OpenAI-compatible API
- `llm_client.py` — lightweight HTTP client (pure `urllib`, zero external deps)
- `llm_decomposer.py` — intelligent decomposition with graceful fallback to rule-based engine
- Environment variable configuration: `BOSS_LLM_API_KEY`, `BOSS_LLM_BASE_URL`, `BOSS_LLM_MODEL`
- Dual-mode operation: LLM mode when API key is set, rule-based mode otherwise
- Dependency ID remapping: LLM index-based references resolved to generated IDs
- Markdown fence stripping for robust LLM output parsing
- 23 unit tests covering all core modules

### Fixed
- Temperature `0.0` treated as falsy (now uses `is not None` check)
- Environment variable parsing crashes on invalid values (added safe parsing helpers)
- Dependency chain broken between LLM output and generated task IDs

## [0.1.0] - 2026-03-31

### Added
- Rule-based task decomposition with keyword detection
- Shell executor for running system commands
- TaskPlan data model with subtask dependencies
- CLI interface via `python -m boss_agent`
- MIT License
