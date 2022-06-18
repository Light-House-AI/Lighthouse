#Abstract class
class Layer:
    def __init__(self):
        self.input = None
        self.output = None

    # computes the output Y of a layer for a given input X
    def forward_propagation(self, input):
        pass

    # computes dE/dX for a given dE/dY (and update parameters if any)
    def backward_propagation(self, error, learning_rate):
        pass