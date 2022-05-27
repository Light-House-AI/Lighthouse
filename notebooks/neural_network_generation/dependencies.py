import sys
import os

# append dependencies to sys.path
dir_name = os.path.dirname(os.path.abspath(__file__))
dependencies_path = dir_name + '/../../server/automl'
sys.path.append(dependencies_path)

# import dependencies
from neural_network.activation_functions import sigmoid, sigmoid_derivative, identity, identity_derivative, tanh, tanh_derivative, relu, relu_derivative
from neural_network.loss_functions import mse, mse_derivative, cross_entropy_binary, cross_entropy_binary_derivative, cross_entropy_multi_class, cross_entropy_multi_class_derivative
from neural_network.neural_network import NeuralNetwork
from neural_network.fc_layer import FCLayer
from neural_network.activation_layer import ActivationLayer
from neural_network.network_generator import NetworkGenerator