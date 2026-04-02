# OpenClaw Extension

本项目文档采用统一文档结构，入口和事实源都在 `docs/` 下。

当前项目目标已经明确为：

- `OpenClaw` 负责控制任务、打开本地 Chrome、查询进度并汇报结果
- Chrome 插件只在目标页面已经打开时被动采集
- 后端负责解析、判重、存储和任务状态
- Dashboard 负责展示监控对象、最新内容和任务运行情况

默认阅读入口：

1. [docs/01_active_workspace.md](docs/01_active_workspace.md)
2. [docs/00_project_rules.md](docs/00_project_rules.md)
3. [docs/architecture.md](docs/architecture.md)
4. `docs/reference/`
5. `docs/archive/`

当前代码目录：

- `backend/`: FastAPI + SQLite 后端
- `worker/`: Chrome Extension Manifest V3 Worker
