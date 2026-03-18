# OpenClaw Extension - 接力开发 TODO List

> 开发断点提示：**Phase 1 已经完成**，接下来进入 **Phase 2 (采集闭环)**

## 待接力任务清单

### 1. 采集端 (Chrome Extension) - Task 2.1
- [ ] **目标**: 在 `worker/content.js` 中实现真实的 XHS 页面解析逻辑。
    - [ ] 监听 `background.js` 或页内传递的消息，开始解析。
    - [ ] 提取页面核心信息（例如笔记标题、内容、作者等）。
    - [ ] 解析完成后，将真实获取的数据结构通过 `chrome.runtime.sendMessage` 或直接返回给 `background.js` 上报。
- [ ] **配合修改**: 在 `worker/background.js` 中的 `executeTask`，将当前的 `mockResult` 替换为调用 `content.js` 的真实特征提取逻辑。

### 2. 后端 (FastAPI) - Task 2.2
- [ ] **目标**: 优化任务分发逻辑，支持更复杂的任务参数 (`params` 字段)。
    - [ ] **Database**: 修改 `backend/app/models.py` 中的 `Task` 模型，新增 `params = Column(JSON, nullable=True)` 字段。
    - [ ] **Schema**: 修改 `backend/app/schemas.py` 中的 `TaskBase` 类，新增 `params: Optional[Dict[str, Any]] = None`。
    - [ ] **API**: 确保 `/tasks/create` 和 `/tasks/poll` 等接口在请求和响应中正常处理 `params` 数据以适应更加复杂的任务指令。

---
祝下班愉快，回家开发顺利！
