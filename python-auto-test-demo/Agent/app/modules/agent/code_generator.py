# -*- coding: utf-8 -*-
"""
Agent 接口用例代码生成器（核心模块1）

两条生成路径：
1. LLM 生成（实验组）：CoT + Few-shot 提示词，调用 Ollama 本地大模型，
   生成高覆盖 pytest 脚本；可注入 RAG 历史知识缓解幻觉；
2. 模板直出（降级 / 对照组基础能力）：Ollama 不可用时，
   基于接口参数类型规则化生成 正向/边界/异常/安全 用例，
   保证平台主流程在无 GPU / 未装模型环境下也能完整演示。

输入：OpenAPI 解析结果（dict）或自然语言接口描述（str）
输出：可运行的 pytest + requests 脚本文件（保存至 generated/cases/）
"""
from __future__ import annotations

import json
import logging
import re
from datetime import datetime
from pathlib import Path
from typing import Optional

from app.config import settings
from app.modules.agent.llm_client import get_llm
from app.modules.agent.prompt_templates import (
    SYSTEM_PROMPT,
    build_case_prompt,
    build_nl_prompt,
)

logger = logging.getLogger(__name__)

# SQL 注入等安全测试 payload 库（与实验数据集保持一致）
SQLI_PAYLOADS = [
    "' OR '1'='1",
    "1' OR '1'='1' --",
    "'; DROP TABLE users; --",
]
# 模拟被测服务的鉴权 token（mock 仅校验 Bearer 前缀）
DEFAULT_TOKEN = "test-token"


def _to_snake(name: str) -> str:
    """路径转合法的 Python 标识符片段"""
    cleaned = re.sub(r"[^0-9a-zA-Z\u4e00-\u9fa5]", "_", name)
    cleaned = re.sub(r"_+", "_", cleaned).strip("_")
    return cleaned or "endpoint"


def _safe_class_name(path: str, method: str) -> str:
    """由 path+method 生成类名，如 GET /api/users/{user_id} -> TestGetApiUsersUserId"""
    parts = re.split(r"[\/\-\.]", path)
    words = [method.lower()] + [p for p in parts if p]
    name = "".join(w.capitalize() for w in words)
    name = re.sub(r"[^0-9a-zA-Z]", "", name)
    return "Test" + name if not name.startswith("Test") else name


def _extract_code_block(text: str) -> Optional[str]:
    """从 LLM 输出中提取 ```python 代码块"""
    m = re.search(r"```(?:python|py)?\s*(.*?)```", text, re.S)
    if m:
        code = m.group(1).strip()
        if code:
            return code
    return None


# =====================================================================
# 模板直出（规则化生成，无 LLM 降级路径）
# =====================================================================
def _sample_values(schema: dict) -> dict:
    """
    根据参数 schema 生成 正常值 / 边界值 / 异常值。
    对 format（email/date/date-time）与 maxLength 做针对性取值，
    使生成的脚本能通过模拟被测服务的业务校验。
    """
    t = schema.get("type", "string")
    fmt = schema.get("format")

    if schema.get("enum"):
        return {
            "normal": schema["enum"][0],
            "boundary": schema["enum"][-1],
            "abnormal": "__invalid_enum__",
        }
    if t in ("integer", "number"):
        return {"normal": 1, "boundary": 0, "abnormal": -1}
    if t == "boolean":
        return {"normal": True, "boundary": False, "abnormal": "not_a_bool"}

    # string 各格式
    if fmt == "email":
        return {"normal": "test@example.com", "boundary": "a@b.c", "abnormal": "not-an-email"}
    if fmt == "date":
        return {"normal": "2026-01-01", "boundary": "2026-12-31", "abnormal": "not-a-date"}
    if fmt == "date-time":
        return {
            "normal": "2026-01-01T00:00:00Z",
            "boundary": "2026-01-01T00:00:00Z",
            "abnormal": "not-a-datetime",
        }
    max_len = schema.get("maxLength")
    if isinstance(max_len, int):
        return {"normal": "test_user", "boundary": "A" * max_len, "abnormal": "A" * (max_len + 1)}
    return {"normal": "test_user", "boundary": "", "abnormal": "A" * 100}


def build_template_script(interface: dict, servers: list[str]) -> str:
    """基于接口定义规则化生成 pytest 脚本（无 LLM 时的降级 / 对照组基础能力）"""
    method = interface.get("method", "GET").lower()
    path = interface.get("path", "/")
    summary = interface.get("summary") or f"{method.upper()} {path}"
    base_url = (servers or [settings.MOCK_BASE_URL])[0]

    body_schema = (interface.get("request_body") or {}).get("schema") or {}
    body_props = body_schema.get("properties") or {}
    body_required = body_schema.get("required") or list(body_props.keys())
    params = interface.get("parameters") or []
    need_auth = bool(interface.get("security"))

    path_params = {p["name"]: p for p in params if p.get("in") == "path"}
    query_params = {p["name"]: p for p in params if p.get("in") == "query"}

    lines: list[str] = []
    lines.append("# -*- coding: utf-8 -*-")
    lines.append(f'"""自动生成：{method.upper()} {path} - {summary}"""')
    lines.append("import pytest")
    lines.append("import requests")
    lines.append("")
    lines.append(f'BASE_URL = "{base_url}"')
    if need_auth:
        lines.append(f'TOKEN = "{DEFAULT_TOKEN}"  # 鉴权 token（按被测系统配置）')
    lines.append("")
    lines.append(f"class {_safe_class_name(path, method)}:")
    lines.append(f'    """{summary}"""')
    lines.append("")

    # ---------- 工具函数：构造请求表达式 ----------
    def _url_for(path_vals: dict, query_kv: list) -> str:
        """构造 f-string URL 表达式"""
        url = path
        for name, val in path_vals.items():
            url = url.replace("{" + name + "}", str(val))
        qs = "&".join(f"{k}={v}" for k, v in query_kv)
        if qs:
            url += "?" + qs
        return f'f"{base_url}{url}"'

    def _call(url_expr: str, body: Optional[str] = None) -> str:
        call = f"requests.{method}({url_expr}"
        if body is not None:
            call += f", json={body}"
        if need_auth:
            call += ', headers={"Authorization": "Bearer " + TOKEN}'
        call += ")"
        return call

    def _values(p: dict, kind: str):
        return _sample_values(p.get("schema") or {})[kind]

    path_ok = {name: _values(p, "normal") for name, p in path_params.items()}
    path_steal = {name: 999999 for name in path_params}
    query_ok = [(name, _values(p, "normal")) for name, p in query_params.items()]
    query_b = [(name, _values(p, "boundary")) for name, p in query_params.items()]
    body_ok = {name: _values({"schema": body_props.get(name) or {"type": "string"}}, "normal")
               for name in body_props}
    body_b = {name: _values({"schema": body_props.get(name) or {"type": "string"}}, "boundary")
              for name in body_props}

    # ---------- 1. 正向用例 ----------
    lines.append("    def test_正向_正常请求(self):")
    lines.append(f"        resp = {_call(_url_for(path_ok, query_ok), json.dumps(body_ok, ensure_ascii=False))}")
    lines.append("        assert resp.status_code == 200")
    lines.append("        assert 'code' in resp.json()")
    lines.append("")

    # ---------- 2. 边界值用例 ----------
    lines.append("    def test_边界_边界值(self):")
    lines.append(f"        resp = {_call(_url_for(path_ok, query_b), json.dumps(body_b, ensure_ascii=False))}")
    lines.append("        assert resp.status_code < 500  # 边界值允许被业务层拒绝(4xx)")
    lines.append("")

    # ---------- 3. 异常参数用例（缺少必填字段/参数） ----------
    if body_required:
        missing_body = {k: body_ok[k] for k in body_ok if k not in (body_required[0],)}
        lines.append("    def test_异常_缺少必填字段(self):")
        lines.append(f"        resp = {_call(_url_for(path_ok, query_ok), json.dumps(missing_body, ensure_ascii=False))}")
        lines.append("        assert resp.status_code in (400, 422)")
        lines.append("")
    elif query_params:
        # 仅当存在必填 query 参数时生成"缺少必填参数"用例
        required_query = [name for name, p in query_params.items() if p.get("required")]
        if required_query:
            target = required_query[0]
            missing_query = [(name, v) for name, v in query_ok if name != target]
            lines.append("    def test_异常_缺少必填参数(self):")
            lines.append(f"        resp = {_call(_url_for(path_ok, missing_query))}")
            lines.append("        assert resp.status_code in (400, 422)")
            lines.append("")

    # ---------- 4. 安全用例：SQL 注入 ----------
    lines.append("    def test_安全_SQL注入(self):")
    if body_props:
        target = list(body_props.keys())[0]
        inj_body = {**body_ok, target: SQLI_PAYLOADS[0]}
        lines.append(f"        resp = {_call(_url_for(path_ok, query_ok), json.dumps(inj_body, ensure_ascii=False))}")
    elif query_params:
        target = list(query_params.keys())[0]
        q_inj = [(name, SQLI_PAYLOADS[0] if name == target else v) for name, v in query_ok]
        lines.append(f"        resp = {_call(_url_for(path_ok, q_inj))}")
    elif path_params:
        target = list(path_params.keys())[0]
        p_inj = {**path_ok, target: SQLI_PAYLOADS[0]}
        lines.append(f"        resp = {_call(_url_for(p_inj, query_ok), json.dumps(body_ok, ensure_ascii=False))}")
    else:
        lines.append("        pytest.skip('该接口无可注入参数')")
    lines.append("        assert resp.status_code in (400, 422, 500)  # 注入应被拒绝")
    lines.append("")

    # ---------- 5. 安全用例：越权 / 资源不存在 ----------
    if path_params:
        lines.append("    def test_安全_越权访问(self):")
        lines.append(f"        resp = {_call(_url_for(path_steal, query_ok), json.dumps(body_ok, ensure_ascii=False))}")
        lines.append("        assert resp.status_code in (403, 404)  # 越权/资源不存在应被拒绝")
        lines.append("")
    elif "user_id" in body_props:
        lines.append("    def test_安全_越权访问(self):")
        steal_body = {**body_ok, "user_id": 999999}
        lines.append(f"        resp = {_call(_url_for(path_ok, query_ok), json.dumps(steal_body, ensure_ascii=False))}")
        lines.append("        assert resp.status_code in (403, 404)  # 越权/资源不存在应被拒绝")
        lines.append("")

    return "\n".join(lines)


# =====================================================================
# 主生成流程
# =====================================================================
def generate_case_script(
    endpoint: dict,
    servers: list[str],
    knowledge: str = "",
    use_llm: bool = True,
    save: bool = True,
) -> dict:
    """
    生成单个接口的 pytest 脚本。

    返回：
    {
        "path": 脚本文件绝对路径,
        "content": 脚本源码,
        "source": "llm" | "template",
        "title": 接口摘要,
    }
    """
    interface_json = json.dumps(endpoint, ensure_ascii=False, indent=2)
    prompt = build_case_prompt(interface_json, knowledge)

    content: Optional[str] = None
    source = "llm"

    if use_llm:
        llm = get_llm()
        if llm.is_available():
            raw = llm.generate_with_retry(SYSTEM_PROMPT, prompt)
            content = _extract_code_block(raw) if raw else None
            if content:
                logger.info("LLM 生成成功：%s %s", endpoint["method"], endpoint["path"])

    if not content:
        # LLM 不可用或输出不合法 -> 模板直出
        content = build_template_script(endpoint, servers)
        source = "template"

    # 保存文件
    file_name = f"{endpoint['method'].lower()}_{_to_snake(endpoint['path'])}.py"
    case_path = settings.CASE_DIR / file_name
    case_path.write_text(content, encoding="utf-8")

    return {
        "path": str(case_path),
        "content": content,
        "source": source,
        "title": endpoint.get("summary") or f"{endpoint['method']} {endpoint['path']}",
        "endpoint": endpoint["path"],
        "method": endpoint["method"],
    }


def generate_from_nl(description: str, knowledge: str = "", use_llm: bool = True) -> dict:
    """自然语言描述接口 -> 生成脚本（无 OpenAPI 场景）"""
    prompt = build_nl_prompt(description, knowledge)

    content: Optional[str] = None
    source = "llm"

    if use_llm:
        llm = get_llm()
        if llm.is_available():
            raw = llm.generate_with_retry(SYSTEM_PROMPT, prompt)
            content = _extract_code_block(raw) if raw else None

    if not content:
        # 自然语言场景无法模板直出，给出可编辑的占位脚本
        content = (
            "# -*- coding: utf-8 -*-\n"
            f'"""自动生成：{description[:60]}"""\n'
            "import pytest\nimport requests\n\n"
            'BASE_URL = "http://localhost:9000"\n\n'
            "class TestNlInterface:\n"
            "    def test_placeholder(self):\n"
            "        # TODO: 请根据 LLM 输出填写具体用例\n"
            "        pass\n"
        )
        source = "template"

    file_name = f"nl_{datetime.now().strftime('%Y%m%d_%H%M%S')}.py"
    case_path = settings.CASE_DIR / file_name
    case_path.write_text(content, encoding="utf-8")

    return {
        "path": str(case_path),
        "content": content,
        "source": source,
        "title": description[:80],
        "endpoint": "",
        "method": "",
    }
