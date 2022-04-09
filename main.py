import uvicorn
from fastapi import FastAPI

from services.model_helpers import get_environment_variables, load_pkl_model
from services.azure_helpers import download_blob

app = FastAPI()
environment_variables_dict = get_environment_variables()
download_blob()


@ app.get("/")
def root():
    return {"Message":  "Welcome to the ML API"}


@ app.get("/predict")
def predict():
    model_features_list = environment_variables_dict['model_features_list']
    loaded_model = load_pkl_model()

    # ! REMOVE BRACKETS FROM LIST (ONLY FOR CLASSIFIER MODEL)
    prediction = loaded_model.predict([model_features_list])
    # #! FOR CLASSIFIER PREDICTION
    if prediction[0] > 0.5:
        result = "True"
    else:
        result = "False"

    return {"message": f"{prediction[0], result}"}


if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
