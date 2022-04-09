import os
from os.path import join, dirname
from dotenv import load_dotenv
import pickle


def get_environment_variables():
    folder_path = dirname(dirname(__file__))
    dotenv_path = join(folder_path, '.env')
    load_dotenv(dotenv_path)

    model_id = os.getenv('MODEL_ID')
    model_version = os.getenv('MODEL_VERSION')
    number_of_model_features = os.getenv('NUMBER_OF_MODEL_FEATURES')

    environment_variables_dict = {}
    environment_variables_dict['model_id'] = model_id
    environment_variables_dict['model_version'] = float(
        model_version)
    environment_variables_dict['number_of_model_features'] = int(
        number_of_model_features)

    return environment_variables_dict


def load_pkl_model(model_id):
    try:
        models_folder_path = dirname(dirname(__file__)) + "/models/"
        model_path = models_folder_path + model_id + ".pkl"
        pickle_in = open(model_path, 'rb')
        model = pickle.load(pickle_in)
        return model
    except Exception as ex:
        print(ex)
        return None

# if __name__ == "__main__":
#     print(get_environment_variables())
#     print(load_pkl_model("model_id"))
