# app/models.py
from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime

from .database import Base


class Project(Base):
    __tablename__ = "projects"

    id = Column(Integer, primary_key=True, index=True)
    project_name = Column(String, index=True)
    location = Column(String)
    status = Column(String, default="processing")  # processing, in_progress, completed
    created_at = Column(DateTime, default=datetime.utcnow)

    # Relationship with tasks
    tasks = relationship("Task", back_populates="project")


class Task(Base):
    __tablename__ = "tasks"

    id = Column(Integer, primary_key=True, index=True)
    project_id = Column(Integer, ForeignKey("projects.id"))
    name = Column(String)
    status = Column(String, default="pending")  # pending, in_progress, completed

    # Relationship with project
    project = relationship("Project", back_populates="tasks")