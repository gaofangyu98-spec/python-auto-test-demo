# -*- coding: utf-8 -*-
"""
模拟被测业务接口服务 —— 论文实验用被测系统
覆盖游戏业务：用户管理、道具查询、充值、PVP积分

设计目的：
1. 为"Agent生成接口用例脚本"提供可执行、有业务规则（参数校验/鉴权/错误码）的被测对象；
2. 接口含 正向/边界/异常/安全 可触发的逻辑，方便对比实验统计
   "脚本可直接运行通过率"、"异常&安全场景缺陷覆盖率"等指标。

启动：uvicorn mock_service.main:app --host 0.0.0.0 --port 9000
"""
from __future__ import annotations

import re
from typing import Optional

from fastapi import FastAPI, Header, HTTPException
from pydantic import BaseModel, Field

app = FastAPI(title="模拟游戏业务接口服务", version="1.0.0")

# ---------- 内存数据存储（演示用，重启即重置） ----------
USERS: dict[int, dict] = {
    1: {"user_id": 1, "nickname": "test_001", "email": "user001@game.com", "age": 22},
    2: {"user_id": 2, "nickname": "test_002", "email": "user002@game.com", "age": 25},
}
ITEMS: list[dict] = [
    {"item_id": 1, "name": "新手礼包", "price": 6},
    {"item_id": 2, "name": "月卡", "price": 30},
    {"item_id": 3, "name": "传说皮肤", "price": 88},
]
RECHARGE_ORDERS: list[dict] = []
PVP_SCORES: dict[int, int] = {1: 1500, 2: 1320}
_NEXT_USER_ID = 100


def _require_auth(authorization: Optional[str]) -> None:
    """简易鉴权：Header 需携带 Authorization: Bearer <token>"""
    if not authorization or not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="未登录或登录已过期")


_SQL_PATTERNS = ["' or", "or '1'='1", "drop table", "union select", "; --", "-- "]


def _validate_sql_injection(value: str, field: str = "参数") -> None:
    """SQL 注入防护（模拟被测系统的基础安全能力）"""
    if isinstance(value, str):
        lower = value.lower()
        if any(p in lower for p in _SQL_PATTERNS):
            raise HTTPException(status_code=400, detail=f"{field}存在非法字符，已拒绝")


# ================= 用户模块 =================
class UserCreate(BaseModel):
    nickname: str = Field(..., min_length=1, max_length=20, description="昵称(1-20)")
    email: str = Field(..., description="邮箱")
    age: int = Field(..., ge=1, le=150, description="年龄(1-150)")


@app.get("/api/users/{user_id}")
def get_user(user_id: int):
    """查询用户信息"""
    if user_id not in USERS:
        raise HTTPException(status_code=404, detail="用户不存在")
    return {"code": 0, "data": USERS[user_id]}


@app.post("/api/users")
def create_user(body: UserCreate):
    """创建用户"""
    if not re.match(r"^[\w.+-]+@[\w-]+\.[\w.]+$", body.email):
        raise HTTPException(status_code=400, detail="邮箱格式不正确")
    _validate_sql_injection(body.nickname, "昵称")
    _validate_sql_injection(body.email, "邮箱")
    global _NEXT_USER_ID
    new_user = {
        "user_id": _NEXT_USER_ID,
        "nickname": body.nickname,
        "email": body.email,
        "age": body.age,
    }
    USERS[_NEXT_USER_ID] = new_user
    _NEXT_USER_ID += 1
    return {"code": 0, "data": new_user}


@app.put("/api/users/{user_id}")
def update_user(user_id: int, body: UserCreate):
    """更新用户信息"""
    if user_id not in USERS:
        raise HTTPException(status_code=404, detail="用户不存在")
    if not re.match(r"^[\w.+-]+@[\w-]+\.[\w.]+$", body.email):
        raise HTTPException(status_code=400, detail="邮箱格式不正确")
    _validate_sql_injection(body.nickname, "昵称")
    _validate_sql_injection(body.email, "邮箱")
    USERS[user_id].update(nickname=body.nickname, email=body.email, age=body.age)
    return {"code": 0, "data": USERS[user_id]}


@app.delete("/api/users/{user_id}")
def delete_user(user_id: int):
    """删除用户"""
    if user_id not in USERS:
        raise HTTPException(status_code=404, detail="用户不存在")
    USERS.pop(user_id)
    return {"code": 0, "message": "删除成功"}


# ================= 道具模块 =================
@app.get("/api/items")
def list_items(page: int = 1, size: int = 10, authorization: Optional[str] = Header(None)):
    """道具列表（分页，需登录）"""
    _require_auth(authorization)
    start = (page - 1) * size
    return {"code": 0, "data": ITEMS[start:start + size], "total": len(ITEMS)}


# ================= 充值模块 =================
class RechargeBody(BaseModel):
    user_id: int = Field(..., description="用户ID")
    amount: float = Field(..., gt=0, description="充值金额(>0)")
    channel: str = Field(..., description="支付渠道")


@app.post("/api/recharge")
def recharge(body: RechargeBody):
    """游戏充值"""
    if body.channel not in ("wechat", "alipay", "bank"):
        raise HTTPException(status_code=400, detail="不支持的支付渠道")
    if body.user_id not in USERS:
        raise HTTPException(status_code=404, detail="用户不存在")
    order = {
        "order_id": len(RECHARGE_ORDERS) + 1,
        "user_id": body.user_id,
        "amount": body.amount,
        "channel": body.channel,
        "status": "paid",
    }
    RECHARGE_ORDERS.append(order)
    return {"code": 0, "data": order}


# ================= PVP 积分模块 =================
class PvpScoreBody(BaseModel):
    score: int = Field(..., ge=0, le=10000, description="PVP积分(0-10000)")


@app.get("/api/pvp/score/{user_id}")
def get_pvp_score(user_id: int):
    """查询PVP积分"""
    if user_id not in PVP_SCORES:
        raise HTTPException(status_code=404, detail="暂无PVP积分记录")
    return {"code": 0, "data": {"user_id": user_id, "score": PVP_SCORES[user_id]}}


@app.post("/api/pvp/score/{user_id}")
def update_pvp_score(user_id: int, body: PvpScoreBody):
    """更新PVP积分"""
    if user_id not in USERS:
        raise HTTPException(status_code=404, detail="用户不存在")
    PVP_SCORES[user_id] = body.score
    return {"code": 0, "data": {"user_id": user_id, "score": body.score}}


@app.post("/api/_internal/reset")
def reset_state():
    """测试辅助：重置内存数据到初始状态（仅平台内部验证使用，非业务接口）"""
    global USERS, ITEMS, RECHARGE_ORDERS, PVP_SCORES, _NEXT_USER_ID
    USERS = {
        1: {"user_id": 1, "nickname": "test_001", "email": "user001@game.com", "age": 22},
        2: {"user_id": 2, "nickname": "test_002", "email": "user002@game.com", "age": 25},
    }
    ITEMS = [
        {"item_id": 1, "name": "新手礼包", "price": 6},
        {"item_id": 2, "name": "月卡", "price": 30},
        {"item_id": 3, "name": "传说皮肤", "price": 88},
    ]
    RECHARGE_ORDERS = []
    PVP_SCORES = {1: 1500, 2: 1320}
    _NEXT_USER_ID = 100
    return {"code": 0, "message": "状态已重置"}


@app.get("/")
def root():
    return {"service": "模拟游戏业务接口服务", "endpoints": [
        "POST /api/users", "GET /api/users/{user_id}", "PUT /api/users/{user_id}", "DELETE /api/users/{user_id}",
        "GET /api/items", "POST /api/recharge", "GET /api/pvp/score/{user_id}", "POST /api/pvp/score/{user_id}",
    ]}
