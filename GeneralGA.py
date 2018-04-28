import random


class GeneticAlgorithm:
    """
    Template for genetic algorithm.
    check_fitness, gen_genome, gen_bit must be overwritten
    run may need to be changed if check_fitness requires custom parameters

    """

    def __init__(self, pop_size=100, generations=100, mutate_rate=0.05, breed_rate=0.9):
        self.POP_SIZE = pop_size
        self.GENERATIONS = generations
        self.MUTATE_RATE = mutate_rate
        self.BREED_RATE = breed_rate

        # Constants calculated once here instead of per func call
        self.MUTATE_RATE_BI = 0.5 * (1 + self.MUTATE_RATE)

    def check_fitness(self, genome):
        r = {
            "value": genome,
            "score": 0
        }

        # Project specific fitness here

        return r

    def breed(self, p1, p2):
        rands = [random.random() for _ in range(len(p1))]
        return [self.gen_bit() if r < self.MUTATE_RATE else (p1[i] if r < self.MUTATE_RATE_BI else p2[i]) for (i, r) in
                enumerate(rands)]

    def gen_pop(self, n):
        return [self.gen_genome() for _ in range(n)]

    def gen_genome(self):
        # Project specific function here
        pass

    def gen_bit(self):
        # One piece of the genome, may need to be index-specific if bits represent different things
        pass

    def run(self):
        population = self.gen_pop(self.POP_SIZE)
        results = []
        generation = 0

        while generation < self.GENERATIONS:
            generation += 1
            # This lambda may need to be changed depending on your fitness function
            results = sorted(list(map(lambda g: self.check_fitness(g), population)),
                             key=lambda g: g["score"], reverse=True)

            elders = results[:int(self.POP_SIZE * (1 - self.BREED_RATE))]
            population = [x["value"] for x in elders]
            tot_score = sum(x["score"] for x in elders)

            for i in range(int(self.POP_SIZE * self.BREED_RATE)):
                population.append(self.breed(self.select_parent(elders, tot_score)["value"],
                                             self.select_parent(elders, tot_score)["value"]))

        return results[0]["value"]

    @staticmethod
    def select_parent(elders, tot_score):
        selection = random.random() * tot_score
        _sum = 0
        for e in elders:
            _sum += e["score"]
            if selection <= _sum:
                return e
