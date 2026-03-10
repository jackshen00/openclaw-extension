# GEMINI.md - OpenClaw 扩展项目上下文

此文件为与此工作区交互的 AI 助手提供基础背景信息。

## 项目简介
**OpenClaw 社媒情报系统** 是一个 AI 驱动的社媒监控平台，旨在自动化收集、分析和提醒社媒内容（初期目标平台为小红书 - XHS）。

该系统充当了高层 AI 代理（通过 Slack 运行的 OpenClaw）与底层浏览器自动化（Chrome 插件 Worker）之间的桥梁。

## 系统架构
项目遵循 5 层架构：
1. **代理层 (OpenClaw)**: 接收 Slack 指令，编排任务，并执行最终的数据分析/总结。
2. **后端层 (FastAPI)**: 管理任务、Worker、数据存储以及规则/提醒引擎。
3. **采集层 (浏览器插件)**: Chrome 插件 Worker，处理页面导航、DOM 解析和 API 拦截。
4. **数据层 (MongoDB/Redis)**: 存储任务状态、用户画像、帖子和提醒（目前初期使用 SQLite）。
5. **UI 层 (Next.js Dashboard)**: 用于人工监控和管理任务及 Worker。

## 技术栈 (计划中)
- **后端**: Python (FastAPI), MongoDB (初期 SQLite), Redis, Celery/RQ。
- **采集端**: TypeScript, Chrome Extension API。
- **控制台**: React, Next.js, Tailwind CSS。
- **集成**: Slack (通过 OpenClaw)。

## 当前项目状态
项目目前处于 **设计与架构阶段**。
- **`openclaw_social_intelligence_architecture.md`**: 详细说明系统设计、任务状态、Worker 协议和数据模型的核心规范文档。
- **`main.py`**: 占位脚本（标准的 PyCharm 模板）。

## 构建与运行
由于项目处于早期阶段，目前主要运行后端服务。
- **TODO**: 脚手架搭建 FastAPI 后端（已完成）。
- **TODO**: 初始化 Chrome 插件（TypeScript）（已完成基础框架）。
- **TODO**: 设置 Next.js 控制台。

## 开发规范
- **命名**: 后端遵循 Python (PEP 8)，采集端/UI 遵循 TypeScript/JavaScript 规范。
- **通信**: Worker 通过 REST API 与后端通信（注册、心跳、轮询、结果上报）。
- **架构优先级**: 所有设计决策和协议实现请参考 `openclaw_social_intelligence_architecture.md`。
