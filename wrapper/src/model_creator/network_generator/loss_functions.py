import numpy as np

epsilon = 0.0001
# loss function and its derivative for regression
def mse(y_true, y_pred):
    return np.mean(np.power(y_true-y_pred, 2));

def mse_derivative(y_true, y_pred):
    return 2*(y_pred-y_true)/y_true.size;

def mae(y_true, y_pred):
    return np.sqrt(np.mean(np.abs(y_true-y_pred)));
def mae_derivative(y_true, y_pred):
    return 2*(y_pred-y_true)/y_true.size;

def rmse(y_true, y_pred):
    y_pred = np.nan_to_num(y_pred)
    return np.sqrt(np.mean(np.power(abs(y_true-y_pred), 2)));
                   
def rmse_derivative(y_true, y_pred):
    y_pred = np.nan_to_num(y_pred)
    return 2*(abs(y_pred-y_true))/y_true.size;

def msle(y_true, y_pred):
    return np.mean(np.power(np.sqrt(abs(y_pred)+epsilon) - np.sqrt(y_true+epsilon), 2));

def msle_derivative(y_true, y_pred):
    return 2*(np.sqrt(abs(y_pred)+epsilon) - np.sqrt(y_true+epsilon))/y_true.size;
# loss function and its derivative for binary an multi-class classification
def cross_entropy_binary(y_true, y_pred):
    return -(y_true * np.log(y_pred+epsilon) + (1-y_true) * np.log(1-y_pred+epsilon));
    #return -np.mean(y_true*np.log(y_pred+epsilon));

def cross_entropy_binary_derivative(y_true, y_pred):
    return -(y_true/(y_pred+epsilon))-((1-y_true)/(1-y_pred+epsilon));

def cross_entropy_multi_class(y_true, y_pred):
    return -np.mean(np.sum(y_true*np.log(y_pred+epsilon), axis=1));

def cross_entropy_multi_class_derivative(y_true, y_pred):
    return -(y_true/(y_pred+epsilon))-((1-y_true)/(1-y_pred+epsilon)).sum(axis=1).reshape(y_true.shape[0], 1);



# def cross_entropy(y_true, y_pred):
#     return -np.mean(y_true*np.log(y_pred)+(1-y_true)*np.log(1-y_pred));

# def cross_entropy_derivative(y_true, y_pred):
#     return -(y_true/y_pred)-((1-y_true)/(1-y_pred));