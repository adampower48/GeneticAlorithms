import numpy as np


def sigmoid(x):
    return 1.0 / (1 + np.exp(-x))


class Network:
    # For use with pre-generated weights
    def __init__(self, weights, dims):
        self.weights = weights
        self.dims = dims

    def feedforward(self, x):
        h_layer = x
        for i in range(len(self.dims) - 1):
            # x2 = s(w1*x1 + b1)
            h_layer = sigmoid(np.dot(h_layer, self.weights[i]))

        return h_layer
