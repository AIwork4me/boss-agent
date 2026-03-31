"""
Boss Agent - LLM 客户端

支持 OpenAI 兼容 API（OpenAI、DeepSeek、Ollama 等）。
刘邦不会亲自打每一个电话，但他的信使系统必须可靠。
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
    """LLM 配置"""
    api_key: str = ""
    base_url: str = "https://api.openai.com/v1"
    model: str = "gpt-4o-mini"
    temperature: float = 0.3
    max_tokens: int = 2048
    timeout: int = 30


@dataclass
class LLMMessage:
    """一条消息"""
    role: str  # system / user / assistant
    content: str


@dataclass
class LLMResponse:
    """LLM 响应"""
    content: str
    model: str = ""
    usage: dict = field(default_factory=dict)
    success: bool = True
    error: str = ""


class LLMClient:
    """
    LLM 客户端——信使系统
    
    支持 OpenAI 兼容 API。
    不依赖任何第三方库，只用标准库的 urllib。
    """

    def __init__(self, config: Optional[LLMConfig] = None):
        self.config = config or self._load_config()

    @staticmethod
    def _load_config() -> LLMConfig:
        """从环境变量加载配置"""
        return LLMConfig(
            api_key=os.environ.get("BOSS_LLM_API_KEY", ""),
            base_url=os.environ.get("BOSS_LLM_BASE_URL", "https://api.openai.com/v1"),
            model=os.environ.get("BOSS_LLM_MODEL", "gpt-4o-mini"),
            temperature=float(os.environ.get("BOSS_LLM_TEMPERATURE", "0.3")),
            max_tokens=int(os.environ.get("BOSS_LLM_MAX_TOKENS", "2048")),
            timeout=int(os.environ.get("BOSS_LLM_TIMEOUT", "30")),
        )

    @property
    def is_available(self) -> bool:
        """LLM 是否可用（有 API Key）"""
        return bool(self.config.api_key)

    def chat(
        self,
        messages: list[LLMMessage],
        temperature: Optional[float] = None,
        max_tokens: Optional[int] = None,
    ) -> LLMResponse:
        """
        发送聊天请求
        
        Args:
            messages: 消息列表
            temperature: 温度（可选，覆盖配置）
            max_tokens: 最大 token 数（可选，覆盖配置）
        
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
            "temperature": temperature or self.config.temperature,
            "max_tokens": max_tokens or self.config.max_tokens,
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
