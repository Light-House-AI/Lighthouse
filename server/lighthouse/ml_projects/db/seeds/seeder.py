from lighthouse.ml_projects.db.models.user import User
from lighthouse.ml_projects.db.models.project import Project
from lighthouse.ml_projects.db.models.model import Model
from lighthouse.ml_projects.db.models.deployment import Deployment, DeploymentType
from lighthouse.ml_projects.db.models.data import Data

from lighthouse.ml_projects.db.database import get_session, get_session_factory, get_engine


def add_users(session):
    users = [{
        "id": "50555621-7791-4ca0-9f95-ff351bcec788",
        "first_name": "John",
        "last_name": "Doe",
        "email": "johndoe@gmail.com",
        "hashed_password": "password"
    }]

    for user in users:
        # session.add(User(**user))
        db_user = User(**user)
        print(db_user)
        session.add(db_user)


def add_projects(session):
    projects = [{
        "name": "Project 1",
        "id": "a6a19a2b-c7bf-4c66-9d87-83d4007f65a3",
        "user_id": "50555621-7791-4ca0-9f95-ff351bcec788",
        "type": "classification"
    }]

    for project in projects:
        session.add(Project(**project))


def add_data(session):
    data = [{
        "name": "Data 1",
        "project_id": "a6a19a2b-c7bf-4c66-9d87-83d4007f65a3",
        "id": "f82cb577-da16-4445-8cdc-9acbea16edb0"
    }, {
        "name": "Data 2",
        "project_id": "a6a19a2b-c7bf-4c66-9d87-83d4007f65a3",
        "id": "25ef5e52-f23b-48a5-8151-5d30ae16d42e"
    }]

    for d in data:
        session.add(Data(**d))


def add_models(session):
    models = [{
        "name": "Model 1",
        "id": "7388516b-3501-4a66-8f79-b872cd926b7c",
        "project_id": "a6a19a2b-c7bf-4c66-9d87-83d4007f65a3",
        "data_id": "f82cb577-da16-4445-8cdc-9acbea16edb0"
    }, {
        "name": "Model 2",
        "id": "1c5e3b26-503f-4f01-b5ce-564515104ded",
        "project_id": "a6a19a2b-c7bf-4c66-9d87-83d4007f65a3",
        "data_id": "25ef5e52-f23b-48a5-8151-5d30ae16d42e"
    }]

    for model in models:
        session.add(Model(**model))


def add_deployments(session):
    deployments = [{
        "name": "Deployment 1",
        "project_id": "a6a19a2b-c7bf-4c66-9d87-83d4007f65a3",
        "id": "a8711a7d-252f-4a96-a387-35380e38bba8",
        "primary_model_id": "7388516b-3501-4a66-8f79-b872cd926b7c"
    }, {
        "name": "Deployment 2",
        "project_id": "a6a19a2b-c7bf-4c66-9d87-83d4007f65a3",
        "id": "ce5ab1f5-cf35-41c2-906f-57e1abcee725",
        "deployment_type": DeploymentType.champion_challenger,
        "primary_model_id": "7388516b-3501-4a66-8f79-b872cd926b7c",
        "secondary_model_id": "1c5e3b26-503f-4f01-b5ce-564515104ded"
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
