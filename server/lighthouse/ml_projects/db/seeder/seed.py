from lighthouse.ml_projects.db import (User, Project, Model, Deployment,
                                       DeploymentType, RawDataset,
                                       CleanedDataset, CleanedDatasetSource,
                                       Notification)

from lighthouse.ml_projects.db.database import get_session_factory, get_engine
from lighthouse.ml_projects.services import password


def add_users(session):
    users_data = [{
        "email": "johndoe@gmail.com",
        "first_name": "John",
        "last_name": "Doe",
        "hashed_password": password.get_password_hash("password")
    }]

    users = [User(**user_data) for user_data in users_data]

    for user in users:
        session.add(user)

    return users


def add_notifications(session, user):
    notifications_data = [{
        "user": user,
        "title": "Notification 1",
        "body": "This is a notification"
    }, {
        "user": user,
        "title": "Notification 2",
        "body": "This is another notification"
    }]

    notifications = [
        Notification(**notification_data)
        for notification_data in notifications_data
    ]

    for notification in notifications:
        session.add(notification)

    return notifications


def add_projects(session, user):
    projects_data = [{
        "user": user,
        "name": "Project 1",
        "overview": "This is an overview for project 1",
        "type": "classification",
        "predicted_column": "class",
    }]

    projects = [Project(**project_data) for project_data in projects_data]

    for project in projects:
        session.add(project)

    return projects


def add_raw_datasets(session, project):
    datasets_data = [{
        "name": "Raw dataset 1",
        "project": project,
        "creation_method": "upload",
    }, {
        "name": "Raw dataset 2",
        "project": project,
        "creation_method": "upload",
    }]

    datasets = [RawDataset(**dataset_data) for dataset_data in datasets_data]

    for dataset in datasets:
        session.add(dataset)

    return datasets


def add_cleaned_datasets(session, project, raw_dataset_1, raw_dataset_2):
    datasets_data = [{
        "name": "Cleaned dataset 1",
        "project": project
    }, {
        "name": "Cleaned dataset 2",
        "project": project
    }]

    cleaned_datasets = [
        CleanedDataset(**dataset_data) for dataset_data in datasets_data
    ]

    for dataset in cleaned_datasets:
        session.add(dataset)

    sources = [{
        "cleaned_dataset": cleaned_datasets[0],
        "raw_dataset": raw_dataset_1
    }, {
        "cleaned_dataset": cleaned_datasets[1],
        "raw_dataset": raw_dataset_1
    }, {
        "cleaned_dataset": cleaned_datasets[1],
        "raw_dataset": raw_dataset_2
    }]

    for source in sources:
        session.add(CleanedDatasetSource(**source))

    return cleaned_datasets


def add_models(session, project, cleaned_dataset_1, cleaned_dataset_2):
    models_data = [{
        "project": project,
        "dataset": cleaned_dataset_1,
        "name": "Model 1",
    }, {
        "project": project,
        "dataset": cleaned_dataset_2,
        "name": "Model 2",
    }]

    models = [Model(**model_data) for model_data in models_data]

    for model in models:
        session.add(model)

    return models


def add_deployments(session, project, model_1, model_2):
    deployments_data = [{
        "project": project,
        "primary_model": model_1,
        "name": "Deployment 1",
    }, {
        "project": project,
        "primary_model": model_1,
        "secondary_model": model_2,
        "name": "Deployment 2",
        "type": DeploymentType.champion_challenger,
    }]

    deployments = [
        Deployment(**deployment_data) for deployment_data in deployments_data
    ]

    for deployment in deployments:
        session.add(deployment)

    return deployments


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
        session.query(Notification).delete()
        session.query(User).delete()

    # check if users table is empty
    elif session.query(User).count() > 0:
        if verbose: print("Users table is not empty. Skipping seeding..")
        return False

    # seed tables
    users = add_users(session)
    projects = add_projects(session, users[0])
    raw_datasets = add_raw_datasets(session, projects[0])

    cleaned_dataset = add_cleaned_datasets(session, projects[0],
                                           raw_datasets[0], raw_datasets[1])

    models = add_models(session, projects[0], cleaned_dataset[0],
                        cleaned_dataset[1])

    add_deployments(session, projects[0], models[0], models[1])
    add_notifications(session, users[0])
    session.commit()
    session.close()

    if verbose: print("Seeding complete.")
    return True
