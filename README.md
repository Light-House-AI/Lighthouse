# Purpose

- The wrapper repo will be used to
  1. Download the model from the azure storage container named models
  2. expose the ML model to interact with it.
  - There is a predict router that retrieves the classification of the model.
- All the parameters will be passed from the .env file
  - azure_storage_connection, model parameters and model_features_list
