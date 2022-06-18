import numpy as np
import pandas as pd
from .network_generator import NetworkGenerator, to_categorical
from .save_load_model import import_model, export_model
from sklearn.preprocessing import StandardScaler, normalize
from sklearn.datasets import load_wine
from sklearn.model_selection import train_test_split 
from sklearn.metrics import accuracy_score, mean_squared_error, classification_report, roc_auc_score, mean_squared_log_error
import time

data = pd.read_csv('../../datasets/cleaned_datasets/titanic_final.csv')

hyperparameters = {
    # Obligatory
    "type": "Classification", # "Regression"
    "predicted": "Survived", # "Price"
    # Optional
    # Each element in the list is a trial
    "number_of_layers": [5, 6, 7, 8, 9],
    "maximum_neurons_per_layer": [32, 16, 8], # Number of neurons in the middle layer
    "learning_rate": [0.01, 0.1],
    "batch_size": [1, 2, 4, 8], # [1] is for stochastic Gradient Descent else is mini-batch
}
# hyperparameters = {
#     # Obligatory
#     "type": "Classification", # "Regression"
#     "predicted": "Survived", # "Price"
#     # Optional
#     # Each element in the list is a trial
#     "number_of_layers": [7, 8],
#     "maximum_neurons_per_layer": [32, 16, 8], # Number of neurons in the middle layer
#     "learning_rate": [0.01, 0.1],
#     "batch_size": [1, 2], # [1] is for stochastic Gradient Descent else is mini-batch
# }
start = time.time()
network_generator = NetworkGenerator(data, hyperparameters)
network, config = network_generator.get_best_network()
end = time.time()
print("Time to create network(in minutes):", (end - start)/60)

X_train, X_test, y_train, y_test = train_test_split(
    data.loc[:, data.columns != hyperparameters["predicted"]], data[hyperparameters["predicted"]], test_size=0.20)
X_train = np.asarray(X_train)
y_train = np.asarray(y_train)
X_test = np.asarray(X_test)
y_test = np.asarray(y_test)
y_train = to_categorical(y_train)
y_test = to_categorical(y_test)


y_pred = network.predict(X_test)
print(config, accuracy_score(y_test, y_pred.round()))

export_model("titanic_model.pkl", network)

loaded_network = import_model("titanic_model.pkl")
# After you load the model, use it like the line below:
y_pred = loaded_network.predict(X_test)

print(accuracy_score(y_test, y_pred.round()))