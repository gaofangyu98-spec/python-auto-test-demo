# -*- coding: utf-8 -*-
"""
OpenAPI 解析器单元测试
运行：python -m pytest tests/test_parser.py -v
"""
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from app.modules.openapi.parser import OpenApiParser  # noqa: E402

OPENAPI_YAML = r"""
openapi: "3.0.3"
info:
  title: 测试接口
  version: "1.0.0"
servers:
  - url: "http://localhost:9000"
paths:
  /api/users/{user_id}:
    get:
      summary: 查询用户
      operationId: getUserById
      parameters:
        - name: user_id
          in: path
          required: true
          schema: { type: integer, minimum: 1 }
      responses:
        "200": { description: 成功 }
        "404": { description: 用户不存在 }
  /api/recharge:
    post:
      summary: 充值
      requestBody:
        required: true
        content:
          application/json:
            schema:
              type: object
              required: [amount, channel]
              properties:
                amount: { type: number, exclusiveMinimum: 0 }
                channel:
                  type: string
                  enum: [wechat, alipay]
      responses:
        "200": { description: 成功 }
"""


def test_parse_basic():
    parser = OpenApiParser(OPENAPI_YAML)
    result = parser.parse()
    assert result["title"] == "测试接口"
    assert result["servers"] == ["http://localhost:9000"]
    assert len(result["endpoints"]) == 2


def test_parse_path_method():
    result = OpenApiParser(OPENAPI_YAML).parse()
    methods = {(e["path"], e["method"]) for e in result["endpoints"]}
    assert ("/api/users/{user_id}", "GET") in methods
    assert ("/api/recharge", "POST") in methods


def test_parse_parameters():
    result = OpenApiParser(OPENAPI_YAML).parse()
    get_user = [e for e in result["endpoints"] if e["path"] == "/api/users/{user_id}"][0]
    assert get_user["parameters"][0]["name"] == "user_id"
    assert get_user["parameters"][0]["in"] == "path"
    assert get_user["parameters"][0]["required"] is True
    assert "integer" in get_user["parameters"][0]["type"]


def test_parse_request_body_enum():
    result = OpenApiParser(OPENAPI_YAML).parse()
    recharge = [e for e in result["endpoints"] if e["path"] == "/api/recharge"][0]
    body = recharge["request_body"]
    assert body is not None
    assert body["required"] is True
    assert "channel" in body["type"]  # 含 enum


def test_parse_errors():
    with pytest.raises(ValueError):
        OpenApiParser("not a yaml: [").parse()
    with pytest.raises(ValueError):
        OpenApiParser("a: 1").parse()  # 无 openapi/paths


def test_parse_json_content():
    import json
    doc = {
        "openapi": "3.0.3",
        "info": {"title": "JSON接口", "version": "1.0"},
        "paths": {"/ping": {"get": {"responses": {"200": {"description": "ok"}}}}},
    }
    result = OpenApiParser(json.dumps(doc)).parse()
    assert len(result["endpoints"]) == 1
    assert result["endpoints"][0]["path"] == "/ping"
