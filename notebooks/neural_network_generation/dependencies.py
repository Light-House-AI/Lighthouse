import sys
import os

# append dependencies to sys.path
dir_name = os.path.dirname(os.path.abspath(__file__))
dependencies_path = dir_name + '/../../server/automl'
sys.path.append(dependencies_path)

# import dependencies
from neural_network.activation_functions import sigmoid