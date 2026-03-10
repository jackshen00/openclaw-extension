from pydantic import BaseModel
from typing import Optional, Dict, Any, List
from datetime import datetime

class TaskBase(BaseModel):
    task_id: str
    type: str
    platform: str
    target_url: str

class TaskCreate(TaskBase):
    pass

class TaskUpdate(BaseModel):
    status: Optional[str] = None
    worker_id: Optional[str] = None
    result: Optional[Dict[str, Any]] = None

class TaskResponse(TaskBase):
    id: int
    status: str
    worker_id: Optional[str]
    result: Optional[Dict[str, Any]]
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

class WorkerPollRequest(BaseModel):
    worker_id: str
    platform: str
    capabilities: List[str]
