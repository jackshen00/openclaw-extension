from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List, Optional
import uuid

from . import models, schemas, database

# Initialize database
models.Base.metadata.create_all(bind=database.engine)

app = FastAPI(title="OpenClaw Extension Backend")

@app.get("/")
def read_root():
    return {"status": "ok", "message": "OpenClaw Extension Backend is running"}

@app.post("/tasks/create", response_model=schemas.TaskResponse)
def create_task(task: schemas.TaskCreate, db: Session = Depends(database.get_db)):
    db_task = models.Task(**task.dict())
    db.add(db_task)
    db.commit()
    db.refresh(db_task)
    return db_task

@app.post("/tasks/poll", response_model=Optional[schemas.TaskResponse])
def poll_task(poll_req: schemas.WorkerPollRequest, db: Session = Depends(database.get_db)):
    # Find a queued task for the specified platform
    task = db.query(models.Task).filter(
        models.Task.status == "queued",
        models.Task.platform == poll_req.platform
    ).first()

    if task:
        task.status = "claimed"
        task.worker_id = poll_req.worker_id
        db.commit()
        db.refresh(task)
        return task
    return None

@app.post("/tasks/{task_id}/status")
def update_task_status(task_id: str, update: schemas.TaskUpdate, db: Session = Depends(database.get_db)):
    task = db.query(models.Task).filter(models.Task.task_id == task_id).first()
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    
    if update.status:
        task.status = update.status
    if update.worker_id:
        task.worker_id = update.worker_id
    
    db.commit()
    return {"status": "success"}

@app.post("/tasks/{task_id}/result")
def report_task_result(task_id: str, update: schemas.TaskUpdate, db: Session = Depends(database.get_db)):
    task = db.query(models.Task).filter(models.Task.task_id == task_id).first()
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    
    task.status = "success"
    task.result = update.result
    db.commit()
    return {"status": "success"}

@app.get("/tasks", response_model=List[schemas.TaskResponse])
def list_tasks(db: Session = Depends(database.get_db)):
    return db.query(models.Task).all()
