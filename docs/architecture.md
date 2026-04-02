# Architecture

## 项目定位

OpenClaw Extension 的目标是构建一个基于 `OpenClaw + 本地 Chrome + Chrome 插件 + 后端 + Dashboard` 的社媒用户更新监控系统。

当前业务目标：

- 通过 `OpenClaw` 添加和管理需要监控的用户主页
- 由 `OpenClaw` 控制本地 Chrome 打开指定主页
- 页面打开后由插件被动采集页面数据
- 后端解析、判重、存储结果并维护任务状态
- Dashboard 展示监控对象、最新内容和任务运行情况
- `OpenClaw` 对用户汇报任务进度和最终结果

当前首个目标平台是小红书（`xhs`），后续扩展到抖音等平台。

## 模块划分

### OpenClaw

职责：

- 接收对话或 Slack 指令
- 创建监控任务
- 控制本地 Chrome 打开目标用户主页
- 查询任务进度
- 向用户汇报任务状态与最终结果

说明：

- `OpenClaw` 只做控制，不做页面采集

### Backend

职责：

- 接收任务创建与状态查询
- 接收插件上传的原始数据和采集状态
- 解析为统一结构
- 判定是否为新内容
- 保存结果到数据库
- 为 Dashboard 提供查询接口

入口：

- `backend/app/main.py`

### Worker

职责：

- 检测当前页面是否为目标用户主页
- 在目标页面中拦截接口、提取注水数据或解析 DOM
- 回传采集状态和原始数据

说明：

- 插件是被动采集端，不负责主动调度任务，不负责决定打开哪个页面

入口：

- `worker/background.js`

### Dashboard

职责：

- 展示当前监控用户
- 展示最近发现的新内容
- 展示任务进度和失败记录
- 提供基础运行观察能力

说明：

- 当前仓库尚未实现该模块，但它属于目标系统的一部分

## 依赖方向

```text
Slack / 对话
      |
      v
OpenClaw（控制层）
      |
      v
Backend API / Task Service
      |
      v
本地 Chrome 打开目标主页
      |
      v
Chrome Extension（被动采集）
      |
      v
Backend Processing + Database
      |
      v
Dashboard / OpenClaw 结果查询
```

## 关键数据流

1. 用户通过 `OpenClaw` 添加需要监控的用户主页。
2. `OpenClaw` 调用后端创建任务。
3. `OpenClaw` 控制本地 Chrome 打开目标主页。
4. 插件检测到目标页面后开始被动采集。
5. 插件优先拦截 API 响应，其次读取页面注水数据，最后用 DOM 解析兜底。
6. 插件把采集状态和原始数据发送给后端。
7. 后端解析、判重、入库，并更新任务状态。
8. Dashboard 展示最新状态和结果。
9. `OpenClaw` 查询任务进度并向用户汇报结果。

## 采集策略优先级

采集链路按以下优先级设计：

1. network 响应拦截
2. 页面注水数据 / 全局状态
3. HTML / DOM 解析
4. AI 辅助分析

说明：

- AI 只用于辅助分析异常页面、帮助生成规则，不进入主采集主链路。

## 当前任务模型

当前代码中的任务字段：

- `task_id`
- `type`
- `platform`
- `target_url`
- `status`
- `worker_id`
- `result`
- `created_at`
- `updated_at`

已明确但尚未实现的扩展：

- `params`

目标上还需要承载：

- 监控用户主页标识
- 任务来源（例如 OpenClaw / Slack）
- 进度状态
- 原始采集载荷
- 解析结果摘要

## 非目标

以下内容目前不属于当前仓库已实现范围：

- 在插件中内置任务调度器
- 让插件主动决定页面跳转
- 依赖 AI 作为主采集手段

## 当前实现约束

- 后端使用 SQLite，本地数据库文件位于 `backend/openclaw.db`
- Worker 通过 `fetch` 直接访问后端 HTTP API
- `worker/content.js` 尚未实现，因此真实页面解析尚未落地

## 当前实现偏差

当前代码与目标模型存在以下偏差：

- 插件仍在主动轮询后端任务
- 插件仍在主动打开目标页面
- 采集结果仍然是 mock 数据
- 后端还没有解析、判重、Dashboard 查询等正式处理能力

后续开发应优先消除这些偏差，而不是继续强化“插件主动调度”的实现。
