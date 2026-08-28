import os
import time
from loguru import logger

# 自动创建根目录下的 logs 文件夹
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
LOG_DIR = os.path.join(BASE_DIR, "logs")
os.makedirs(LOG_DIR, exist_ok=True)

# 动态按天生成日志文件
log_file_path = os.path.join(LOG_DIR, f"test_{time.strftime('%Y_%m_%d')}.log")

# 配置日志级别与格式
logger.add(log_file_path, rotation="10 MB", retention="7 days", level="INFO", encoding="utf-8")

__all__ = ["logger"]