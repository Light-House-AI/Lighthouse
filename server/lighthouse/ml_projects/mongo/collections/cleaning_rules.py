"""ML-Projects Data Schema MongoDB collection."""

from lighthouse.config import config

from mongoengine import (
    Document,
    EmbeddedDocumentField,
    DynamicEmbeddedDocument,
    IntField,
)


class CleaningRules(DynamicEmbeddedDocument):
    """
    Class to store the cleaning rules.
    """
    ...


class DatasetCleaningRules(Document):
    """
    Class to store the Dataset Cleaning Rules.
    """

    dataset_id = IntField(required=True)
    rules = EmbeddedDocumentField(CleaningRules)

    meta = {
        # create index on project_id
        "indexes": ["dataset_id"],

        # choose db connection alias
        "db_alias": config.ML_PROJECTS_MONGO_ALIAS
    }
