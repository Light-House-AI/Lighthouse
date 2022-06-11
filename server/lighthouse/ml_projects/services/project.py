"""Projects service."""

from sqlalchemy.orm import Session

from lighthouse.ml_projects.db import Project
from lighthouse.ml_projects.schemas.project import ProjectCreate


def get_user_projects(user_id: int,
                      db: Session,
                      skip: int = 0,
                      limit: int = 100):
    """
    Returns current user projects.
    """
    return db.query(Project).filter(
        Project.user_id == user_id).offset(skip).limit(limit).all()


def create_project(user_id: int, project_data: ProjectCreate, db: Session):
    """
    Creates a new project.
    """
    project = Project(**project_data.dict(), user_id=user_id)
    db.add(project)
    db.commit()
    db.refresh(project)
    return project
