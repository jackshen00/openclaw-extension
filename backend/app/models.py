from sqlalchemy import Column, Integer, String, JSON, DateTime
from datetime import datetime
from .database import Base

class Task(Base):
    __tablename__ = "tasks"

    id = Column(Integer, primary_key=True, index=True)
    task_id = Column(String, unique=True, index=True)
    type = Column(String)  # PROFILE_SNAPSHOT, NOTE_DETAIL, etc.
    platform = Column(String) # xhs
    target_url = Column(String)
    status = Column(String, default="queued") # queued, claimed, running, success, failed
    worker_id = Column(String, nullable=True)
    result = Column(JSON, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
