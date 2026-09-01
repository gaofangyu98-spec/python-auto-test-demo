# -*- coding: utf-8 -*-
"""自动生成：PUT /api/users/{user_id} - 更新用户信息"""
import pytest
import requests

BASE_URL = "http://localhost:9000"

class TestPutApiUsersuserid:
    """更新用户信息"""

    def test_正向_正常请求(self):
        resp = requests.put(f"http://localhost:9000/api/users/1", json={"nickname": "test_user", "email": "test@example.com", "age": 1})
        assert resp.status_code == 200
        assert 'code' in resp.json()

    def test_边界_边界值(self):
        resp = requests.put(f"http://localhost:9000/api/users/1", json={"nickname": "AAAAAAAAAAAAAAAAAAAA", "email": "a@b.c", "age": 0})
        assert resp.status_code < 500  # 边界值允许被业务层拒绝(4xx)

    def test_异常_缺少必填字段(self):
        resp = requests.put(f"http://localhost:9000/api/users/1", json={"email": "test@example.com", "age": 1})
        assert resp.status_code in (400, 422)

    def test_安全_SQL注入(self):
        resp = requests.put(f"http://localhost:9000/api/users/1", json={"nickname": "' OR '1'='1", "email": "test@example.com", "age": 1})
        assert resp.status_code in (400, 422, 500)  # 注入应被拒绝

    def test_安全_越权访问(self):
        resp = requests.put(f"http://localhost:9000/api/users/999999", json={"nickname": "test_user", "email": "test@example.com", "age": 1})
        assert resp.status_code in (403, 404)  # 越权/资源不存在应被拒绝
