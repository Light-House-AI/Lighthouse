from layer import Layer
import numpy as np

hyperparameters = {
    "number_of_layers": 2,
    "number_of_neurons": [2, 1],
    "activation_function": "sigmoid",
    "learning_rate": 0.1,
    "epochs": 100,
    "batch_size": 1,
    "loss_function": "mean_squared_error",
    "optimizer": "adam",
}

class FCLayer(Layer): #Neural Network Layer
    def __init__(self, input_size, output_size):
        self.weights = np.random.rand(input_size, output_size) - 0.5
        self.bias = np.random.rand(1, output_size) - 0.5
        # self.learning_rate = hyperparameters["learning_rate"]
        # self.number_of_neurons = hyperparameters["number_of_neurons"]
        # self.number_of_layers = hyperparameters["number_of_layers"]
        # self.activation_function = hyperparameters["activation_function"]
        # self.epochs = hyperparameters["epochs"]
        # self.loss_function = hyperparameters["loss_function"]
        # self.optimizer = hyperparameters["optimizer"]
        
    def error(self):
        pass
    
    # returns output for a given input
    def forward_propagation(self, input_data):
        self.input = input_data
        self.output = np.dot(self.input, self.weights) + self.bias
        return self.output
    
    # computes dE/dW, dE/dB for a given output_error=dE/dY. Returns input_error=dE/dX.
    def backward_propagation(self, error, learning_rate):
        input_error = np.dot(error, self.weights.T)
        weights_error = np.dot(self.input.T, error)
        self.__update(learning_rate, weights_error, error)
        return input_error
    
    def __update(self, learning_rate, weights_error, error):
        self.weights -= learning_rate * weights_error
        self.bias -= learning_rate * error