# -*- coding: utf-8 -*-
"""自动生成：POST /api/users - 创建用户"""
import pytest
import requests

BASE_URL = "http://localhost:9000"

class TestPostApiUsers:
    """创建用户"""

    def test_正向_正常请求(self):
        resp = requests.post(f"http://localhost:9000/api/users", json={"nickname": "test_user", "email": "test@example.com", "age": 1})
        assert resp.status_code == 200
        assert 'code' in resp.json()

    def test_边界_边界值(self):
        resp = requests.post(f"http://localhost:9000/api/users", json={"nickname": "AAAAAAAAAAAAAAAAAAAA", "email": "a@b.c", "age": 0})
        assert resp.status_code < 500  # 边界值允许被业务层拒绝(4xx)

    def test_异常_缺少必填字段(self):
        resp = requests.post(f"http://localhost:9000/api/users", json={"email": "test@example.com", "age": 1})
        assert resp.status_code in (400, 422)

    def test_安全_SQL注入(self):
        resp = requests.post(f"http://localhost:9000/api/users", json={"nickname": "' OR '1'='1", "email": "test@example.com", "age": 1})
        assert resp.status_code in (400, 422, 500)  # 注入应被拒绝
