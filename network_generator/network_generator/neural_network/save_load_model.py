import pickle
from .neural_network import NeuralNetwork

def import_model(filepath):
    with open(filepath, 'rb') as f:
        res = pickle.load(f, encoding='bytes')
    if not isinstance(res, NeuralNetwork):
        raise TypeError('File does not exist or is corrupted')
    return res

def export_model(filepath, network):
    with open(filepath, 'wb') as f:
        pickle.dump(network, f)