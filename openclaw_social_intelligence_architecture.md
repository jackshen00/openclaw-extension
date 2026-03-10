
# OpenClaw 社媒监控系统架构文档 (Architecture Specification v1)

Author: Jacky  
Purpose: AI-assisted social media monitoring system using OpenClaw

---

# 1 系统目标

构建一个 **AI 驱动的社媒情报系统**

支持：

- 自动监控社媒用户
- 自动解析用户主页
- 自动解析笔记
- 自动分析数据
- 自动发现高价值内容
- 自动提醒

系统核心：

OpenClaw  
↓  
Backend Task System  
↓  
Browser Plugin Worker  
↓  
Data Processing  
↓  
Dashboard + Alerts  

---

# 2 系统总体架构

```
                Slack
                  │
                  │
              OpenClaw
                  │
          ┌───────┴────────┐
          │ Backend API    │
          │ Task Manager   │
          │ Data Store     │
          └───────┬────────┘
                  │
        ┌─────────┴──────────┐
        │                    │
  Browser Plugin Worker   Dashboard
        │                    │
        │                    │
     XHS Platform       Human Control
```

系统分为 **5 层**

1. Agent Layer  
2. Backend Layer  
3. Worker Layer  
4. Data Layer  
5. UI Layer  

---

# 3 模块职责

## 3.1 OpenClaw

负责：

- 接收 Slack 指令
- 调用 backend API
- 查询结果
- 数据分析
- 生成总结
- 发送提醒

OpenClaw **不负责采集**

只负责：

- intent
- task orchestration
- analysis

---

## 3.2 Backend

Backend 是整个系统的核心。

职责：

- 任务管理
- worker 调度
- 数据存储
- 规则引擎
- 提醒系统

核心模块：

- task manager
- worker manager
- data service
- analysis engine
- alert service

---

## 3.3 Browser Plugin Worker

插件负责：

- 页面访问
- API 拦截
- DOM解析
- 数据提取
- 任务上报

插件是：

Browser-based crawler worker

---

## 3.4 Dashboard

Dashboard 提供：

- 监控管理
- 任务状态
- Worker状态
- 数据浏览
- 人工复核

---

# 4 任务系统设计

任务模型：

```
Task
 ├ id
 ├ type
 ├ platform
 ├ target
 ├ status
 ├ worker
 ├ result
 ├ trace
```

---

## 4.1 Task Types

支持任务：

### PROFILE_SNAPSHOT

解析用户主页

返回：

- 用户信息
- 最近笔记

---

### NOTE_DETAIL

解析笔记详情

返回：

- 内容
- 评论
- 互动数据

---

### MONITOR_PROFILE

监控用户

流程：

snapshot  
↓  
compare  
↓  
detect new post  
↓  
deep parse  

---

### DELTA_ANALYSIS

变化检测

用于：

- 新笔记
- 热度变化
- 评论增长

---

# 5 Task State Machine

任务状态：

- queued
- claimed
- opening_page
- waiting_page_ready
- parsing
- uploading
- success
- failed
- retryable_failed
- cancelled

任务生命周期：

queued  
↓  
claimed  
↓  
running  
↓  
success / failed  

---

# 6 Worker Architecture

Worker = 浏览器插件

worker属性：

- workerId
- platform
- version
- machine
- profile
- capabilities

示例：

macmini-xhs-profile20

---

# 7 Worker 注册协议

POST /workers/register

request

```json
{
  "workerId": "macmini-xhs-profile20",
  "platform": "xhs",
  "pluginVersion": "1.3.2",
  "browser": "Chrome",
  "capabilities": [
    "profile_parse",
    "note_parse"
  ]
}
```

response

```json
{
  "status": "ok"
}
```

---

# 8 Worker 心跳

POST /workers/heartbeat

```json
{
  "workerId": "macmini-xhs-profile20",
  "taskId": "task_123",
  "status": "parsing",
  "lastSeenAt": "timestamp"
}
```

---

# 9 Worker 获取任务

POST /tasks/poll

```json
{
  "workerId": "macmini-xhs-profile20",
  "platform": "xhs",
  "capabilities": ["profile_parse", "note_parse"]
}
```

response

```json
{
 "taskId": "task_123",
 "type": "PROFILE_SNAPSHOT",
 "target": {
   "url": "https://xhs.com/user/xxx",
   "userId": "xxx"
 }
}
```

---

# 10 Worker 状态更新

POST /tasks/status

```json
{
  "taskId": "task_123",
  "status": "parsing_profile",
  "progress": 40
}
```

---

# 11 Worker 结果上报

POST /tasks/result

```json
{
 "taskId": "task_123",
 "status": "success",
 "result": {
   "profile": {},
   "notes": []
 },
 "trace": {
   "pageUrl": "",
   "apiCaptured": []
 }
}
```

---

# 12 数据模型

建议 MongoDB

Collections：

- workers
- tasks
- profiles
- posts
- comments
- alerts

---

## profiles

```json
{
 "platform": "",
 "profileId": "",
 "nickname": "",
 "followers": 0,
 "description": "",
 "lastSnapshotAt": ""
}
```

---

## posts

```json
{
 "platform": "",
 "postId": "",
 "authorId": "",
 "title": "",
 "content": "",
 "likeCount": 0,
 "commentCount": 0,
 "publishTime": ""
}
```

---

## comments

```json
{
 "commentId": "",
 "postId": "",
 "content": "",
 "author": "",
 "publishTime": ""
}
```

---

# 13 插件架构

插件目录：

```
plugin/
 ├ runtime/
 ├ parsers/
 ├ adapters/
 ├ transport/
 ├ telemetry/
```

---

## runtime

负责：

- 拉任务
- 执行任务
- 状态上报

---

## adapters

页面适配：

- xhs_profile_adapter
- xhs_note_adapter

---

## parsers

解析数据：

- parseProfile()
- parseNote()
- parseComment()

---

## transport

API通信

- fetchTask()
- updateStatus()
- uploadResult()
- heartbeat()

---

## telemetry

日志系统

---

# 14 OpenClaw 集成

OpenClaw 不直接控制浏览器。

OpenClaw 调用 Backend API。

支持命令：

- monitor user xxx
- parse note xxx
- show recent alerts

---

# 15 Alert Engine

规则引擎检测：

- new post
- high engagement
- keyword match
- comment intent

示例规则：

```
if like_count > 1000
alert
```

---

# 16 Dashboard 页面

页面：

- monitor_targets
- task_center
- worker_status
- content_browser
- alerts

---

# 17 Backend 目录结构

```
backend
 ├ api
 ├ services
 ├ models
 ├ workers
 ├ analysis
 ├ alerts
```

---

# 18 任务执行流程

```
OpenClaw
  ↓
Create Task
  ↓
Task Queue
  ↓
Worker Poll
  ↓
Worker Claim
  ↓
Open Browser
  ↓
Parse Page
  ↓
Upload Result
  ↓
Backend Store
  ↓
Analysis Engine
  ↓
Alert Engine
  ↓
Slack Notification
```

---

# 19 推荐技术栈

Backend

- FastAPI
- MongoDB
- Redis
- Celery / RQ

Worker

- Chrome Extension
- TypeScript

Dashboard

- Next.js
- React
- Tailwind

---

# 20 Phase 实现路线

## Phase 1

基础功能

- worker注册
- 任务分发
- 解析用户
- 存储数据

---

## Phase 2

监控系统

- 定时任务
- 新内容检测
- dashboard

---

## Phase 3

AI分析

- 内容评分
- 价值识别
- 自动总结

---

# 21 安全建议

建议：

- OpenClaw 运行在隔离环境
- API 使用 Token
- Worker sandbox
- 限制 shell 权限

---

# 22 最终系统能力

AI Social Intelligence System

功能：

- 自动监控社媒
- 自动解析内容
- 自动发现高价值内容
- 自动提醒
- AI分析趋势
- Slack实时通知
