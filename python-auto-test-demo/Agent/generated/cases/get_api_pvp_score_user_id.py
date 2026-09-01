# -*- coding: utf-8 -*-
"""自动生成：GET /api/pvp/score/{user_id} - 查询PVP积分"""
import pytest
import requests

BASE_URL = "http://localhost:9000"

class TestGetApiPvpScoreuserid:
    """查询PVP积分"""

    def test_正向_正常请求(self):
        resp = requests.get(f"http://localhost:9000/api/pvp/score/1", json={})
        assert resp.status_code == 200
        assert 'code' in resp.json()

    def test_边界_边界值(self):
        resp = requests.get(f"http://localhost:9000/api/pvp/score/1", json={})
        assert resp.status_code < 500  # 边界值允许被业务层拒绝(4xx)

    def test_安全_SQL注入(self):
        resp = requests.get(f"http://localhost:9000/api/pvp/score/' OR '1'='1", json={})
        assert resp.status_code in (400, 422, 500)  # 注入应被拒绝

    def test_安全_越权访问(self):
        resp = requests.get(f"http://localhost:9000/api/pvp/score/999999", json={})
        assert resp.status_code in (403, 404)  # 越权/资源不存在应被拒绝
