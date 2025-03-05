# app/routes.py
from fastapi import APIRouter, Depends, HTTPException, BackgroundTasks
from sqlalchemy.orm import Session
from typing import List

from . import models, schemas, services
from .database import get_db

router = APIRouter()


@router.post("/projects/", response_model=schemas.Project)
async def create_project(
        project: schemas.ProjectCreate,
        background_tasks: BackgroundTasks,
        db: Session = Depends(get_db)
):
    # Create new project in database
    db_project = models.Project(
        project_name=project.project_name,
        location=project.location
    )
    db.add(db_project)
    db.commit()
    db.refresh(db_project)

    # Generate tasks using Gemini API
    tasks = await services.generate_tasks(project.project_name, project.location)

    # Add tasks to database
    for task in tasks:
        db_task = models.Task(
            name=task["name"],
            status=task["status"],
            project_id=db_project.id
        )
        db.add(db_task)

    db.commit()
    db.refresh(db_project)

    # Start background task to simulate task completion
    background_tasks.add_task(services.simulate_task_completion, db_project.id, db)

    return db_project


@router.get("/projects/{project_id}", response_model=schemas.Project)
def get_project(project_id: int, db: Session = Depends(get_db)):
    db_project = db.query(models.Project).filter(models.Project.id == project_id).first()
    if db_project is None:
        raise HTTPException(status_code=404, detail="Project not found")
    return db_project
