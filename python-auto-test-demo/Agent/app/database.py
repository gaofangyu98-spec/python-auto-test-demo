# -*- coding: utf-8 -*-
"""
数据库会话管理：SQLAlchemy 2.x + SQLite
统一管理引擎、会话工厂，供所有业务模块复用。
"""
from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker

from app.config import settings

engine = create_engine(
    settings.DATABASE_URL,
    connect_args={"check_same_thread": False},  # SQLite + FastAPI 多线程
    echo=False,
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


class Base(DeclarativeBase):
    """所有 ORM 模型的基类"""
    pass


def get_db():
    """FastAPI 依赖注入：请求级数据库会话"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def init_db() -> None:
    """建表（应用启动时调用）"""
    # 延迟导入，避免循环依赖
    import app.models  # noqa: F401
    Base.metadata.create_all(bind=engine)
