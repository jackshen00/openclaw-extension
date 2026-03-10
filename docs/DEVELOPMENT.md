# OpenClaw Extension - 开发指南

## 1. 项目愿景 (Project Vision)
构建一个在本地环境运行的、AI 驱动的社媒（小红书）情报系统。利用本地已登录的浏览器环境，通过 Chrome 插件作为执行单元（Worker），实现低成本、高效率的数据自动化采集与 AI 分析。

## 2. 核心架构 (Core Architecture)
项目采用 **三层闭环架构**：
1.  **OpenClaw (大脑)**: 运行在本地/Slack，负责意图解析、任务分发指令、数据最终汇总分析。
2.  **Backend (中枢)**: FastAPI 实现。管理任务队列、存储爬取结果、连接 OpenClaw 与 Worker。
3.  **Worker (手脚)**: Chrome 浏览器插件。负责页面导航、API 拦截解析、结果上报。

## 3. 开发接力原则 (Collaboration Rules for AIs)
*   **Language Priority**: **所有开发文档（DEVELOPMENT.md, PROGRESS.log, README.md 等）必须以中文为主**，除非用户明确要求编写英文。代码注释可保持中英结合。
*   **Context First**: 每次开始任务前，必须阅读 `docs/GEMINI.md` 和 `docs/DEVELOPMENT.md`。
*   **Consistency**: 保持代码风格一致。Backend 使用 Python (FastAPI + PEP 8)，Worker 使用 TypeScript/JavaScript (Chrome Ext MV3)。
*   **Review Requirement**: 在修改代码前，必须 review 已有的接口定义（API Contract），确保不破坏存量功能。
*   **State Update**: 完成一个 Sub-task 后，必须在 `docs/PROGRESS.log` 中追加记录，并在结束时更新 `README.md` 的当日总结。

## 4. 技术栈协议 (Tech Stack)
*   **Backend**: Python 3.10+, FastAPI, SQLite (初期为了快速落地，使用 SQLite/JSON 存储), Uvicorn.
*   **Worker**: Chrome Extension Manifest V3, Content Scripts, Background Service Worker.
*   **Communication**: REST API (初期使用 HTTP Polling)。

## 5. 核心 API 合约 (API Contracts - Draft)
*   `GET /tasks/poll`: Worker 获取待执行任务。
*   `POST /tasks/result`: Worker 上报采集结果。
*   `POST /tasks/status`: Worker 更新执行进度（如：正在打开页面...）。
*   `GET /admin/summary`: OpenClaw 获取汇总报告。

## 6. 开发进度看板 (Development Progress)

### Phase 1: 基础设施搭建 (已完成)
- [x] **[Task 1.1]** 初始化 FastAPI 后端脚手架 (路由、模型、基础存储逻辑)。
- [x] **[Task 1.2]** 初始化 Chrome 插件基础框架 (manifest.json, background.js)。
- [x] **[Task 1.3]** 实现 Worker 注册与心跳机制。

### Phase 2: 采集闭环 (进行中)
- [ ] **[Task 2.1]** XHS 用户主页解析逻辑 (Adapter 模式)。
- [ ] **[Task 2.2]** 任务分发逻辑 (OpenClaw -> Backend -> Worker)。
- [ ] **[Task 2.3]** 存储与去重逻辑。

### Phase 3: AI 集成与提醒 (计划中)
- [ ] **[Task 3.1]** 接入 OpenClaw 分析接口。
- [ ] **[Task 3.2]** 关键词/热度提醒规则引擎。

---

## 7. 如何运行与测试 (How to Run & Test)

### Step 1: 启动后端 (Backend)
1. 确保安装了 `uv`: `curl -LsSf https://astral.sh/uv/install.sh | sh`
2. 进入 `backend` 目录并安装环境：`uv venv && uv pip install -r requirements.txt`
3. 激活虚拟环境并启动服务：
   ```bash
   source .venv/bin/activate
   uvicorn app.main:app --reload
   ```
4. 后端接口文档可见：`http://localhost:8000/docs`

### Step 2: 加载 Chrome 插件 (Worker)
1. 打开 Chrome 浏览器，访问 `chrome://extensions/`。
2. 开启右上角的 "开发者模式"。
3. 点击 "加载已解压的扩展程序"，选择项目根目录下的 `worker` 文件夹。
4. 插件加载后，会自动开始每 10 秒向后端轮询一次任务。

### Step 3: 测试完整流程 (Full Flow Test)
1. **创建模拟任务**: 通过接口文档或 `curl` 在后端创建一个任务。
2. **观察插件行为**: 插件会在 10 秒内发现任务，并自动打开新标签页。
3. **查看结果**: 约 5 秒后，查看 `http://localhost:8000/tasks` 确认任务状态为 `success`。

## 8. 给下一位 AI 的指令
Phase 1 已完成。请开始 **Phase 2: 采集闭环**。
1. **[Task 2.1]**: 在 `worker/content.js` 中实现真实的 XHS 页面解析逻辑。
2. **[Task 2.2]**: 优化任务分发逻辑，支持更复杂的任务参数。
