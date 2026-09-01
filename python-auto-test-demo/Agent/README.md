# 基于大模型Agent的混合智能自动化测试平台（第一版可运行骨架）

> 毕业设计：基于大模型Agent的混合智能自动化测试平台设计与实现（接口为主，UI为辅）
> 当前版本：第一版可运行代码骨架 —— **OpenAPI 文档解析 + Agent 生成 pytest 接口脚本**

## 一、当前已实现（第一版）

| 模块 | 状态 | 说明 |
|---|---|---|
| 模块1 OpenAPI解析 & Agent用例生成 | ✅ 可运行 | 上传 OpenAPI3.0 yaml/json 自动解析并生成 pytest+requests 脚本；支持自然语言描述 |
| 模块5 接口执行引擎 | ✅ 可运行 | pytest 执行生成的脚本，返回通过/失败统计，支持 Allure 结果输出 |
| 服务层 FastAPI | ✅ 可运行 | 提供 /api/openapi/parse、/api/agent/generate、/api/agent/run |
| 数据层 SQLAlchemy+SQLite | ✅ 可运行 | 用例记录、执行记录落库 |
| 模拟被测业务接口服务 | ✅ 可运行 | 游戏业务（用户/道具/充值/PVP积分），含参数校验/鉴权/错误码 |
| 模块2 接口脚本智能修正 | ⏳ 第二版 | 目录已建，待实现 |
| 模块3 RAG知识库（ChromaDB） | ⏳ 第二版 | 目录已建，待实现 |
| 模块4 AI缺陷分析 | ⏳ 第二版 | 目录已建，待实现 |
| 模块6 AI测试数据生成 | ⏳ 第二版 | 目录已建，待实现 |
| 附属 UI 自动化（Playwright） | ⏳ 靠后 | 演示用，不参与实验 |

## 二、快速启动

```powershell
# 1. 安装依赖
pip install -r requirements.txt

# 2. 启动模拟被测接口服务（新开一个终端）
python -m uvicorn mock_service.main:app --host 0.0.0.0 --port 9000

# 3. 启动平台后端（新开一个终端）
python run.py        # 或 uvicorn app.main:app --port 8000

# 4. 打开 API 文档（Swagger UI）
#    http://localhost:8000/docs
```

## 三、本地大模型（Ollama）

```powershell
ollama serve
ollama pull qwen2.5:7b
```

**降级机制**：Ollama 未启动时，Agent 自动切换为「模板直出」模式（基于参数类型规则化生成 正向/边界/异常/安全 用例），
平台主流程在无 GPU 环境也能完整演示。配置开关：`LLM_MOCK_FALLBACK=true`（config.py）。

## 四、一条命令体验完整流程（验证脚本）

```powershell
# 先启动 mock 服务，再运行（自动解析 mock 的 openapi.yaml -> 生成脚本 -> 执行）
python scripts/demo_e2e.py
```

## 五、项目结构

```
Agent/
├── app/
│   ├── main.py                 # FastAPI 入口
│   ├── config.py               # 配置中心
│   ├── database.py             # SQLAlchemy + SQLite
│   ├── models.py               # ORM 模型
│   ├── api/agent.py            # 核心 Agent API
│   └── modules/
│       ├── openapi/parser.py   # OpenAPI 3.0 解析器
│       ├── agent/              # LLM客户端 + CoT/Few-shot提示词 + 代码生成
│       ├── executor/runner.py  # pytest 执行引擎
│       ├── rag/                # 【第二版】RAG 知识库
│       ├── smart_fix/          # 【第二版】接口脚本智能修正
│       ├── analysis/           # 【第二版】AI 缺陷分析
│       └── data_gen/           # 【第二版】AI 测试数据生成
├── generated/cases/            # 生成的接口用例脚本
├── generated/reports/          # 执行报告
├── mock_service/               # 模拟被测游戏业务接口 + openapi.yaml
├── tests/                      # 单元测试
└── scripts/                    # 启动/演示脚本
```

## 六、开发路线（按优先级）

1. ✅ FastAPI 骨架 + Ollama 接入
2. ✅ OpenAPI 文档解析
3. ✅ Agent 生成 pytest+requests 接口脚本（核心）
4. ⏳ RAG 知识库（ChromaDB）：文档上传、向量检索、知识注入
5. ⏳ 接口脚本智能修正（核心创新点）：捕获报错→Agent分析→自动修复→版本记录
6. ⏳ AI 测试数据生成 + AI 缺陷根因分析
7. ⏳ 接口批量执行 + Allure 报告封装
8. ⏳ 附属 UI 模块（Playwright 基础能力，演示用）
9. ⏳ Vue3 简易前端
10. ⏳ 对比实验数据采集 + 论文整理
