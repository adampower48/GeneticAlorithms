import random
from copy import deepcopy

import numpy as np

from GeneralGA import GeneticAlgorithm
from NeuralNetwork.Network import Network


class NNGA(GeneticAlgorithm):
    def __init__(self, dimensions, pop_size=50, generations=20, mutate_rate=0.06, breed_rate=0.9, max_time=0,
                 verbose_interval=10, **kwargs):
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

        r["score"] = - simulate(genome, self.dimensions)

        return r

    def breed(self, p1, p2):
        # Fully random bit selection
        # rands = np.random.rand(self.genome_size)
        # r = 0
        # child = []
        # for i in range(len(p1)):
        #     arr_i = []
        #     for j in range(len(p1[i])):
        #         arr_j = []
        #         for k in range(len(p1[i][j])):
        #             if rands[r] < 0.5:
        #                 arr_j.append(p1[i][j][k])
        #             else:
        #                 arr_j.append(p2[i][j][k])
        #             r += 1
        #
        #         arr_i.append(np.array(arr_j))
        #     child.append(np.array(arr_i))
        # child = np.array(child)

        # One-points crossover
        xpos = random.randrange(len(p1))
        if random.random() < 0.5:
            child = np.concatenate((p1[:xpos], p2[xpos:]))
        else:
            child = np.concatenate((p2[:xpos], p1[xpos:]))
        child = deepcopy(child)

        # Randomly choose bits to mutate
        n_mutates = np.random.poisson(self.MUTATE_RATE * self.genome_size)
        for _ in range(n_mutates):
            i = random.randrange(len(child))
            j = random.randrange(len(child[i]))
            k = random.randrange(len(child[i][j]))
            # print(i, j, k)

            child[i][j][k] = self.gen_bit()

        return child


def simulate(genome, dims):
    tot_error = 0
    net = Network(genome, dims)
    for i in range(len(actual_inputs)):
        outputs = net.feedforward(actual_inputs[i])
        error = MSError(actual_outputs[i], outputs)
        tot_error += error

    return tot_error


def MSError(actual, predicted):
    return sum(map(lambda a, p: (a - p) ** 2, actual, predicted))


# actual_inputs = np.array([1, 0, 0])
# actual_outputs = np.array([1, 0, 1])
actual_inputs = np.array([[0, 0],
                          [0, 1],
                          [1, 0],
                          [1, 1]])
actual_outputs = np.array([[0], [1], [1], [0]])

if __name__ == '__main__':
    nnga = NNGA([2, 4, 1])
    best_weights = nnga.run()
    print(*best_weights.tolist(), sep="\n\n")
    net = Network(best_weights, [2, 4, 1])
    print(net.feedforward(actual_inputs[3]))
