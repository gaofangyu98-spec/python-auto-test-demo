# -*- coding: utf-8 -*-
"""
ORM 数据模型（第一版核心表）
- CaseRecord: 生成的接口用例脚本记录
- ExecRecord: 脚本执行记录
后续版本将扩展：KB文档记录、脚本修正版本记录、缺陷报告等。
"""
from datetime import datetime

from sqlalchemy import JSON, DateTime, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column

from app.database import Base


class CaseRecord(Base):
    """生成的测试用例脚本记录"""
    __tablename__ = "case_records"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    title: Mapped[str] = mapped_column(String(255))            # 脚本标题（接口摘要）
    path: Mapped[str] = mapped_column(String(512))             # 脚本文件路径
    method: Mapped[str] = mapped_column(String(16), default="")  # HTTP 方法
    endpoint: Mapped[str] = mapped_column(String(512), default="")  # 接口路径
    source_type: Mapped[str] = mapped_column(String(32), default="openapi")  # openapi / nl
    content: Mapped[str] = mapped_column(Text, default="")     # 脚本源码
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.now)


class ExecRecord(Base):
    """用例执行记录"""
    __tablename__ = "exec_records"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    case_id: Mapped[int] = mapped_column(Integer, default=0)
    status: Mapped[str] = mapped_column(String(32), default="pending")  # pending/running/passed/failed
    passed: Mapped[int] = mapped_column(Integer, default=0)
    failed: Mapped[int] = mapped_column(Integer, default=0)
    total: Mapped[int] = mapped_column(Integer, default=0)
    output: Mapped[str] = mapped_column(Text, default="")     # 执行日志摘要
    error: Mapped[str] = mapped_column(Text, default="")      # 执行错误信息
    report_path: Mapped[str] = mapped_column(String(512), default="")
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.now)
    extra: Mapped[dict] = mapped_column(JSON, default=dict)   # 预留扩展字段
