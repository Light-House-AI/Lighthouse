import numpy as np
from math import floor, ceil
from sklearn.model_selection import train_test_split 
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import accuracy_score, mean_squared_error, classification_report, roc_auc_score, mean_squared_log_error
from keras.utils import np_utils
from neural_network import NeuralNetwork
from fc_layer import FCLayer
from activation_layer import ActivationLayer
from activation_functions import sigmoid, sigmoid_derivative, identity, identity_derivative, tanh, tanh_derivative, relu, relu_derivative
from loss_functions import mse, mse_derivative
from ray import tune, init, shutdown
from ray.tune.schedulers import AsyncHyperBandScheduler

class NetworkGenerator:
    def __init__(self, data, hyperparameters):
        '''
        hyperparameters = {
            # Obligatory
            "type": "Classification", # "Regression"
            "predicted": "Survived", # "Price"
            # Optional
            # Each element in the list is a trial
            "number_of_layers": [3, 4, 5],
            "maximum_neurons_per_layer": [128, 64, 32, 16, 8], # Number of neurons in the middle layer
            "learning_rate": [0.001, 0.01, 0.1, 0.5, 1],
            "batch_size": [1, 2, 4, 8, 16, 32, 64, 128, 256, 512, 1024], # [1] is for stochastic Gradient Descent else is mini-batch
        }
        '''
        self.data = data
        self.predicted = hyperparameters["predicted"]
        X_train, X_test, y_train, y_test = train_test_split(self.data.loc[:, self.data.columns != self.predicted], self.data[self.predicted], test_size=0.20)
        self.X_train = np.asarray(X_train)
        self.y_train = np.asarray(y_train)
        self.X_test = np.asarray(X_test)
        self.y_test = np.asarray(y_test)
        self.type = hyperparameters["type"]
        self.input_layer_size = self.X_train.shape[1]
        if "number_of_layers" in hyperparameters:
            self.number_of_layers = hyperparameters["number_of_layers"]
        else:
            self.number_of_layers = [4, 5, 6, 7, 8]
        if "maximum_neurons_per_layer" in hyperparameters:
            self.maximum_neurons_per_layer = hyperparameters["maximum_neurons_per_layer"]
        else: 
            self.maximum_neurons_per_layer = [8, 16, 32]
        if "learning_rate" in hyperparameters:
            self.learning_rate = hyperparameters["learning_rate"]
        else:
            self.learning_rate = [0.001, 0.01, 0.1, 1]
        if "batch_size" in hyperparameters:
            self.batch_size = hyperparameters["batch_size"]
        else:
            self.batch_size = [4, 8, 16, 32]
        if(self.type == "Regression"):
            self.output_layer_size = 1
            self.activation_function = relu
            self.activation_function_derivative = relu_derivative
        else: 
            self.y_train = np_utils.to_categorical(self.y_train)
            self.y_test = np_utils.to_categorical(self.y_test)
            self.output_layer_size = self.y_train.shape[1]
            self.activation_function = tanh
            self.activation_function_derivative = tanh_derivative
        
#interpolating the hidden layer sizes
    def __interpolate_hidden_layer_sizes(self, middle_layer_size, number_of_layers):
        hidden_layer_sizes = [0 for x in range(number_of_layers)]
        layers_before_middle = floor(number_of_layers/2) #2
        hidden_layer_sizes[layers_before_middle] = middle_layer_size
        index = layers_before_middle - 1
        for i in range(layers_before_middle, 0, -1):
            hidden_layer_sizes[index] = ceil(2*(self.input_layer_size + hidden_layer_sizes[i])/3)
            index -= 1
        
        index = layers_before_middle + 1
        for i in range(layers_before_middle, number_of_layers - 1, 1):
            hidden_layer_sizes[index] = ceil(2*(hidden_layer_sizes[i] + self.output_layer_size)/3)
            index += 1
        return hidden_layer_sizes

    def __create_network(self, middle_layer_size, number_of_layers, alpha, batch_size):
        network = NeuralNetwork()
        hidden_layer_sizes = self.__interpolate_hidden_layer_sizes(middle_layer_size, number_of_layers)
        hidden_layer_sizes.insert(0, self.input_layer_size)
        hidden_layer_sizes.append(self.output_layer_size)
        for i in range(len(hidden_layer_sizes) - 1):
            network.add(FCLayer(hidden_layer_sizes[i], hidden_layer_sizes[i + 1]))
            if i < len(hidden_layer_sizes) - 1:
                network.add(ActivationLayer(self.activation_function, self.activation_function_derivative))
        if self.type == "Classification":
            network.add(ActivationLayer(sigmoid, sigmoid_derivative))
            network.use(mse, mse_derivative)
        else: 
            network.add(ActivationLayer(identity, identity_derivative))
            network.use(mse, mse_derivative)
        network.fit(self.X_train, self.y_train, epochs=1000, learning_rate=alpha, batch_size=batch_size)
        return network
            
    def __network_generator(self, config, reporter):
        network = self.__create_network(config["middle_layer_size"], config["number_of_layers"], config["alpha"], config["batch_size"])
        y_pred = np.array(network.predict(self.X_test))
        if self.type == "Classification":
            reporter(config, mean_accuracy = accuracy_score(self.y_test, y_pred.round()), network=network)
        else:
            reporter(config, mean_loss = mean_squared_log_error(self.y_test, y_pred), network=network)
        
    def __train_network(self):
        scheduler = AsyncHyperBandScheduler()
        init()
        if self.type == "Classification":
            res = tune.run(
            self.__network_generator,
            name="my_exp",
            metric="mean_accuracy",
            stop={"mean_accuracy": 0.9},
            mode="max",
            scheduler=scheduler,
            config={
                "number_of_layers": tune.grid_search(self.number_of_layers),
                "middle_layer_size": tune.grid_search(self.maximum_neurons_per_layer),
                "alpha": tune.grid_search(self.learning_rate),
                "batch_size": tune.grid_search(self.batch_size),
            }
            )
            results = {k: v for k, v in sorted(res.results.items(), key=lambda item: (item[1]["mean_accuracy"], -item[1]["time_this_iter_s"]), reverse=True)}
                
        else:
            res = tune.run(
            self.__network_generator,
            name="my_exp",
            metric="mean_loss",
            stop={"mean_loss": 0.01},
            mode="min",
            scheduler=scheduler,
            config={
                "number_of_layers": tune.grid_search(self.number_of_layers),
                "middle_layer_size": tune.grid_search(self.maximum_neurons_per_layer),
                "alpha": tune.grid_search(self.learning_rate),
                "batch_size": tune.grid_search(self.batch_size),
            },
            )
            results = {k: v for k, v in sorted(res.results.items(), key=lambda item: (item[1]["mean_loss"], item[1]["time_this_iter_s"]))}
        shutdown()
        return list(results.values())[0]
    
    def get_best_network(self):
        best_result = self.__train_network()
        print(best_result)
        config = best_result["config"]
        network = best_result["network"]
        return network, config