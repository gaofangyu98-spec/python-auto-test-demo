# -*- coding: utf-8 -*-
"""
接口自动化执行引擎（模块5 - 主体）
基于 pytest + requests 执行生成的用例脚本，返回结构化执行结果。

执行结果说明：
- 通过 subprocess 调用 pytest，-q 精简输出；
- 解析 pytest 退出码与输出，汇总 通过/失败/总数；
- 支持 -p no:cacheprovider 避免缓存文件；支持输出 Allure 报告目录（可选）。
"""
from __future__ import annotations

import subprocess
import sys
from pathlib import Path
from typing import Optional

from app.config import settings


class ExecutionResult:
    """执行结果对象"""

    def __init__(
        self,
        passed: int = 0,
        failed: int = 0,
        total: int = 0,
        output: str = "",
        exit_code: int = 0,
        error: str = "",
    ):
        self.passed = passed
        self.failed = failed
        self.total = total
        self.output = output
        self.exit_code = exit_code
        self.error = error

    @property
    def success(self) -> bool:
        return self.failed == 0 and self.error == ""

    def to_dict(self) -> dict:
        return {
            "passed": self.passed,
            "failed": self.failed,
            "total": self.total,
            "success": self.success,
            "exit_code": self.exit_code,
            "output": self.output[-4000:],  # 截断避免过大数据
            "error": self.error,
        }


def run_pytest(
    target: str,
    allure_dir: Optional[str] = None,
    timeout: int = 300,
) -> ExecutionResult:
    """
    执行 pytest 用例。
    :param target: 用例文件路径 或 目录
    :param allure_dir: Allure 结果目录（可选）
    """
    cmd = [
        sys.executable, "-m", "pytest",
        str(target),
        "-q",
        "-p", "no:cacheprovider",
        "--disable-warnings",
    ]
    if allure_dir:
        Path(allure_dir).mkdir(parents=True, exist_ok=True)
        cmd += ["--alluredir", str(allure_dir)]

    try:
        proc = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            timeout=timeout,
        )
    except subprocess.TimeoutExpired:
        return ExecutionResult(error=f"执行超时（>{timeout}s）", output="")
    except Exception as e:  # noqa: BLE001
        return ExecutionResult(error=f"执行异常：{e}", output="")

    output = (proc.stdout or "") + "\n" + (proc.stderr or "")
    result = ExecutionResult(
        exit_code=proc.returncode,
        output=output.strip(),
    )

    # 解析统计
    import re
    m = re.search(r"(\d+) passed", output)
    m_f = re.search(r"(\d+) failed", output)
    m_e = re.search(r"(\d+) error", output)
    result.passed = int(m.group(1)) if m else 0
    result.failed = (int(m_f.group(1)) if m_f else 0) + (int(m_e.group(1)) if m_e else 0)
    result.total = result.passed + result.failed

    return result


def run_case_file(case_path: str, use_allure: bool = True) -> ExecutionResult:
    """执行单个用例文件（便捷入口）"""
    allure_dir = str(settings.REPORT_DIR / "allure-results") if use_allure else None
    return run_pytest(case_path, allure_dir=allure_dir)
