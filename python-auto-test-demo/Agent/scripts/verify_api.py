# -*- coding: utf-8 -*-
"""
平台 API 链路验证脚本：走完整的 HTTP 接口链路
1. POST /api/openapi/parse   解析 OpenAPI 文档
2. POST /api/agent/generate  Agent 生成接口用例脚本
3. POST /api/agent/run       执行第一个生成的脚本

前置：mock 服务(9000) 与平台后端(8000) 均已启动。
运行：python scripts/verify_api.py
"""
import json
import sys
from pathlib import Path

import requests

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

BASE = "http://localhost:8000/api"
YAML_PATH = Path(__file__).resolve().parent.parent / "mock_service" / "openapi.yaml"


def main() -> None:
    openapi_text = YAML_PATH.read_text(encoding="utf-8")

    # 1. 解析
    print("[1/3] POST /api/openapi/parse")
    r = requests.post(f"{BASE}/openapi/parse", json={"content": openapi_text}, timeout=30)
    r.raise_for_status()
    data = r.json()["data"]
    print(f"      接口数：{data['endpoint_count']}，服务：{data['servers']}")
    print(f"      第一个接口：{data['endpoints'][0]['method']} {data['endpoints'][0]['path']}")

    # 2. 生成（use_llm=False 走模板，不依赖 Ollama；接 Ollama 后置 True）
    print("[2/3] POST /api/agent/generate")
    r = requests.post(
        f"{BASE}/agent/generate",
        json={"openapi_content": openapi_text, "use_llm": False},
        timeout=60,
    )
    r.raise_for_status()
    gen = r.json()["data"]
    print(f"      生成脚本数：{gen['count']}")
    for c in gen["cases"][:3]:
        print(f"      ✓ {c['method']} {c['endpoint']}  ({c['source']})")

    # 3. 执行第一个脚本
    first_path = gen["cases"][0]["path"]
    print(f"[3/3] POST /api/agent/run -> {first_path}")
    r = requests.post(f"{BASE}/agent/run", json={"case_path": first_path}, timeout=120)
    r.raise_for_status()
    exec_data = r.json()["data"]
    print(f"      结果：passed={exec_data['passed']} failed={exec_data['failed']} total={exec_data['total']}")

    print("\n✅ API 全链路验证完成")


if __name__ == "__main__":
    main()
