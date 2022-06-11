"""ML-Projects Data Schema MongoDB collection."""

from lighthouse.config import config

from mongoengine import (
    Document,
    EmbeddedDocumentField,
    DynamicEmbeddedDocument,
    IntField,
)


class DataSchema(DynamicEmbeddedDocument):
    """
    Class to store the data schema.
    """
    ...


class ProjectDataSchema(Document):
    """
    Class to store the ML Project Data Schema.
    """

    project_id = IntField(required=True)
    schema = EmbeddedDocumentField(DataSchema)

    meta = {
        # create index on project_id
        "indexes": ["project_id"],

        # choose db connection alias
        "db_alias": config.ML_PROJECTS_MONGO_ALIAS
    }
