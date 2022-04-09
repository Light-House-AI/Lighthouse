import uvicorn
from fastapi import FastAPI, HTTPException

from services.model_helpers import load_pkl_model
from services.generic_model import GenericModel, environment_variables_dict

app = FastAPI()


@ app.get("/")
def root():
    return {"Message":  environment_variables_dict['model_path']}


@ app.post("/predict")
def predict(data: GenericModel):
    if len(data.features_list) != environment_variables_dict['number_of_model_features']:
        raise HTTPException(status_code=400,
                            detail=f"Mismatch between the sent and the required number of model features")

    model_id = data.model_id
    model_features_list = data.features_list
    loaded_model = load_pkl_model(model_id)

    if not loaded_model:
        raise HTTPException(status_code=404,
                            detail=f"Something went wring while loading the model, check the model id")

    # ! REMOVE BRACKETS FROM LIST (ONLY FOR CLASSIFIER MODEL)
    prediction = loaded_model.predict([model_features_list])
    #! FOR CLASSIFIER PREDICTION
    if prediction[0] > 0.5:
        result = "True"
    else:
        result = "False"

    return {"message": f"{prediction[0], result}"}


if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
