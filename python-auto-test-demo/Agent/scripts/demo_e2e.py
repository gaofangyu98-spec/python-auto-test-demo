# -*- coding: utf-8 -*-
"""
端到端验证脚本：解析 mock 服务的 openapi.yaml -> Agent 生成接口用例脚本 -> pytest 执行
用法：先启动 mock 服务（scripts/start_mock.ps1），再运行本脚本
"""
import sys
from pathlib import Path

import requests

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from app.config import settings  # noqa: E402
from app.modules.agent.code_generator import generate_case_script  # noqa: E402
from app.modules.executor.runner import run_pytest  # noqa: E402
from app.modules.openapi.parser import parse_openapi  # noqa: E402


def main() -> None:
    # 1. 读取并解析 OpenAPI 文档
    yaml_path = Path(__file__).resolve().parent.parent / "mock_service" / "openapi.yaml"
    print(f"[1/4] 解析 OpenAPI 文档：{yaml_path}")
    parsed = parse_openapi(yaml_path.read_text(encoding="utf-8"))
    print(f"      接口数：{len(parsed['endpoints'])}，服务：{parsed['servers']}")

    # 2. Agent 生成脚本（use_llm=False 走模板直出，验证流程；接入 Ollama 后可开 True）
    print("[2/4] Agent 生成接口用例脚本 ...")
    generated_paths = []
    for ep in parsed["endpoints"]:
        case = generate_case_script(ep, parsed["servers"], use_llm=False)
        generated_paths.append(case["path"])
        print(f"      ✓ {case['method']} {case['endpoint']}  ->  {case['source']}")

    # 3. 执行生成的脚本（每个文件执行前重置 mock 状态，避免测试数据相互污染）
    print("[3/4] pytest 执行 ...")
    total_passed = total_failed = total = 0
    for p in generated_paths:
        try:
            requests.post(f"{settings.MOCK_BASE_URL}/api/_internal/reset", timeout=5)
        except requests.RequestException:
            print("      ! 警告：mock 服务不可达，请先启动（scripts/start_mock.ps1）")
        result = run_pytest(p)
        total_passed += result.passed
        total_failed += result.failed
        total += result.total
        print(f"      {Path(p).name}: {result.passed} passed / {result.failed} failed")

    # 4. 汇总
    print("[4/4] 汇总")
    print(f"      通过率：{total_passed}/{total} = {total_passed / total * 100:.1f}%" if total else "      （无用例执行）")
    print(f"      报告目录：{settings.REPORT_DIR / 'allure-results'}")


if __name__ == "__main__":
    main()
