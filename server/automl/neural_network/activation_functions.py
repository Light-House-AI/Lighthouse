import numpy as np

def tanh(x):
    return np.tanh(x);

def tanh_derivative(x):
    return 1-np.tanh(x)**2;

# activation function and its derivative for binary classification
def sigmoid(x):
    return 1/(1+np.exp(-x))

def sigmoid_derivative(x):
    return sigmoid(x)*(1-sigmoid(x))

# activation function and its derivative for multi-class classification
def softmax(x):
    return np.exp(x) / np.sum(np.exp(x), axis=0)

def softmax_derivative(x):
    return softmax(x)*(1-softmax(x))

# activation function and its derivative for regression
def relu(x):
    return np.maximum(0,x)

def relu_derivative(x):
    return 1. * (x > 0)

def identity(x):
    return x

def identity_derivative(x):
    return 1.