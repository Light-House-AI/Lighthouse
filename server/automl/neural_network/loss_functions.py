import numpy as np

# loss function and its derivative for regression
def mse(y_true, y_pred):
    return np.mean(np.power(y_true-y_pred, 2));

def mse_derivative(y_true, y_pred):
    return 2*(y_pred-y_true)/y_true.size;

# loss function and its derivative for binary an multi-class classification
def cross_entropy(y_true, y_pred):
    return -np.mean(y_true*np.log(y_pred)+(1-y_true)*np.log(1-y_pred));

def cross_entropy_derivative(y_true, y_pred):
    return -(y_true/y_pred)-((1-y_true)/(1-y_pred));