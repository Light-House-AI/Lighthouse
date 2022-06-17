import numpy as np
import pandas as pd
from network_generator import NetworkGenerator
from save_load_model import import_model, export_model
from sklearn.model_selection import train_test_split 
from sklearn.metrics import mean_squared_log_error
import time

data = pd.read_csv('../../../datasets/cleaned_datasets/cars_final.csv')

hyperparameters = {
    # Obligatory
    "type": "Regression", # "Regression"
    "predicted": "price", # "Price"
    # Optional
    # Each element in the list is a trial
    "number_of_layers": [5, 6, 7, 8, 9],
    "maximum_neurons_per_layer": [32, 16, 8], # Number of neurons in the middle layer
    "learning_rate": [0.001, 0.01, 0.1],
    "batch_size": [8, 16, 32], # [1] is for stochastic Gradient Descent else is mini-batch
}

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

y_pred = network.predict(X_test)
print(config, mean_squared_log_error(y_test, y_pred.round()))

export_model("cars_model.pkl", network)

loaded_network = import_model("cars_model.pkl")
# After you load the model, use it like the line below:
y_pred = loaded_network.predict(X_test)

print(mean_squared_log_error(y_test, y_pred.round()))