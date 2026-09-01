# -*- coding: utf-8 -*-
"""
本地大模型客户端（Ollama）

设计说明：
- 通过 Ollama HTTP API（/api/chat）直连本地模型，Python 3.13 下依赖最轻、最稳定；
- 预留 LangChain 接入点：后续 RAG 阶段可平滑替换为 langchain-ollama 的 ChatOllama，
  本类只暴露 chat(system, user) 一个统一接口，上层无需改动；
- 提供 mock 降级：Ollama 未启动 / 模型未拉取时，返回 None，
  由 code_generator 走"模板直出"分支，保证平台主流程在无 GPU 环境可演示。

启动 Ollama 的命令（供参考，不随代码执行）：
    ollama serve
    ollama pull qwen2.5:7b
"""
from __future__ import annotations

import logging
import time
from typing import Optional

import requests

from app.config import settings

logger = logging.getLogger(__name__)


class LLMClient:
    """Ollama 本地大模型客户端"""

    def __init__(
        self,
        base_url: Optional[str] = None,
        model: Optional[str] = None,
        temperature: Optional[float] = None,
        timeout: Optional[int] = None,
    ):
        self.base_url = (base_url or settings.OLLAMA_BASE_URL).rstrip("/")
        self.model = model or settings.LLM_MODEL
        self.temperature = temperature if temperature is not None else settings.LLM_TEMPERATURE
        self.timeout = timeout or settings.LLM_TIMEOUT

    # ---------- 可用性探测 ----------
    def is_available(self) -> bool:
        """检查 Ollama 服务是否可达，以及模型是否存在"""
        try:
            resp = requests.get(f"{self.base_url}/api/tags", timeout=3)
            if resp.status_code != 200:
                return False
            models = [m.get("name", "") for m in resp.json().get("models", [])]
            return any(self.model in name or name in self.model for name in models)
        except requests.RequestException:
            return False

    def list_models(self) -> list[str]:
        try:
            resp = requests.get(f"{self.base_url}/api/tags", timeout=3)
            return [m.get("name", "") for m in resp.json().get("models", [])]
        except requests.RequestException:
            return []

    # ---------- 对话 ----------
    def chat(self, system: str, user: str, temperature: Optional[float] = None) -> Optional[str]:
        """
        调用 Ollama /api/chat 生成文本。
        返回生成内容；若服务不可用返回 None（由上层降级处理）。
        """
        payload = {
            "model": self.model,
            "messages": [
                {"role": "system", "content": system},
                {"role": "user", "content": user},
            ],
            "stream": False,
            "options": {
                "temperature": self.temperature if temperature is None else temperature,
                "num_predict": 4096,
            },
        }
        try:
            resp = requests.post(
                f"{self.base_url}/api/chat", json=payload, timeout=self.timeout
            )
            resp.raise_for_status()
            data = resp.json()
            return data.get("message", {}).get("content") or ""
        except requests.RequestException as e:
            logger.warning("调用 Ollama 失败（%s），服务可能未启动", e)
            return None

    def generate_with_retry(
        self, system: str, user: str, retries: int = 1, **kwargs
    ) -> Optional[str]:
        """带简单重试的生成"""
        for i in range(retries + 1):
            result = self.chat(system, user, **kwargs)
            if result:
                return result
            if i < retries:
                time.sleep(2)
        return None


# 全局单例
_llm: Optional[LLMClient] = None


def get_llm() -> LLMClient:
    global _llm
    if _llm is None:
        _llm = LLMClient()
    return _llm
