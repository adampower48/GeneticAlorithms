import random
from copy import deepcopy

import numpy as np

from GeneralGA import GeneticAlgorithm
from NeuralNetwork.Network import Network


class NNGA(GeneticAlgorithm):
    def __init__(self, dimensions, pop_size=50, generations=100, mutate_rate=0.05, breed_rate=0.9, max_time=0,
                 verbose_interval=1, **kwargs):
        super().__init__(pop_size=pop_size, generations=generations, mutate_rate=mutate_rate, breed_rate=breed_rate,
                         max_time=max_time, verbose_interval=verbose_interval, **kwargs)

        self.dimensions = dimensions
        self.genome_size = sum(self.dimensions[i] * self.dimensions[i + 1] for i in range(len(self.dimensions) - 1))

        for k, v in kwargs.items():
            setattr(self, k, v)

    def gen_bit(self):
        return np.random.rand()

    def gen_genome(self):
        return np.array(
            [np.random.rand(self.dimensions[i], self.dimensions[i + 1]) for i in range(len(self.dimensions) - 1)])

    def check_fitness(self, genome):
        r = {
            "value": genome,
            "score": 0
        }

        output = simulate(genome, self.dimensions)
        r["score"] = - MSError(actual_outputs, output)

        return r

    def breed(self, p1, p2):
        xpos = random.randrange(len(p1))
        if random.random() < 0.5:
            child = np.concatenate((p1[:xpos], p2[xpos:]))
        else:
            child = np.concatenate((p2[:xpos], p1[xpos:]))
        child = deepcopy(child)

        # Randomly choose bits to mutate todo: fix this, Needs to work with ndarrays.
        n_mutates = np.random.poisson(self.MUTATE_RATE * self.genome_size)
        for _ in range(n_mutates):
            i = random.randrange(len(child))
            j = random.randrange(len(child[i]))
            k = random.randrange(len(child[i][j]))
            # print(i, j, k)

            child[i][j][k] = self.gen_bit()

        return child


def simulate(genome, dims):
    net = Network(genome, dims)
    return net.feedforward(actual_inputs)


def MSError(actual, predicted):
    return sum(map(lambda a, p: (a - p) ** 2, actual, predicted))


actual_inputs = np.array([1, 0, 0])
actual_outputs = np.array([1, 0, 1])

if __name__ == '__main__':
    nnga = NNGA([3, 4, 4, 3])
    best_weights = nnga.run()
    print(*best_weights.tolist(), sep="\n\n")
