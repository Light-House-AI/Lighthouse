from datetime import datetime
from lighthouse.config import config

from mongoengine import (
    Document,
    DynamicEmbeddedDocument,
    EmbeddedDocumentField,
    DateTimeField,
    StringField,
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
    deployment_id = StringField(required=True)
    created_at = DateTimeField(required=True, default=datetime.utcnow)
    primary_model_prediction = StringField(required=True)
    secondary_model_prediction = StringField()

    input_data = EmbeddedDocumentField(InputData)

    meta = {
        # create index on deployment_id
        'indexes': ['deployment_id'],

        # choose db connection alias
        'db_alias': config.MONITORING_MONGO_ALIAS
    }
