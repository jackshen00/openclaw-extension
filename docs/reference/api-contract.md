# API 合约

本文件描述当前代码已经实现的接口，以及为了对齐目标架构而明确需要补充的方向。

## `GET /`

- 健康检查

## `POST /tasks/create`

请求体：

```json
{
  "task_id": "task-001",
  "type": "PROFILE_SNAPSHOT",
  "platform": "xhs",
  "target_url": "https://www.xiaohongshu.com/user/profile/xxx"
}
```

当前字段：

- `task_id`
- `type`
- `platform`
- `target_url`

计划中的下一步扩展：

- `params`

## `POST /tasks/poll`

这是当前原型代码中的接口，用于插件主动轮询任务。

当前行为：

- 查询第一条 `status=queued` 且 `platform` 匹配的任务
- 找到后将其状态改为 `claimed`
- 没有任务时返回 `null`

说明：

- 该接口符合当前原型，不符合目标架构中的 `OpenClaw 主控、插件被动采集` 模型
- 后续应弱化或移除它在主链路中的地位

## `POST /tasks/{task_id}/status`

当前支持字段：

- `status`
- `worker_id`

## `POST /tasks/{task_id}/result`

当前行为：

- 接口内部会直接把任务状态设为 `success`
- `result` 存入任务记录

## `GET /tasks`

- 返回当前所有任务记录列表

## 目标方向

为了对齐项目目标，后端后续应支持：

- `OpenClaw` 创建监控任务
- `OpenClaw` 查询任务进度与结果
- 插件上报采集进度
- 插件上报原始采集载荷
- 后端返回适合 Dashboard 展示的结果列表
