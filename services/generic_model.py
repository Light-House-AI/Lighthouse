from pydantic import BaseModel, conlist

from services.model_helpers import get_environment_variables

environment_variables_dict = get_environment_variables()


class GenericModel(BaseModel):
    model_id: str
    features_list: conlist(
        float, min_items=environment_variables_dict['number_of_model_features'], max_items=environment_variables_dict['number_of_model_features'])
