# -*- coding: utf-8 -*-
"""自动生成：GET /api/items - 道具列表（分页，需登录）"""
import pytest
import requests

BASE_URL = "http://localhost:9000"
TOKEN = "test-token"  # 鉴权 token（按被测系统配置）

class TestGetApiItems:
    """道具列表（分页，需登录）"""

    def test_正向_正常请求(self):
        resp = requests.get(f"http://localhost:9000/api/items?page=1&size=1", json={}, headers={"Authorization": "Bearer " + TOKEN})
        assert resp.status_code == 200
        assert 'code' in resp.json()

    def test_边界_边界值(self):
        resp = requests.get(f"http://localhost:9000/api/items?page=0&size=0", json={}, headers={"Authorization": "Bearer " + TOKEN})
        assert resp.status_code < 500  # 边界值允许被业务层拒绝(4xx)

    def test_安全_SQL注入(self):
        resp = requests.get(f"http://localhost:9000/api/items?page=' OR '1'='1&size=1", headers={"Authorization": "Bearer " + TOKEN})
        assert resp.status_code in (400, 422, 500)  # 注入应被拒绝
