# Python implementation of Genetic Algorithm to match string
# https://github.com/frogamic/GeneticHelloWorldJs/blob/master/index.js

import random

MUTATE_RATE = 0.02
BREED_RATE = 0.9
POP_SIZE = 1000
TARGET = "Lorem ipsum dolor sit amet, consectetur adipiscing elit. Sed vehicula mi at tortor mollis, sit amet."

# Constants calculated at program start instead of per func call
MUTATE_RATE_BI = 0.5 * (1 + MUTATE_RATE)
CHARS = [chr(x) for x in range(32, 123)]


def generate_character():
    return chr(random.randrange(32, 123))


def select_parent(elders, tot_score):
    selection = random.random() * tot_score
    _sum = 0
    for e in elders:
        _sum += e["score"]
        if selection <= _sum:
            return e


def generate_pop():
    return ["".join(random.choices(CHARS, k=len(TARGET)))
            for i in range(POP_SIZE)]


def check_fitness(x):
    return {
        "value": x,
        "score": sum([x[i] == TARGET[i] for i in range(len(x))])
    }


def breed(p1, p2):
    rands = [random.random() for _ in range(len(TARGET))]
    return "".join([generate_character() if r < MUTATE_RATE else (p1[i] if r < MUTATE_RATE_BI else p2[i]) for (i, r) in enumerate(rands)])

    # Long version:
    # c = []
    # for i in range(len(TARGET)):
    #     if random.random() < MUTATE_RATE:
    #         c.append(generate_character())
    #     else:
    #         if random.random() < 0.5:
    #             c.append(p1[i])
    #         else:
    #             c.append(p2[i])
    #
    # return "".join(c)


def main():
    population = generate_pop()
    generation = 0

    while True:
        generation += 1
        results = sorted(list(map(check_fitness, population)), key=lambda x: x["score"], reverse=True)
        if results[0]["value"] != TARGET:
            elders = results[:int(POP_SIZE * (1 - BREED_RATE))]
            population = [x["value"] for x in elders]
            tot_score = sum(x["score"] for x in elders)
            for i in range(int(POP_SIZE * BREED_RATE)):
                population.append(
                    breed(select_parent(elders, tot_score)["value"], select_parent(elders, tot_score)["value"]))
        else:
            population = [x["value"] for x in results]

        print("Gen {}: {}, score: {}".format(generation, results[0]["value"], results[0]["score"]))

        if population[0] == TARGET:
            break


if __name__ == '__main__':
    # import cProfile
    # cProfile.run("main()", sort="tottime")
    main()
