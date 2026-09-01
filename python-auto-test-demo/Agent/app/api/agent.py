# -*- coding: utf-8 -*-
"""
核心 Agent API 路由（第一版）
- POST /api/openapi/parse   解析 OpenAPI 文档
- POST /api/agent/generate  Agent 生成接口用例脚本（OpenAPI 或自然语言）
- POST /api/agent/run       执行生成的脚本
"""
from __future__ import annotations

from typing import Optional

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import CaseRecord, ExecRecord
from app.modules.agent.code_generator import generate_case_script, generate_from_nl
from app.modules.executor.runner import run_case_file
from app.modules.openapi.parser import parse_openapi

router = APIRouter(prefix="/api", tags=["Agent核心"])


# ---------------- 请求模型 ----------------
class OpenApiParseReq(BaseModel):
    content: str = Field(..., description="OpenAPI 3.0 文档内容（yaml/json）")


class GenerateReq(BaseModel):
    openapi_content: Optional[str] = Field(None, description="OpenAPI 文档内容")
    description: Optional[str] = Field(None, description="自然语言接口描述（无OpenAPI时）")
    knowledge: str = Field("", description="RAG 检索到的历史知识（实验组注入）")
    use_llm: bool = Field(True, description="是否使用 LLM 生成（False 走模板）")
    save: bool = Field(True, description="是否保存到 generated/cases")


class RunReq(BaseModel):
    case_path: str = Field(..., description="待执行用例脚本路径")


# ---------------- 1. OpenAPI 解析 ----------------
@router.post("/openapi/parse")
def api_parse_openapi(req: OpenApiParseReq):
    try:
        result = parse_openapi(req.content)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e)) from e
    return {
        "code": 0,
        "data": {
            "title": result["title"],
            "version": result["version"],
            "servers": result["servers"],
            "endpoint_count": len(result["endpoints"]),
            "endpoints": result["endpoints"],
        },
    }


# ---------------- 2. Agent 生成 ----------------
@router.post("/agent/generate")
def api_generate(req: GenerateReq, db: Session = Depends(get_db)):
    if not req.openapi_content and not req.description:
        raise HTTPException(status_code=400, detail="必须提供 openapi_content 或 description")

    try:
        if req.openapi_content:
            parsed = parse_openapi(req.openapi_content)
            servers = parsed["servers"] or []
            cases = []
            for ep in parsed["endpoints"]:
                case = generate_case_script(
                    ep, servers, knowledge=req.knowledge,
                    use_llm=req.use_llm, save=req.save,
                )
                cases.append(case)
                # 落库
                record = CaseRecord(
                    title=case["title"], path=case["path"],
                    method=case["method"], endpoint=case["endpoint"],
                    source_type="openapi", content=case["content"],
                )
                db.add(record)
        else:
            case = generate_from_nl(req.description, req.knowledge, use_llm=req.use_llm)
            cases = [case]
            record = CaseRecord(
                title=case["title"], path=case["path"],
                source_type="nl", content=case["content"],
            )
            db.add(record)

        db.commit()
    except ValueError as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=str(e)) from e

    return {
        "code": 0,
        "data": {
            "count": len(cases),
            "cases": [
                {
                    "title": c["title"], "path": c["path"],
                    "source": c["source"], "method": c["method"],
                    "endpoint": c["endpoint"], "content": c["content"],
                }
                for c in cases
            ],
        },
    }


# ---------------- 3. 执行 ----------------
@router.post("/agent/run")
def api_run(req: RunReq, db: Session = Depends(get_db)):
    import os
    if not os.path.exists(req.case_path):
        raise HTTPException(status_code=404, detail=f"用例文件不存在：{req.case_path}")

    result = run_case_file(req.case_path)

    record = ExecRecord(
        status="passed" if result.success else "failed",
        passed=result.passed, failed=result.failed, total=result.total,
        output=result.output, error=result.error,
    )
    db.add(record)
    db.commit()

    return {"code": 0, "data": result.to_dict(), "exec_id": record.id}
