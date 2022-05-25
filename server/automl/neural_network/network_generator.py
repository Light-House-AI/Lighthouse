import numpy as np
from math import floor, ceil
from sklearn.model_selection import train_test_split 
from sklearn.metrics import accuracy_score, mean_squared_error, classification_report, roc_auc_score
from keras.utils import np_utils
from .neural_network import NeuralNetwork
from .fc_layer import FCLayer
from .activation_layer import ActivationLayer
from .activation_functions import sigmoid, sigmoid_derivative, identity, identity_derivative, tanh, tanh_derivative, relu, relu_derivative
from .loss_functions import mse, mse_derivative
from ray import tune
from ray.tune.schedulers import AsyncHyperBandScheduler
import pickle

class NetworkGenerator:
    def __init__(self, X_train, y_train, X_test, y_test, type):
        #TODO: change data input, finalize needed parameters
        self.X_train = X_train
        self.y_train = y_train
        self.X_test = X_test
        self.y_test = y_test
        self.type = type
        self.input_layer_size = X_train.shape[1]
        if(self.type == "Regression"):
            self.output_layer_size = 1
            self.activation_function = relu
            self.activation_function_derivative = relu_derivative
        else: 
            self.output_layer_size = y_train.shape[1]
            self.activation_function = tanh
            self.activation_function_derivative = tanh_derivative
        self.middle_layer_size = ceil((2*(self.input_layer_size + self.output_layer_size))/3)
        
    #interpolating the hidden layer sizes
    def __interpolate_hidden_layer_sizes(self, middle_layer_size, number_of_layers):
        '''
        using the number of layers and the size of input, output and middle layer, the function interpolates the remaining hidden layers
        and returns the list of hidden layer sizes without the input and output layer
        '''
        hidden_layer_sizes = [0 for x in range(number_of_layers)]
        layers_before_middle = floor(number_of_layers/2) #2
        layers_after_middle = ceil(number_of_layers/2) - 1 #2
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

    def __create_network(self, middle_layer_size, number_of_layers, epochs, alpha):
        '''
        creates a network with the given parameters
        '''
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
            network.use(mse, mse_derivative)  #TODO: change loss function
        else: 
            network.add(ActivationLayer(identity, identity_derivative))
            network.use(mse, mse_derivative)
        network.fit(self.X_train, self.y_train, epochs=epochs, learning_rate=alpha)
        return network
            
    def __network_generator(self, config, reporter):
        '''
        This function is used in the ray.tune.run function to generate the network the reporter is used 
        to return anything needed from this trial
        '''
        network = self.__create_network(config["middle_layer_size"], config["number_of_layers"], config["epochs"], config["alpha"])
        y_pred = np.array(network.predict(self.X_test))
        #TODO: accuracy metric 
        if self.type == "Classification":
            reporter(config, mean_accuracy = accuracy_score(self.y_test, y_pred.round()), network=network)
        else:
            reporter(config, mean_loss = mean_squared_error(self.y_test, y_pred))
        
    def __train_network(self):
        '''
        Runs the network generator and returns the best result
        '''
        scheduler = AsyncHyperBandScheduler()
        if self.type == "Classification":
            res = tune.run(
            self.__network_generator,
            name="my_exp",
            metric="mean_accuracy",
            stop={"mean_accuracy": 0.9},
            mode="max",
            scheduler=scheduler,
            config={
                "number_of_layers": tune.grid_search([6, 7, 8, 9]),
                "middle_layer_size": tune.grid_search([8, 16, 32]),#, 64, 128]),
                "epochs": tune.grid_search([500, 1000]),#, 2000, 3000, 4000, 5000]),
                "alpha": tune.grid_search([0.001, 0.01, 0.1]),#, 1]),
            },
            )
            results = {k: v for k, v in sorted(res.results.items(), key=lambda item: (item[1]["mean_accuracy"], -item[1]["time_this_iter_s"]), reverse=True)}
                
        else:
            res = tune.run(
            self.__network_generator,
            name="my_exp",
            metric="mean_loss",
            stop={"mean_loss": 0.2},
            mode="min",
            scheduler=scheduler,
            config={
                "number_of_layers": tune.grid_search([3, 4, 5]),
                "middle_layer_size": tune.grid_search([8, 16, 32, 64, 128]),
                "epochs": tune.grid_search([500, 1000, 2000, 3000, 4000, 5000]),
                "alpha": tune.grid_search([0.001, 0.01, 0.1, 1]),
            },
            )
            results = {k: v for k, v in sorted(res.results.items(), key=lambda item: (item[1]["mean_loss"], item[1]["time_this_iter_s"]))}
        return list(results.values())[0]
    
    def get_best_network(self):
        '''
        The only function needed to be called to get the best network with it's accuracy and configuration
        '''
        best_result = self.__train_network()
        print(best_result)
        accuracy = best_result["mean_accuracy"] if self.type == "Classification" else best_result["mean_loss"]
        config = best_result["config"]
        network = best_result["network"]
        return network, accuracy, config
    
    def import_model(self, filepath):
        with open(filepath, 'rb') as f:
            res = pickle.load(f, encoding='bytes')
        if not isinstance(res, NeuralNetwork):
            raise TypeError('File does not exist or is corrupted')
        return res

    def export_model(self, filepath, network):
        with open(filepath, 'wb') as f:
            pickle.dump(network, f)