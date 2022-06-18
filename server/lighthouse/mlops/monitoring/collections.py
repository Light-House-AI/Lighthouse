from datetime import datetime
from lighthouse.config import config

from mongoengine import (
    Document,
    DynamicEmbeddedDocument,
    EmbeddedDocumentField,
    DateTimeField,
    StringField,
    IntField,
)


class InputData(DynamicEmbeddedDocument):
    """
    Class to store the input metadata.
    """
    ...


class DeploymentInput(Document):
    """
    Class to store the input parameters for a deployment.
    """
    deployment_id = IntField(required=True)
    project_id = IntField(required=True)

    created_at = DateTimeField(required=True, default=datetime.utcnow)
    primary_model_prediction = StringField(required=True)
    secondary_model_prediction = StringField()
    label = StringField()

    input_data = EmbeddedDocumentField(InputData)

    meta = {
        # create index on deployment_id, project_id
        'indexes': ['deployment_id', 'project_id'],

        # choose db connection alias
        'db_alias': config.MONITORING_MONGO_ALIAS
    }


class ExpectationsSuite(DynamicEmbeddedDocument):
    """
    Class to store the expectations suite for a dataset.
    """
    ...


class DatasetExpectationsSuite(Document):
    """
    Class to store the expectations suite for a dataset.
    """
    dataset_id = IntField(required=True)
    expectations_suite = EmbeddedDocumentField(ExpectationsSuite)

    meta = {
        # create index on dataset_id
        'indexes': ['dataset_id'],

        # choose db connection alias
        'db_alias': config.MONITORING_MONGO_ALIAS
    }