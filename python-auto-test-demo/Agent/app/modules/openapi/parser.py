# -*- coding: utf-8 -*-
"""
OpenAPI 3.0 文档解析器（核心模块1）

功能：
- 支持上传 OpenAPI 3.0 的 yaml / json 文件（内容字符串）
- 解析：servers、paths、HTTP method、请求参数（query/path/header/cookie）、
  请求体（requestBody）、响应（responses）、错误码
- 递归解析 Schema 与 $ref 引用，输出标准化结构，供 Agent 生成用例代码

标准化输出示例（dict）：
{
  "title": "模拟游戏业务接口",
  "version": "1.0.0",
  "servers": ["http://localhost:9000"],
  "endpoints": [
    {
      "path": "/api/users/{user_id}",
      "method": "get",
      "summary": "查询用户信息",
      "operation_id": "getUserById",
      "tags": ["用户"],
      "parameters": [{"name": "user_id", "in": "path", "required": true, "schema": {...}}],
      "request_body": {...} | None,
      "responses": {"200": {"description": "成功"}, "404": {...}}
    }
  ]
}
"""
import json
from typing import Any, Dict, List, Optional

import yaml


class OpenApiParser:
    """OpenAPI 3.0 文档解析器"""

    def __init__(self, content: str):
        # 兼容传入 dict 或字符串
        if isinstance(content, (dict, list)):
            self.doc: dict = content
        else:
            self.doc: dict = self._load(content)

    # ---------- 装载 ----------
    @staticmethod
    def _load(content: str) -> dict:
        text = content.strip()
        try:
            if text.startswith("{"):
                return json.loads(text)
            return yaml.safe_load(text)
        except Exception as e:  # noqa: BLE001
            raise ValueError(f"无法解析 OpenAPI 文档（应为 YAML 或 JSON）：{e}") from e

    def validate(self) -> None:
        """校验是否为 OpenAPI 3.0 文档"""
        if not isinstance(self.doc, dict):
            raise ValueError("OpenAPI 文档根节点必须是对象")
        if "openapi" not in self.doc or "paths" not in self.doc:
            raise ValueError("缺少 openapi 或 paths 字段，请确认是 OpenAPI 3.0 文档")
        version = str(self.doc.get("openapi", ""))
        if not version.startswith("3."):
            raise ValueError(f"当前仅支持 OpenAPI 3.x，收到版本：{version}")

    # ---------- 顶层信息 ----------
    def get_title(self) -> str:
        return self.doc.get("info", {}).get("title", "未命名接口")

    def get_version(self) -> str:
        return self.doc.get("info", {}).get("version", "")

    def get_servers(self) -> List[str]:
        servers = self.doc.get("servers") or []
        return [s.get("url", "") for s in servers if s.get("url")]

    # ---------- $ref 解析 ----------
    def _resolve_ref(self, ref: str, visited: Optional[set] = None) -> dict:
        """解析 '#/components/schemas/xxx' 形式的引用，防循环"""
        visited = visited or set()
        if ref in visited:
            return {"$ref_cycle": ref}
        visited.add(ref)
        parts = [p for p in ref.lstrip("#/").split("/") if p]
        node: Any = self.doc
        for p in parts:
            if not isinstance(node, dict) or p not in node:
                return {"$ref": ref, "resolved": False}
            node = node[p]
        # 若引用的还是引用，继续解
        if isinstance(node, dict) and "$ref" in node:
            return self._resolve_ref(node["$ref"], visited)
        return node or {}

    def _resolve(self, node: Any) -> Any:
        """深度解析：把 schema 里的 $ref 替换为真实定义"""
        if isinstance(node, dict):
            if "$ref" in node and isinstance(node["$ref"], str):
                return self._resolve_ref(node["$ref"])
            return {k: self._resolve(v) for k, v in node.items()}
        if isinstance(node, list):
            return [self._resolve(i) for i in node]
        return node

    # ---------- Schema 提取 ----------
    @staticmethod
    def _type_of(schema: dict) -> str:
        """从 schema 中提取类型描述（用于 Agent 生成测试数据）"""
        t = schema.get("type", "object")
        fmt = schema.get("format")
        if t == "string":
            if fmt == "date-time":
                return "string(date-time)"
            if fmt == "date":
                return "string(date)"
            if fmt == "email":
                return "string(email)"
            if schema.get("enum"):
                return f"enum{list(schema['enum'])}"
            if schema.get("maxLength") or schema.get("minLength"):
                return f"string(len {schema.get('minLength', 0)}-{schema.get('maxLength', '∞')})"
            return "string"
        if t == "integer":
            rng = f"[{schema.get('minimum', '-∞')},{schema.get('maximum', '+∞')}]"
            return f"integer{rng}"
        if t == "number":
            return "number"
        if t == "boolean":
            return "boolean"
        if t == "array":
            item = schema.get("items") or {}
            return f"array<{OpenApiParser._type_of(item)}>"
        if t == "object":
            props = schema.get("properties") or {}
            required = schema.get("required") or []
            desc = ",".join(props.keys()) if props else ""
            return f"object{{{desc}}}{' req:' + ','.join(required) if required else ''}"
        if schema.get("enum"):
            return f"enum{list(schema['enum'])}"
        return t or "any"

    def _extract_parameters(self, parameters: List[dict]) -> List[dict]:
        """提取 path/query/header/cookie 参数"""
        result = []
        for p in parameters or []:
            schema = self._resolve(p.get("schema") or {})
            result.append({
                "name": p.get("name", ""),
                "in": p.get("in", ""),            # path/query/header/cookie
                "required": bool(p.get("required", False)),
                "description": p.get("description", ""),
                "type": self._type_of(schema),
                "schema": schema,
            })
        return result

    def _extract_request_body(self, request_body: Optional[dict]) -> Optional[dict]:
        if not request_body:
            return None
        content = request_body.get("content") or {}
        # 优先取 application/json
        media = content.get("application/json") or content.get("*/*") or (
            next(iter(content.values())) if content else None
        )
        if not media:
            return {"required": bool(request_body.get("required", False)), "media": None}
        schema = self._resolve(media.get("schema") or {})
        return {
            "required": bool(request_body.get("required", False)),
            "media_type": "application/json",
            "type": self._type_of(schema),
            "schema": schema,
        }

    def _extract_responses(self, responses: dict) -> List[dict]:
        """提取响应（含错误码）"""
        result = []
        for code, resp in (responses or {}).items():
            desc = ""
            if isinstance(resp, dict):
                desc = resp.get("description", "")
            result.append({"code": str(code), "description": desc or ""})
        return result

    # ---------- 主流程 ----------
    def parse(self) -> dict:
        """解析整份文档，返回标准化结构"""
        self.validate()
        endpoints: List[dict] = []
        paths = self.doc.get("paths") or {}
        top_security = self.doc.get("security")  # 顶层安全定义（可为 None / []）

        for path, path_item in paths.items():
            if not isinstance(path_item, dict):
                continue
            for method in ("get", "post", "put", "delete", "patch", "head", "options"):
                op = path_item.get(method)
                if not isinstance(op, dict):
                    continue
                parameters = list(op.get("parameters") or []) + list(
                    path_item.get("parameters") or []
                )
                # 安全要求：操作级优先，未定义时继承顶层
                op_security = op.get("security", top_security)
                if op_security is None:
                    op_security = []
                endpoints.append({
                    "path": path,
                    "method": method.upper(),
                    "summary": op.get("summary", "") or op.get("operationId", ""),
                    "operation_id": op.get("operationId", ""),
                    "tags": op.get("tags") or [],
                    "parameters": self._extract_parameters(parameters),
                    "request_body": self._extract_request_body(op.get("requestBody")),
                    "responses": self._extract_responses(op.get("responses") or {}),
                    "security": op_security,  # 非空表示接口需要鉴权
                })

        return {
            "title": self.get_title(),
            "version": self.get_version(),
            "servers": self.get_servers(),
            "endpoints": endpoints,
        }


def parse_openapi(content: str) -> dict:
    """便捷入口"""
    return OpenApiParser(content).parse()
