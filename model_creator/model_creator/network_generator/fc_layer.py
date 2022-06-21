from .layer import Layer
import numpy as np

class FCLayer(Layer): #Neural Network Layer
    def __init__(self, input_size, output_size):
        self.weights = np.random.rand(input_size, output_size) - 0.5
        self.bias = np.random.rand(1, output_size) - 0.5

    # returns output for a given input
    def forward_propagation(self, input_data):
        self.input = input_data.reshape(-1, 1).T
        self.output = np.dot(self.input, self.weights) + self.bias
        return self.output
    
    # computes dE/dW, dE/dB for a given output_error=dE/dY. Returns input_error=dE/dX.
    def backward_propagation(self, output_error, learning_rate):
        input_error = np.dot(output_error, self.weights.T)
        weights_error = np.dot(self.input.T, output_error)
        self.__update(learning_rate, weights_error, output_error)
        return input_error
    
    def __update(self, learning_rate, weights_error, output_error):
        self.weights -= learning_rate * weights_error
        self.bias -= learning_rate * output_error