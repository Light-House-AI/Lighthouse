from datetime import datetime
from lighthouse.config import config

from mongoengine import (
    DynamicDocument,
    EmbeddedDocument,
    EmbeddedDocumentField,
    DateTimeField,
    StringField,
)


class InputMetadata(EmbeddedDocument):
    """
    Class to store the input metadata.
    """
    deployment_id = StringField(required=True)
    created_at = DateTimeField(required=True, default=datetime.utcnow)
    primary_model_prediction = StringField(required=True)
    secondary_model_prediction = StringField()


class DeploymentInput(DynamicDocument):
    """
    Class to store the input parameters for a deployment.
    """
    _metadata = EmbeddedDocumentField(InputMetadata)

    meta = {
        # create index on deployment_id
        'indexes': ['_metadata.deployment_id'],

        # choose db connection alias
        'db_alias': config.MONITORING_MONGO_ALIAS
    }
