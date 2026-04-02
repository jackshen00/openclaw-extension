# 运行与联调

## 环境概览

- Python: 3.10+
- Backend: FastAPI
- 数据库: SQLite
- Worker: Chrome Extension Manifest V3

当前目标链路是：

- `OpenClaw` 触发任务并打开本地 Chrome 到目标主页
- 插件在页面已打开的前提下被动采集
- 后端接收并处理采集结果

## 启动后端

```bash
cd backend
uv venv
uv pip install -r requirements.txt
source .venv/bin/activate
uvicorn app.main:app --reload
```

默认服务地址：

- `http://localhost:8000`
- `http://localhost:8000/docs`

## 加载 Worker

1. 打开 Chrome 并访问 `chrome://extensions/`
2. 打开“开发者模式”
3. 选择“加载已解压的扩展程序”
4. 选择仓库中的 `worker/` 目录

## 当前原型联调流程

1. 启动后端
2. 加载 Worker
3. 调用 `POST /tasks/create`
4. 观察 Worker 是否轮询到任务并打开页面
5. 用 `GET /tasks` 检查任务状态与结果

## 目标联调流程

1. 启动后端
2. 加载 Worker
3. 由 `OpenClaw` 创建任务
4. 由 `OpenClaw` 打开本地 Chrome 到目标主页
5. 插件在页面中被动采集并上报状态
6. 后端处理结果
7. `OpenClaw` 查询进度并汇报
