# app/schemas.py
from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime

# Task schemas
class TaskBase(BaseModel):
    name: str
    status: str = "pending"

class TaskCreate(TaskBase):
    pass

class Task(TaskBase):
    id: int
    project_id: int

    class Config:
        orm_mode = True

# Project schemas
class ProjectBase(BaseModel):
    project_name: str
    location: str

class ProjectCreate(ProjectBase):
    pass

class Project(ProjectBase):
    id: int
    status: str
    created_at: datetime
    tasks: List[Task] = []

    class Config:
        orm_mode = True
