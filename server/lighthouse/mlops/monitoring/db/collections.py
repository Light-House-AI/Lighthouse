from datetime import datetime

from mongoengine import (Document, 
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
    
    # create index on deployment_id
    meta = {'indexes':['deployment_id']}


class DeploymentInput(Document):
    """
    Class to store the input parameters for a deployment.
    """
    input_params = ListField(required=True)
    _metadata = EmbeddedDocumentField(InputMetadata)
