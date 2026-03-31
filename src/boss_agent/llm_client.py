"""Boss Agent - LLM Client (v0.2)

OpenAI-compatible API client using only stdlib (no third-party deps).
"""

from __future__ import annotations

import json
import os
import urllib.request
import urllib.error
from dataclasses import dataclass, field
from typing import Optional


@dataclass
class LLMConfig:
    """LLM configuration."""
    api_key: str = ""
    base_url: str = "https://api.openai.com/v1"
    model: str = "gpt-4o-mini"
    temperature: float = 0.3
    max_tokens: int = 2048
    timeout: int = 30


@dataclass
class LLMMessage:
    """A single message."""
    role: str  # system / user / assistant
    content: str


@dataclass
class LLMResponse:
    """LLM response."""
    content: str
    model: str = ""
    usage: dict = field(default_factory=dict)
    success: bool = True
    error: str = ""


class LLMClient:
    """
    LLM Client - the messenger system.
    
    Supports OpenAI-compatible APIs.
    No third-party dependencies - uses only stdlib urllib.
    """

    def __init__(self, config: Optional[LLMConfig] = None):
        self.config = config or self._load_config()

    @staticmethod
    def _load_config() -> LLMConfig:
        """Load config from environment variables with safe parsing."""
        def _env_float(key: str, default: float) -> float:
            try:
                return float(os.environ.get(key, str(default)))
            except (ValueError, TypeError):
                return default

        def _env_int(key: str, default: int) -> int:
            try:
                return int(os.environ.get(key, str(default)))
            except (ValueError, TypeError):
                return default

        return LLMConfig(
            api_key=os.environ.get("BOSS_LLM_API_KEY", ""),
            base_url=os.environ.get("BOSS_LLM_BASE_URL", "https://api.openai.com/v1"),
            model=os.environ.get("BOSS_LLM_MODEL", "gpt-4o-mini"),
            temperature=_env_float("BOSS_LLM_TEMPERATURE", 0.3),
            max_tokens=_env_int("BOSS_LLM_MAX_TOKENS", 2048),
            timeout=_env_int("BOSS_LLM_TIMEOUT", 30),
        )

    @property
    def is_available(self) -> bool:
        """Check if LLM is available (has API key)."""
        return bool(self.config.api_key)

    def chat(
        self,
        messages: list[LLMMessage],
        temperature: Optional[float] = None,
        max_tokens: Optional[int] = None,
    ) -> LLMResponse:
        """
        Send a chat request.

        Args:
            messages: Message list
            temperature: Optional temperature override
            max_tokens: Optional max_tokens override

        Returns:
            LLMResponse
        """
        if not self.is_available:
            return LLMResponse(
                content="",
                success=False,
                error="LLM not available: no API key configured. Set BOSS_LLM_API_KEY.",
            )

        url = f"{self.config.base_url.rstrip('/')}/chat/completions"
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.config.api_key}",
        }

        body = {
            "model": self.config.model,
            "messages": [{"role": m.role, "content": m.content} for m in messages],
            "temperature": temperature if temperature is not None else self.config.temperature,
            "max_tokens": max_tokens if max_tokens is not None else self.config.max_tokens,
        }

        req = urllib.request.Request(
            url,
            data=json.dumps(body).encode("utf-8"),
            headers=headers,
            method="POST",
        )

        try:
            with urllib.request.urlopen(req, timeout=self.config.timeout) as resp:
                data = json.loads(resp.read().decode("utf-8"))
                content = data["choices"][0]["message"]["content"]
                return LLMResponse(
                    content=content,
                    model=data.get("model", ""),
                    usage=data.get("usage", {}),
                    success=True,
                )
        except urllib.error.HTTPError as e:
            error_body = ""
            try:
                error_body = e.read().decode("utf-8", errors="replace")
            except Exception:
                pass
            return LLMResponse(
                content="",
                success=False,
                error=f"HTTP {e.code}: {error_body[:500]}",
            )
        except urllib.error.URLError as e:
            return LLMResponse(
                content="",
                success=False,
                error=f"URL Error: {e.reason}",
            )
        except Exception as e:
            return LLMResponse(
                content="",
                success=False,
                error=f"Unexpected error: {type(e).__name__}: {e}",
            )
