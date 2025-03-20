import numpy as np
import pandas as pd
from sklearn.preprocessing import StandardScaler, normalize
from sklearn.datasets import load_wine
from sklearn.model_selection import train_test_split 
from sklearn.metrics import accuracy_score, mean_squared_error, classification_report, roc_auc_score, mean_squared_log_error

from model_creator.neural_network.network_generator import NetworkGenerator, to_categorical
from model_creator.neural_network.save_load_model import import_model, export_model

df = pd.read_csv('../datasets/supermarket/supermarket_final.csv')

hyperparameters = {
    "type": "Regression", # "Regression"
    "predicted": "Sales", # "Price"
    "number_of_layers": [6, 7, 8, 9],
    "maximum_neurons_per_layer": [32, 16], # Number of neurons in the middle layer
    "learning_rate": [0.001,0.01, 0.1],
    "batch_size": [1, 2, 4, 8, 16, 32],
}
network_generator = NetworkGenerator(df, hyperparameters)
network, config, accuracy = network_generator.get_best_network()

X_train, X_test, y_train, y_test = train_test_split(df.loc[:, df.columns != hyperparameters['predicted']], df[hyperparameters['predicted']], test_size=0.20)

y_pred = network.predict(X_test)
print(config, mean_squared_error(y_test, y_pred), accuracy)
#print(config, accuracy_score(y_test, y_pred), accuracy)