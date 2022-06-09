from lighthouse.ml_projects.db import (User, Project, Model, Deployment,
                                       DeploymentType, RawDataset,
                                       CleanedDataset, CleanedDatasetSource)

from lighthouse.ml_projects.db.database import get_session_factory, get_engine


def add_users(session):
    users = [{
        "id": 1,
        "email": "johndoe@gmail.com",
        "first_name": "John",
        "last_name": "Doe",
        "hashed_password": "password"
    }]

    for user in users:
        session.add(User(**user))


def add_projects(session):
    projects = [{
        "id": 1,
        "user_id": 1,
        "name": "Project 1",
        "type": "classification"
    }]

    for project in projects:
        session.add(Project(**project))


def add_raw_datasets(session):
    datasets = [{
        "id": 1,
        "name": "Raw dataset 1",
        "project_id": 1,
        "creation_method": "upload",
    }, {
        "id": 2,
        "name": "Raw dataset 2",
        "project_id": 1,
        "creation_method": "upload",
    }]

    for dataset in datasets:
        session.add(RawDataset(**dataset))


def add_cleaned_datasets(session):
    datasets = [{
        "id": 1,
        "name": "Cleaned dataset 1",
        "project_id": 1
    }, {
        "id": 2,
        "name": "Cleaned dataset 2",
        "project_id": 1
    }]

    for dataset in datasets:
        session.add(CleanedDataset(**dataset))

    sources = [{
        "cleaned_dataset_id": 1,
        "raw_dataset_id": 1
    }, {
        "cleaned_dataset_id": 2,
        "raw_dataset_id": 1
    }, {
        "cleaned_dataset_id": 2,
        "raw_dataset_id": 2
    }]

    for source in sources:
        session.add(CleanedDatasetSource(**source))


def add_models(session):
    models = [{
        "id": "1",
        "project_id": 1,
        "dataset_id": 1,
        "name": "Model 1",
    }, {
        "id": 2,
        "project_id": 1,
        "dataset_id": 2,
        "name": "Model 2",
    }]

    for model in models:
        session.add(Model(**model))


def add_deployments(session):
    deployments = [{
        "id": 1,
        "project_id": 1,
        "primary_model_id": 1,
        "name": "Deployment 1",
    }, {
        "id": 2,
        "project_id": 1,
        "primary_model_id": 1,
        "secondary_model_id": 2,
        "name": "Deployment 2",
        "deployment_type": DeploymentType.champion_challenger,
    }]

    for deployment in deployments:
        session.add(Deployment(**deployment))


def seed(force=False, verbose=True):
    # create a session
    engine = get_engine()
    Session = get_session_factory(engine)
    session = Session()

    # clear all tables if force is True
    if force:
        session.query(Deployment).delete()
        session.query(Model).delete()
        session.query(CleanedDatasetSource).delete()
        session.query(CleanedDataset).delete()
        session.query(RawDataset).delete()
        session.query(Project).delete()
        session.query(User).delete()

    # check if users table is empty
    elif session.query(User).count() > 0:
        if verbose: print("Users table is not empty. Skipping seeding..")
        return False

    # seed tables
    add_users(session)
    add_projects(session)
    add_raw_datasets(session)
    add_cleaned_datasets(session)
    add_models(session)
    add_deployments(session)
    session.commit()
    session.close()

    if verbose: print("Seeding complete.")
    return True
