# Project Rules

## 阅读顺序

1. `README.md`
2. `docs/01_active_workspace.md`
3. `docs/00_project_rules.md`
4. `docs/architecture.md`
5. 按需阅读 `docs/reference/`
6. 仅在追溯历史时阅读 `docs/archive/`

## 文档分层规则

- `docs/01_active_workspace.md` 是唯一热文档，只放当前状态、接力点、进行中事项、下一步、阻塞、Bug、想法。
- `docs/architecture.md` 只写稳定架构事实，不写当天进度。
- `docs/reference/` 只放稳定专题资料，例如 API 合约、运行方式、迁移说明、设计决策。
- `docs/archive/` 只放历史记录、完成事项、旧方案，默认不读。
- 不要新增零散的 `TODO.md`、`notes.md`、`bug_xxx.md`、session summary 等临时文档。

## 文档维护规则

- 新出现的短期信息优先写入 `docs/01_active_workspace.md`。
- 当信息从短期状态变成稳定事实时，下沉到 `docs/architecture.md` 或 `docs/reference/`。
- 当信息完成、过期或仅用于追溯时，移入 `docs/archive/`。
- 会话结束前必须更新 `docs/01_active_workspace.md`。

## 工程协作规则

- 文档以中文为主，除非用户明确要求英文。
- 修改代码前先核对当前实现，不要只根据文档下结论。
- 不要把远期规划写成当前已实现状态。
- 后续开发以 `OpenClaw 主控、插件被动采集、后端处理、Dashboard 展示` 为默认目标模型。
- 当当前代码与目标模型冲突时，文档中要明确标记“当前实现偏差”，不要默认沿偏差继续扩展。
- 后端当前现实实现是 `FastAPI + SQLAlchemy + SQLite`。
- Worker 当前现实实现是 `Chrome Extension Manifest V3`。
- 当前默认本地联调地址是 `http://localhost:8000`。

## 启动与调试

启动后端：

```bash
cd backend
uv venv
uv pip install -r requirements.txt
source .venv/bin/activate
uvicorn app.main:app --reload
```

加载 Worker：

1. 打开 `chrome://extensions/`
2. 开启开发者模式
3. 选择“加载已解压的扩展程序”
4. 选择 `worker/` 目录
