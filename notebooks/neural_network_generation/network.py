import numpy as np
import pickle

class Net:
    def __init__(self, layer_sizes, hyperparameters):
        self.layer_sizes = layer_sizes
        self.n_layers = len(layer_sizes) - 1
        self.hyerparameters = hyperparameters
        self.Ws, self.bs = self._initial_theta()
        
    def _initial_theta(self):
        mu = 0.0
        sigma = 0.001
        Ws, bs = [], []
        for i in range(self.n_layers):
            lhs, rhs = self.network_sizes[i], self.network_sizes[i+1]
            Wi = sigma * np.random.randn(rhs,lhs) + mu
            bi = np.zeros([rhs,1])
            Ws.append(Wi)
            bs.append(bi)
        return Ws, bs
        
    @classmethod
    def import_model(cls, filepath):
        with open(filepath, 'rb') as f:
            res = pickle.load(f, encoding='bytes')
        if not isinstance(res, Net):
            raise TypeError('File does not exist or is corrupted')
        return res

    def export_model(self, filepath):
        with open(filepath, 'wb') as f:
            pickle.dump(self, f)
            
    def _forward(self, X, s_means=None, s_vars=None):

        if self._should_batch_normalize():
            _, _, _, Hs, P = self._forward_bn(X, s_means, s_vars)
            return Hs, P

        Hi = X
        si = None
        Hs = []

        for i in range(self.n_layers):
            Hs.append(Hi)
            Wi, bi = self.Ws[i], self.bs[i]
            si = Wi @ Hi + bi
            Hi = np.maximum(0.0, si)

        P = self._softmax(si)
        return Hs, P
    
    def _backward(self, X, Y, P, Hs):

        N = X.shape[1]
        G = (P - Y)
        grads_W, grads_b = [], []

        for j in range(self.n_layers):

            i = self.n_layers -1 -j # Reversed
            Hi, Wi = Hs[i], self.Ws[i]

            grad_bi = np.mean(G, axis=1).reshape(-1, 1)
            grad_Wi = (G @ Hi.T) / N + (2 * self.lamb * Wi)

            grads_b.append(grad_bi)
            grads_W.append(grad_Wi)

            G = (G.T @ Wi).T
            G[Hi <= 0] = 0.0

        grads_W.reverse()
        grads_b.reverse()

        return grads_W, grads_b


    # ==================== FW/BW passes with Batch Normalization ====================

    def _should_batch_normalize(self):
        return self.descent_params.get('batch_normalize', True)

    @staticmethod
    def _batch_normalize_fw(s, mean=None, var=None):
        if mean is None or var is None:
            eps = 1e-8
            mean = np.mean(s, axis=1).reshape(-1,1)
            var = np.var(s, axis=1).reshape(-1,1) + eps
        s_norm = (s - mean) / (var ** 0.5)
        return s_norm, mean, var

    def _forward_bn(self, X, s_means=None, s_vars=None):

        Hi = X
        Hs = []
        ss = []
        use_estimates = True

        if s_means is None or s_vars is None:
            s_means = []
            s_vars = []
            use_estimates = False

        for i in range(self.n_layers):

            Hs.append(Hi)
            Wi, bi = self.Ws[i], self.bs[i]

            si = Wi @ Hi + bi
            ss.append(si)

            if use_estimates:
                si, mean, var = self._batch_normalize_fw(si, s_means[i], s_vars[i])
            else:
                si, mean, var = self._batch_normalize_fw(si)
                s_means.append(mean)
                s_vars.append(var)

            Hi = np.maximum(0.0, si)

        P = self._softmax(ss[-1])
        assert np.isfinite(P).all()
        return ss, s_means, s_vars, Hs, P

    @staticmethod
    def _batch_normalize_bw(G, si, mean, var):

        eps = 1e-8
        N = G.shape[1]
        var_eps = var + eps
        si_zero_mean = si - mean

        dVar_f = -0.5 * np.sum(G * (var_eps ** (-3 / 2.0)) * si_zero_mean, axis=1).reshape(-1, 1)
        dMean_f = -np.sum(G * (var_eps ** (-1 / 2.0)), axis=1).reshape(-1, 1)

        return G * (var_eps ** (-1 / 2.0)) + (2.0 / N * dVar_f * si_zero_mean) + dMean_f / N

    def _backward_bn(self, X, Y, P, Hs, ss, s_means, s_vars):

        N = X.shape[1]
        G = (P - Y)
        grads_W, grads_b = [], []

        for j in range(self.n_layers):

            i = self.n_layers - 1 - j # Reversed
            Hi, Wi = Hs[i], self.Ws[i]

            grad_bi = np.mean(G, axis=1).reshape(-1, 1)
            grad_Wi = (G @ Hi.T) / N + (2 * self.lamb * Wi)

            assert np.isfinite(grad_bi).all()
            assert np.isfinite(grad_Wi).all()

            grads_b.append(grad_bi)
            grads_W.append(grad_Wi)

            G = (G.T @ Wi).T
            G[Hi <= 0] = 0.0

            if i > 0:
                si, mean, var = ss[i - 1], s_means[i - 1], s_vars[i - 1]
                assert si.shape == G.shape
                G = self._batch_normalize_bw(G, si, mean, var)

        grads_W.reverse()
        grads_b.reverse()

        return grads_W, grads_b


    # ==================== Cost, Accuracy, Utilities ====================

    @staticmethod
    def _softmax(s, axis=0):
        exp_s = np.exp(s)
        exp_sum = np.sum(exp_s, axis=axis)
        return exp_s / exp_sum

    def _cross_entropy_loss(self, X, Y, s_means=None, s_vars=None):
        N = X.shape[1]
        _, P = self._forward(X, s_means, s_vars)
        loss = -Y * np.log(P)
        return np.sum(loss) / N

    def compute_cost(self, X, Y, s_means=None, s_vars=None):
        # Regularization term
        L_2 = np.sum([np.sum(Wi ** 2) for Wi in self.Ws])
        # Cross-entropy loss
        ce_loss = self._cross_entropy_loss(X, Y, s_means, s_vars)
        # Sum of both contributions
        return ce_loss + self.lamb * L_2

    def classify(self, X, s_means=None, s_vars=None):
        _, P = self._forward(X, s_means, s_vars)
        return np.argmax(P, axis=0)

    def compute_accuracy(self, X, y, s_means=None, s_vars=None):
        y_star = self.classify(X, s_means, s_vars)
        correct = np.sum([y_star == y])
        N = X.shape[1]
        return float(correct) / N


    # ==================== Gradient descent ====================

    def train(self, X, Y, X_test, Y_test, silent=False):

        tick_t = timer()

        params = self.descent_params
        batch_size = params.get('batch_size', 100)
        epochs = params.get('epochs', 40)
        eta = params.get('eta', 0.01)
        gamma = params.get('gamma', 0.0)
        decay_rate = params.get('decay_rate', 1.0)
        plateau_guard = params.get('plateau_guard', None)
        overfitting_guard = params.get('overfitting_guard', None)
        output_folder = params.get('output_folder', None)
        batch_normalize = self._should_batch_normalize()

        N = X.shape[1]
        batches = N // batch_size
        Ws, bs = self.Ws, self.bs

        # Prepare the momentum vectors
        v_W = [np.zeros(a.shape) for a in Ws]
        v_b = [np.zeros(a.shape) for a in bs]

        # Convert Y (one-hot) into a normal label representation
        y = np.argmax(Y, axis=0)

        # Keep track of the performance at each epoch
        costs = [self.compute_cost(X, Y)]
        losses = [self._cross_entropy_loss(X, Y)]
        accuracies = [self.compute_accuracy(X, y)]
        times = []
        speed = []
        test_speed = []

        y_test = np.argmax(Y_test, axis=0)
        test_costs = [self.compute_cost(X_test, Y_test)]
        test_losses = [self._cross_entropy_loss(X_test, Y_test)]
        test_accuracies = [self.compute_accuracy(X_test, y_test)]

        s_means_est = None
        s_vars_est = None
        alpha = 0.99

        # For each epoch
        for e in range(1, epochs + 1):

            tick_e = timer()

            # For each mini batch
            for i in range(batches):

                # Extract batch
                i_beg = i * batch_size
                i_end = (i + 1) * batch_size
                X_batch = X[:, i_beg:i_end]
                Y_batch = Y[:, i_beg:i_end]

                # Compute gradients
                if batch_normalize:
                    ss, s_means, s_vars, Hs, P = self._forward_bn(X_batch)
                    grads_W, grads_b = self._backward_bn(X_batch, Y_batch, P, Hs, ss, s_means, s_vars)
                    if s_means_est is None:
                        s_means_est = s_means
                        s_vars_est = s_vars
                    else:
                        s_means_est = [alpha * s_means_est[l] + (1 - alpha) * s_means[l] for l in range(len(s_means))]
                        s_vars_est = [alpha * s_vars_est[l] + (1 - alpha) * s_vars[l] for l in range(len(s_vars))]
                else:
                    Hs, P = self._forward(X_batch)
                    grads_W, grads_b = self._backward(X_batch, Y_batch, P, Hs)

                # Update W and b
                for j in range(len(Ws)):
                    v_W[j] = gamma * v_W[j] + eta * grads_W[j]
                    v_b[j] = gamma * v_b[j] + eta * grads_b[j]
                    Ws[j] -= v_W[j]
                    bs[j] -= v_b[j]

            # Apply the decay rate to eta
            eta *= decay_rate

            # Keep track of the performance at each epoch
            costs.append(self.compute_cost(X, Y, s_means_est, s_vars_est))
            losses.append(self._cross_entropy_loss(X, Y, s_means_est, s_vars_est))
            accuracies.append(self.compute_accuracy(X, y, s_means_est, s_vars_est))

            test_costs.append(self.compute_cost(X_test, Y_test, s_means_est, s_vars_est))
            test_losses.append(self._cross_entropy_loss(X_test, Y_test, s_means_est, s_vars_est))
            test_accuracies.append(self.compute_accuracy(X_test, y_test, s_means_est, s_vars_est))

            dJ = costs[-1] - costs[-2]
            dJ_star = test_costs[-1] - test_costs[-2]

            speed.append(dJ)
            test_speed.append(dJ_star)
            mean_dJ_star = np.mean(test_speed[-2:])

            if output_folder is not None:
                filepath = "{}/model_epoch_{}.pkl".format(output_folder, e)
                self.export_model(filepath)

            if not silent:
                tock_e = timer()
                interval = tock_e - tick_e
                times.append(interval)
                rem = (epochs - e) * np.mean(times[-3:])
                print('===> Epoch[{}]: {}s remaining, {} dJ, {} dJ*, {} J, {} J*, acc_v: {}%'.format(e, int(round(rem)), round(dJ, 5), round(dJ_star, 5), round(costs[-1], 5), round(test_costs[-1], 5), round(100.0*test_accuracies[-1], 5)))

            if overfitting_guard is not None and mean_dJ_star >= overfitting_guard:
                print('Overfitting detected, aborting training...')
                break

            if eta > 0.001 and plateau_guard is not None and mean_dJ_star >= plateau_guard:
                if not silent:
                    print('Plateau reached, adjusting eta...')
                eta /= 10.0

        if not silent:
            tock_t = timer()
            print("Done. Took ~{}s".format(round(tock_t - tick_t)))
            best_epoch = np.argmax(test_accuracies)
            best_test_acc = test_accuracies[best_epoch]
            print("Best test accuracy reached at epoch {} ({}%)".format(best_epoch, round(best_test_acc*100.0, 4)))

        return {
            'costs': costs,
            'test_costs': test_costs,
            'losses': losses,
            'test_losses': test_losses,
            'accuracies': accuracies,
            'test_accuracies': test_accuracies,
            'speed': speed,
            'test_speed': test_speed,
            'params': params
        }