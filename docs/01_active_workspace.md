# Active Workspace

> Last updated: 2026-04-02
> Current tool: Codex

## Status
- Current stage: 文档结构与目标架构已对齐，准备进入控制链路改造阶段
- Current focus: 让后续开发统一围绕 `OpenClaw 主控、插件被动采集、后端处理、Dashboard 展示` 展开

## Last position
- File: `docs/architecture.md`
- Function/module: 目标架构与职责边界
- What was done: 已把项目目标、当前实现偏差和后续开发方向写入正式文档，下一步应开始改任务模型和控制链路

## In Progress
- [ ] 把现有代码从“插件主动调度原型”迁回到目标架构
- [ ] 设计 `OpenClaw`、已打开页面和后端任务之间的匹配方式

## Next
- [ ] 把后端任务模型补上 `params`、平台、目标主页等控制所需字段
- [ ] 设计 `OpenClaw` 触发打开本地 Chrome 后，插件如何识别当前页面对应任务
- [ ] 在插件中实现“页面已打开时的被动采集链路”，优先支持 API 拦截，其次页面注水数据，最后 DOM 兜底
- [ ] 为后端补解析、判重、存储和任务进度查询能力
- [ ] 规划 Dashboard 的最小展示面

## Blockers
- 当前代码的控制权放在插件侧，和目标架构相反；继续在此基础上叠功能会放大偏差

## Bugs
- 当前插件会主动轮询任务、主动打开页面，这不符合项目目标
- 当前任务即使没有真实解析，也可能被上报为 `success`

## Ideas
- 采集优先级固定为：API 响应 > 页面注水数据 > DOM 解析 > AI 辅助
- `OpenClaw` 应负责任务生命周期汇报，插件只汇报页面内采集状态

## Find things
- Architecture: `docs/architecture.md`
- Rules: `docs/00_project_rules.md`
- Reference: `docs/reference/`
