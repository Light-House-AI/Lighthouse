from datetime import datetime

from mongoengine import (DynamicDocument, 
                         EmbeddedDocument, 
                         EmbeddedDocumentField, 
                         DateTimeField,
                         StringField, 
                         ListField)

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

    # create index on deployment_id
    meta = {'indexes':['_metadata.deployment_id']}