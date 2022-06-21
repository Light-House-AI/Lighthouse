"""Projects service."""

from typing import Dict, List
from sqlalchemy.orm import Session, joinedload
from sqlalchemy import func

from lighthouse.ml_projects.db import Project, Deployment, Model, RawDataset, CleanedDataset
from lighthouse.ml_projects.schemas.project import ProjectCreate
from lighthouse.ml_projects.exceptions import NotFoundException
from lighthouse.ml_projects.mongo import ProjectDataColumns

from lighthouse.mlops.monitoring import service as monitoring_service


def get_user_projects(user_id: int,
                      db: Session,
                      skip: int = 0,
                      limit: int = 100):
    """
    Returns current user projects.
    """

    num_deployments = db.query(Deployment.project_id, \
                            func.count(Deployment.id).label('count')). \
                            group_by(Deployment.project_id). \
                            subquery()

    num_models = db.query(Model.project_id, \
                            func.count(Model.id).label('count')). \
                            group_by(Model.project_id). \
                            subquery()

    num_raw_datasets = db.query(RawDataset.project_id, \
                            func.count(RawDataset.id).label('count')). \
                            group_by(RawDataset.project_id). \
                            subquery()

    num_cleaned_datasets = db.query(CleanedDataset.project_id, \
                            func.count(CleanedDataset.id).label('count')). \
                            group_by(CleanedDataset.project_id). \
                            subquery()

    result = db.query(
            Project, num_deployments.c.count, num_models.c.count,
            num_raw_datasets.c.count, num_cleaned_datasets.c.count). \
        filter(Project.user_id == user_id). \
        outerjoin(num_deployments, num_deployments.c.project_id == Project.id). \
        outerjoin(num_models, num_models.c.project_id == Project.id). \
        outerjoin(num_cleaned_datasets, num_cleaned_datasets.c.project_id == Project.id). \
        outerjoin(num_raw_datasets, num_raw_datasets.c.project_id == Project.id). \
        offset(skip). \
        limit(limit). \
        all()

    projects = []
    for project, num_deployments, num_models, num_cleaned_datasets, num_raw_datasets in result:
        project_dict = project.to_dict()

        if not num_deployments:
            project_dict["num_deployments"] = 0
        else:
            project_dict["num_deployments"] = num_deployments

        if not num_models:
            project_dict["num_models"] = 0
        else:
            project_dict["num_models"] = num_models

        if not num_cleaned_datasets:
            project_dict["num_cleaned_datasets"] = 0
        else:
            project_dict["num_cleaned_datasets"] = num_cleaned_datasets

        if not num_raw_datasets:
            project_dict["num_raw_datasets"] = 0
        else:
            project_dict["num_raw_datasets"] = num_raw_datasets

        projects.append(project_dict)

    return projects


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
    project = db.query(Project). \
        outerjoin(Deployment, Deployment.project_id == Project.id). \
        outerjoin(Model, Model.project_id == Project.id). \
        options(joinedload(Project.deployments)). \
        options(joinedload(Project.models)). \
        options(joinedload(Project.raw_datasets)). \
        options(joinedload(Project.cleaned_datasets)). \
        filter(
            Project.id == project_id,
            Project.user_id == user_id,
        ).first()

    if not project:
        raise NotFoundException("Project not found.")

    return project.to_dict()


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


def get_shadow_data(
        user_id: int,
        project_id: int,
        db: Session,
        skip: int = 0,
        limit: int = 100,
):
    """
    Get shadow data for a project.
    """
    project = db.query(Project).filter(Project.user_id == user_id,
                                       Project.id == project_id).first()

    if not project:
        raise NotFoundException("Project not found.")

    return monitoring_service.get_shadow_data(
        project_id,
        project.predicted_column,
        skip,
        limit,
    )


def label_shadow_data(user_id: int, project_id: int,
                      labeled_data: List[Dict[str, str]], db: Session) -> None:
    """
    Label data.
    """
    project = db.query(Project.id).filter(Project.id == project_id,
                                          Project.user_id == user_id).first()

    if not project:
        raise NotFoundException("Project not found.")

    monitoring_service.label_input_data(project_id, labeled_data)

    return {"status": "success"}
