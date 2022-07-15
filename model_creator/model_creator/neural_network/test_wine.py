import numpy as np
import pandas as pd
from sklearn.preprocessing import StandardScaler, normalize
from sklearn.datasets import load_wine
from sklearn.model_selection import train_test_split 
from sklearn.metrics import accuracy_score, mean_squared_error, classification_report, roc_auc_score, mean_squared_log_error

from model_creator.neural_network.network_generator import NetworkGenerator, to_categorical
from model_creator.neural_network.save_load_model import import_model, export_model

'''
For the sake of testing only needed to test the network generator
'''
X, Y = load_wine(return_X_y=True)
print(X.shape, Y.shape)
X_train, X_test, y_train, y_test = train_test_split(X,Y, test_size=0.2)
#Normalizing data
scaler = StandardScaler()
scaler.fit(X_train)
X_train = scaler.transform(X_train)
X_test = scaler.transform(X_test)

y_train = to_categorical(y_train)
y_test = to_categorical(y_test)
print(X_test)
print(X_train.shape, X_test.shape, y_train.shape, y_test.shape)
'''
Till here
'''

data = load_wine(as_frame=True)
print(data["frame"].head())
hyperparameters = {
    # Obligatory
    "type": "Classification", # "Regression"
    "predicted": "target", # "Price"
    # Optional
    # Each element in the list is a trial
    "number_of_layers": [3],
    "maximum_neurons_per_layer": [8], # Number of neurons in the middle layer
    "learning_rate": [0.01, 0.1],
    "batch_size": [4], # [1] is for stochastic Gradient Descent else is mini-batch
} 
network_generator = NetworkGenerator(data["frame"], hyperparameters)
network, config = network_generator.get_best_network()

y_pred = network.predict(X_test)
print(config, accuracy_score(y_test, y_pred.round()))

export_model("wine_model.pkl", network)

loaded_network = import_model("wine_model.pkl")
# After you load the model, use it like the line below:
y_pred = loaded_network.predict(X_test)

print(accuracy_score(y_test, y_pred.round()))