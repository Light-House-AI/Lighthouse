"""Feature Engineering collection."""

from lighthouse.config import config

from mongoengine import (
    Document,
    DictField,
    ListField,
    IntField,
)


class DatasetFeatureRules(Document):
    """
    Class to store the Dataset Feature Engineering Rules.
    """

    dataset_id = IntField(required=True)
    rules = DictField()

    meta = {
        # create index on project_id
        "indexes": ["dataset_id"],

        # choose db connection alias
        "db_alias": config.ML_PROJECTS_MONGO_ALIAS
    }
