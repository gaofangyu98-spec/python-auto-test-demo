# -*- coding: utf-8 -*-
"""自动生成：POST /api/recharge - 游戏充值"""
import pytest
import requests

BASE_URL = "http://localhost:9000"

class TestPostApiRecharge:
    """游戏充值"""

    def test_正向_正常请求(self):
        resp = requests.post(f"http://localhost:9000/api/recharge", json={"user_id": 1, "amount": 1, "channel": "wechat"})
        assert resp.status_code == 200
        assert 'code' in resp.json()

    def test_边界_边界值(self):
        resp = requests.post(f"http://localhost:9000/api/recharge", json={"user_id": 0, "amount": 0, "channel": "bank"})
        assert resp.status_code < 500  # 边界值允许被业务层拒绝(4xx)

    def test_异常_缺少必填字段(self):
        resp = requests.post(f"http://localhost:9000/api/recharge", json={"amount": 1, "channel": "wechat"})
        assert resp.status_code in (400, 422)

    def test_安全_SQL注入(self):
        resp = requests.post(f"http://localhost:9000/api/recharge", json={"user_id": "' OR '1'='1", "amount": 1, "channel": "wechat"})
        assert resp.status_code in (400, 422, 500)  # 注入应被拒绝

    def test_安全_越权访问(self):
        resp = requests.post(f"http://localhost:9000/api/recharge", json={"user_id": 999999, "amount": 1, "channel": "wechat"})
        assert resp.status_code in (403, 404)  # 越权/资源不存在应被拒绝
