from lighthouse.ml_projects.db.models.user import User
from lighthouse.ml_projects.db.models.project import Project
from lighthouse.ml_projects.db.models.model import Model
from lighthouse.ml_projects.db.models.deployment import Deployment, DeploymentType
from lighthouse.ml_projects.db.models.data import Data

from lighthouse.ml_projects.db.database import get_session, get_session_factory, get_engine


def add_users(session):
    users = [{
        "id": 1,
        "first_name": "John",
        "last_name": "Doe",
        "email": "johndoe@gmail.com",
        "hashed_password": "password"
    }]

    for user in users:
        session.add(User(**user))


def add_projects(session):
    projects = [{"id": 1, "name": "Project 1", "user_id": 1}]

    for project in projects:
        session.add(Project(**project))


def add_data(session):
    data = [{"project_id": 1, "version": 1}, {"project_id": 1, "version": 2}]

    for d in data:
        session.add(Data(**d))


def add_models(session):
    models = [{
        "version": 1,
        "project_id": 1,
        "data_version": 1
    }, {
        "version": 2,
        "project_id": 1,
        "data_version": 2
    }]

    for model in models:
        session.add(Model(**model))


def add_deployments(session):
    deployments = [{
        "project_id": 1,
        "id": 1,
        "primary_model_version": 1
    }, {
        "project_id": 1,
        "id": 2,
        "deployment_type": DeploymentType.champion_challenger,
        "primary_model_version": 1,
        "secondary_model_version": 2
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
        session.query(Data).delete()
        session.query(Project).delete()
        session.query(User).delete()

    # check if users table is empty
    elif session.query(User).count() > 0:
        if verbose: print("Users table is not empty. Skipping seeding..")
        return False

    # seed tables
    add_users(session)
    add_projects(session)
    add_data(session)
    add_models(session)
    add_deployments(session)
    session.commit()
    session.close()

    if verbose: print("Seeding complete.")
    return True
