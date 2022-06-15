class NeuralNetwork:
    def __init__(self):
        self.layers = []
        self.loss = None
        self.loss_derivative = None
        
    # add a layer
    def add(self, layer):
        self.layers.append(layer)
        
    # set loss to use
    def use(self, loss, loss_derivative):
        self.loss = loss
        self.loss_derivative = loss_derivative
    
    # predict output for a given input
    def predict(self, input_data):
        # sample dimension first
        samples = len(input_data)
        input_data = input_data.reshape(input_data.shape[0], 1, input_data.shape[1])
        result = []

        # run network over all samples
        for i in range(samples):
            # forward propagation
            output = input_data[i]
            for layer in self.layers:
                output = layer.forward_propagation(output)
            result.append(output[0])

        return result
    
    # train the network
    def fit(self, x_train, y_train, epochs, learning_rate):
        # sample dimension first
        #samples = 
        self.learning_rate = learning_rate
        batch_size = 8
        prev_error = 1
        stopper = 0
        # training loop wth mini-batch gradient descent
        for i in range(epochs):
            err = 0
            for k in range(0, len(x_train), batch_size):
                batch_error = 0
                # forward propagation
                samples = x_train[k:k+batch_size]
                true_outputs = y_train[k:k+batch_size]
                for j in range(len(samples)):
                    output = samples[j]
                    for layer in self.layers:
                        output = layer.forward_propagation(output)
                    # compute loss (for display purpose only)
                    err += self.loss(true_outputs[j], output)
                    # backward propagation
                    batch_error += self.loss_derivative(true_outputs[j], output)
                # update weights and biases
                batch_error /= batch_size
                for layer in reversed(self.layers):
                    batch_error = layer.backward_propagation(batch_error, self.learning_rate)
            
                
                
            
                
            
            # calculate average error on all samples
            err /= len(x_train)
            # stop epochs if error is not decreasing
            if err > prev_error:
                self.learning_rate /= 2
            if err == prev_error:
                stopper += 1
            if stopper == 10:
                break
            #if(prev_error < err):
                #self.learning_rate *= 0.9
                #self.learning_rate /= 2
            prev_error = err
            print('epoch %d/%d   error=%f' % (i+1, epochs, err))