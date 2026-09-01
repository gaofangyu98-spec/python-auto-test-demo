# -*- coding: utf-8 -*-
"""
FastAPI 应用入口（服务层）

启动方式：
    uvicorn app.main:app --host 0.0.0.0 --port 8000
或
    python run.py
"""
from __future__ import annotations

import logging

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.agent import router as agent_router
from app.config import settings
from app.database import init_db

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(name)s: %(message)s")

app = FastAPI(
    title="混合智能自动化测试平台",
    description="基于大模型Agent的混合智能自动化测试平台（接口为主，UI为辅）",
    version="0.1.0",
)

# CORS：允许前端 Vue3 开发服务器访问
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 注册路由
app.include_router(agent_router)


@app.on_event("startup")
def on_startup() -> None:
    init_db()
    logging.info("数据库初始化完成：%s", settings.DATABASE_URL)


@app.get("/")
def root():
    return {
        "service": "混合智能自动化测试平台",
        "version": "0.1.0",
        "docs": "/docs",
    }


@app.get("/api/health")
def health():
    from app.modules.agent.llm_client import get_llm
    llm = get_llm()
    return {
        "status": "ok",
        "llm_available": llm.is_available(),
        "llm_model": settings.LLM_MODEL,
        "llm_base_url": settings.OLLAMA_BASE_URL,
        "mock_service": settings.MOCK_BASE_URL,
    }
