"""ML-Projects Data Schema MongoDB collection."""

from lighthouse.config import config

from mongoengine import (
    Document,
    ListField,
    StringField,
    IntField,
)


class ProjectDataColumns(Document):
    """
    Class to store the ML Project Data Columns.
    """

    project_id = IntField()
    columns = ListField(StringField())

    meta = {
        # create index on project_id
        "indexes": ["project_id"],

        # choose db connection alias
        "db_alias": config.ML_PROJECTS_MONGO_ALIAS
    }
