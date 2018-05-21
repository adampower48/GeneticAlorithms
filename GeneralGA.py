import random
import time

import numpy


class GeneticAlgorithm:
    """
    Template for genetic algorithm.
    check_fitness, gen_genome, gen_bit must be overwritten
    run may need to be changed if check_fitness requires custom parameters
    """

    DEFAULT_MAX_TIME = 1000000

    def __init__(self, pop_size=100, generations=100, mutate_rate=0.05, breed_rate=0.9, verbose=True,
                 verbose_interval=10, max_time=0, **kwargs):
        self.POP_SIZE = pop_size
        self.GENERATIONS = generations
        self.MUTATE_RATE = mutate_rate
        self.BREED_RATE = breed_rate
        self.MAX_TIME = max_time if max_time else self.DEFAULT_MAX_TIME

        # Constants calculated once here instead of per func call
        # Note: If MUTATE_RATE is changed directly this will not update
        self.MUTATE_RATE_BI = 0.5 * (1 + self.MUTATE_RATE)

        # Misc
        self.verbose = verbose
        self.verbose_interval = verbose_interval

        for k, v in kwargs.items():
            setattr(self, k, v)

    def check_fitness(self, genome):
        r = {
            "value": genome,
            "score": 0
        }

        # Project specific fitness here
        # Must implement above dictionary

        return r

    def breed(self, p1, p2):
        # Fully random chance per bit to mutate
        # rands = [random.random() for _ in range(len(p1))]
        # return [self.gen_bit() if r < self.MUTATE_RATE else (p1[i] if r < self.MUTATE_RATE_BI else p2[i]) for (i, r) in
        #         enumerate(rands)]

        # One point crossover
        xpos = random.randrange(len(p1))
        if random.random() < 0.5:
            child = p1[:xpos] + p2[xpos:]
        else:
            child = p2[:xpos] + p1[xpos:]

        # Randomly choose bits to mutate
        n_mutates = numpy.random.poisson(self.MUTATE_RATE * len(child))
        places = numpy.random.randint(len(child), size=n_mutates).tolist()
        for p in places:
            child[p] = self.gen_bit()

        return child

    def gen_pop(self, n):
        return [self.gen_genome() for _ in range(n)]

    def gen_genome(self):
        # Project specific function here
        pass

    def gen_bit(self):
        # One piece of the genome, may need to be index-specific if bits represent different things
        pass

    def run(self):
        # Attempts to find genome with highest fitness
        time_start = time_ms()

        population = self.gen_pop(self.POP_SIZE)
        results = []
        generation = 0

        while generation < self.GENERATIONS and time_ms() - time_start < self.MAX_TIME:
            generation += 1
            # This lambda may need to be changed depending on your fitness function
            results = sorted(list(map(lambda g: self.check_fitness(g), population)),
                             key=lambda g: g["score"], reverse=True)

            elders = results[:int(self.POP_SIZE * (1 - self.BREED_RATE)) + 1]
            population = [x["value"] for x in elders]
            # tot_score = sum(x["score"] for x in elders)  # Used for Proportional Selection

            for i in range(int(self.POP_SIZE * self.BREED_RATE)):
                # Parent selection
                # p1 = self.proportional_selection(elders, tot_score)["value"]
                # p2 = self.proportional_selection(elders, tot_score)["value"]
                p1 = self.tournament_selection(elders)["value"]
                p2 = self.tournament_selection(elders)["value"]

                population.append(self.breed(p1, p2))

            if self.verbose and generation % self.verbose_interval == 0:
                print("Gen {}, Fit {}".format(generation, results[0]["score"]))

        return results[0]["value"]

    @staticmethod
    def proportional_selection(elders, tot_score):
        # Proportional Selection
        selection = random.random() * tot_score
        _sum = 0
        for e in elders:
            _sum += e["score"]
            if selection <= _sum:
                return e

    @staticmethod
    def tournament_selection(pop, k=2):
        # Tournament Selection
        # https://cstheory.stackexchange.com/questions/14758/tournament-selection-in-genetic-algorithms
        best = None
        for i in range(k):
            ind = pop[random.randrange(len(pop))]
            if not best or ind["score"] > best["score"]:
                best = ind

        return best


def time_ms():
    return time.time() * 1000
