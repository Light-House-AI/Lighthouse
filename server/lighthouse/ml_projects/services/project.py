"""Projects service."""

from sqlalchemy.orm import Session

from lighthouse.ml_projects.db import Project
from lighthouse.ml_projects.schemas.project import ProjectCreate
from lighthouse.ml_projects.exceptions import NotFoundException
from lighthouse.ml_projects.mongo import ProjectDataColumns


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


def get_project(user_id: int, project_id: int, db: Session):
    """
    Returns project.
    """
    project = db.query(Project).filter(
        Project.id == project_id,
        Project.user_id == user_id,
    ).first()

    if not project:
        raise NotFoundException("Project not found.")

    return project


def get_project_columns(user_id: int, project_id: int, db: Session):
    """
    Returns project columns.
    """
    project = db.query(Project).filter(
        Project.id == project_id,
        Project.user_id == user_id,
    ).first()

    if not project:
        raise NotFoundException("Project not found.")

    data_columns = ProjectDataColumns.objects(project_id=project_id).first()

    if not data_columns:
        raise NotFoundException(
            "Project columns data not found. Please upload a dataset.")

    return data_columns.columns
