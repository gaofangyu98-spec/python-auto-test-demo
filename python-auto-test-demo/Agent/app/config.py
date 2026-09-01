# -*- coding: utf-8 -*-
"""
全局配置中心
支持通过环境变量覆盖，便于不同机器 / 答辩演示环境灵活切换。
"""
import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent


class Settings:
    # ---------- Web 服务 ----------
    APP_HOST: str = os.getenv("APP_HOST", "0.0.0.0")
    APP_PORT: int = int(os.getenv("APP_PORT", "8000"))

    # ---------- Ollama 本地大模型 ----------
    # 本地开源模型（本科毕设不训练模型，直接使用 Ollama 拉取的量化模型）
    OLLAMA_BASE_URL: str = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")
    LLM_MODEL: str = os.getenv("LLM_MODEL", "qwen2.5:7b")
    LLM_TEMPERATURE: float = float(os.getenv("LLM_TEMPERATURE", "0.2"))
    LLM_TIMEOUT: int = int(os.getenv("LLM_TIMEOUT", "180"))
    # 当 Ollama 未启动 / 模型不存在时，是否降级为"模板直出"模式，
    # 保证平台主流程（解析->生成->执行）在无 GPU 环境下也能演示。
    LLM_MOCK_FALLBACK: bool = os.getenv("LLM_MOCK_FALLBACK", "true").lower() == "true"

    # ---------- 数据库 ----------
    DATABASE_URL: str = os.getenv("DATABASE_URL", f"sqlite:///{BASE_DIR / 'app.db'}")

    # ---------- 目录 ----------
    CASE_DIR: Path = BASE_DIR / "generated" / "cases"      # 生成的接口用例脚本
    REPORT_DIR: Path = BASE_DIR / "generated" / "reports"  # 执行报告
    KNOWLEDGE_DIR: Path = BASE_DIR / "knowledge"           # RAG 知识库上传目录

    # ---------- 模拟被测业务服务 ----------
    # 实验使用的模拟游戏业务接口（用户/道具/充值/PVP积分），见 mock_service/
    MOCK_BASE_URL: str = os.getenv("MOCK_BASE_URL", "http://localhost:9000")


settings = Settings()

# 确保关键目录存在
for _dir in (settings.CASE_DIR, settings.REPORT_DIR, settings.KNOWLEDGE_DIR):
    _dir.mkdir(parents=True, exist_ok=True)
