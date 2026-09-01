# -*- coding: utf-8 -*-
"""
Agent 提示词模板（核心创新点：CoT 思维链 + Few-shot 示例）

设计要点：
1. System Prompt 定义 Agent 角色 = 资深接口测试开发专家；
2. 生成提示词采用 CoT（Chain-of-Thought）：要求模型先输出"测试点规划"，
   再输出"可运行 pytest 代码"，最后自检"预期结果"，降低幻觉；
3. 内置 Few-shot 示例：让模型对齐输出格式（代码块标记、函数命名规范）；
4. 预留 knowledge 注入位：RAG 检索到的历史缺陷 / 业务文档以
   <历史知识> 形式插入，用于缓解大模型幻觉（实验组的关键差异点）。

说明：模板中 {knowledge} / {interface_json} / {description} 为占位符，
用 str.replace 安全替换（避免与示例代码中的 {BASE_URL} 花括号冲突）。
外层定界符使用单引号三连，避免与示例代码中的三引号 docstring 冲突。
"""

# Agent 角色设定
SYSTEM_PROMPT = (
    "你是一名资深的接口自动化测试开发专家，精通 HTTP 协议、RESTful API 设计、"
    "pytest + requests 测试框架。你的任务是根据接口定义生成可直接运行、"
    "覆盖全面的 pytest 接口自动化测试脚本。\n"
    "代码必须满足：\n"
    "1. 使用 pytest + requests，函数命名 test_ 开头，类名 Test 开头；\n"
    "2. 只输出一个被 ```python ``` 包裹的完整代码块，不要输出任何解释文字；\n"
    "3. 测试用例需覆盖：正向功能、边界值、异常参数、安全场景（SQL注入、越权）；\n"
    "4. 每个用例断言明确，用中文 docstring 描述用例意图。"
)

# CoT 生成提示词（实验组使用：CoT + Few-shot + 可选知识注入）
BUILD_CASE_PROMPT = '''请根据下面的接口定义，设计接口自动化测试脚本。

【分析步骤 - 先思考再输出】
1. 先分析接口的 HTTP 方法、请求参数、请求体、响应结构，列出可能的功能场景；
2. 再规划测试用例：正向用例、边界值用例、异常参数用例、安全用例（SQL注入、越权）；
3. 最后把用例翻译成完整的 pytest + requests 代码。

<历史知识>
{knowledge}
</历史知识>

<接口定义>
{interface_json}
</接口定义>

【参考示例（Few-shot）】
```python
# -*- coding: utf-8 -*-
"""自动生成：POST /api/recharge - 游戏充值"""
import pytest
import requests

BASE_URL = "http://localhost:9000"

class TestRecharge:
    def test_正向_正常充值(self):
        resp = requests.post(f"{BASE_URL}/api/recharge",
                             json={"user_id": 1, "amount": 100, "channel": "wechat"})
        assert resp.status_code == 200
        assert resp.json().get("code") == 0

    def test_边界_充值金额为0(self):
        resp = requests.post(f"{BASE_URL}/api/recharge",
                             json={"user_id": 1, "amount": 0, "channel": "wechat"})
        assert resp.status_code == 400  # 金额必须大于0

    def test_安全_越权访问他人账号(self):
        resp = requests.post(f"{BASE_URL}/api/recharge",
                             json={"user_id": 99999, "amount": 100, "channel": "wechat"})
        assert resp.status_code in (403, 404)  # 越权/资源不存在应被拒绝
```
</参考示例>

现在请输出该接口的完整 pytest 测试脚本（只输出代码块）。'''

# 自然语言描述接口 -> 生成脚本（无 OpenAPI 时使用）
NL_BUILD_CASE_PROMPT = '''请根据下面的自然语言接口描述，设计接口自动化测试脚本。

<历史知识>
{knowledge}
</历史知识>

<接口描述>
{description}
</接口描述>

【要求】
1. 推断接口的 URL、HTTP 方法、请求参数与响应结构；
2. 覆盖：正向、边界、异常、安全（注入/越权）场景；
3. 输出完整的 pytest + requests 代码，只输出一个被 ```python ``` 包裹的代码块。

【参考示例（Few-shot）】
用户描述：提供一个查询用户信息的接口 GET /api/users/{user_id}，返回用户昵称和邮箱。
```python
# -*- coding: utf-8 -*-
"""自动生成：GET /api/users/{user_id} - 查询用户信息"""
import pytest
import requests

BASE_URL = "http://localhost:9000"

class TestGetUsersUserId:
    def test_正向_查询已存在用户(self):
        resp = requests.get(f"{BASE_URL}/api/users/1")
        assert resp.status_code == 200

    def test_异常_用户不存在(self):
        resp = requests.get(f"{BASE_URL}/api/users/999999")
        assert resp.status_code == 404

    def test_安全_非法ID注入(self):
        resp = requests.get(f'{BASE_URL}/api/users/1 or 1=1')
        assert resp.status_code == 422  # 非法参数应被拒绝
```
</参考示例>

请输出该接口的完整 pytest 测试脚本（只输出代码块）。'''


def _fill(template: str, **kwargs) -> str:
    """占位符替换（replace 方式，不触碰示例代码中的花括号）"""
    out = template
    for key, value in kwargs.items():
        out = out.replace("{" + key + "}", value)
    return out


def build_case_prompt(interface_json: str, knowledge: str = "") -> str:
    """组装接口用例生成提示词（OpenAPI 输入）"""
    return _fill(
        BUILD_CASE_PROMPT,
        interface_json=interface_json,
        knowledge=knowledge or "（无历史知识）",
    )


def build_nl_prompt(description: str, knowledge: str = "") -> str:
    """组装自然语言接口用例生成提示词"""
    return _fill(
        NL_BUILD_CASE_PROMPT,
        description=description,
        knowledge=knowledge or "（无历史知识）",
    )
