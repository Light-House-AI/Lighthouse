from typing import List
import uvicorn
from fastapi import FastAPI

from services.model_helpers import get_environment_variables
from services.route_helpers import *
from model_creator.network_generator import NetworkGenerator

app = FastAPI()

environment_variables_dict = get_environment_variables()
if environment_variables_dict is None:
    print("Error in generating environment variables dictionary")
    exit(0)


@ app.get("/")
def root():
    return greeting_fn()


@ app.post("/predict")
def predict(models_feature_list: List[List[float]]):
    prediction = predict_for_deployment_type(
        environment_variables_dict, models_feature_list)
    return prediction


if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
