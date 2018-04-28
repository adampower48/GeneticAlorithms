# Finds the optimum starting buy order for idle clicker games
# Current game parameters: Cookie Clicker - http://orteil.dashnet.org/cookieclicker/

import copy
import random

from clickerGame import Game

MAX_GAME_TURNS = 1000
MAX_BUYS = 30

# GA Parameters
POP_SIZE = 200
MUTATE_RATE = 0.05
BREED_RATE = 0.9
MAX_GENERATIONS = 200

# Constants calculated at program start instead of per func call
MUTATE_RATE_BI = 0.5 * (1 + MUTATE_RATE)


def gen_buy(_min=0, _max=len(Game.building_cost)):
    return random.randrange(_min, _max)


def gen_buy_order(l=MAX_BUYS, _min=0, _max=len(Game.building_cost)):
    return [gen_buy(_min, _max) for _ in range(l)]


def gen_pop(n=POP_SIZE, _len=MAX_BUYS, _min=0, _max=len(Game.building_cost)):
    return [gen_buy_order(_len, _min, _max) for _ in range(n)]


def simulate(game_state, max_turns, buy_order):
    # Simulates game until out of buy instructions or given turns exceeded
    game_state = copy.deepcopy(game_state)

    order_ind = 0
    while game_state.turns_taken < max_turns and order_ind < len(buy_order):
        required_turns = game_state.turns_to_buy(buy_order[order_ind])
        if required_turns <= 0:
            game_state.buy_building(buy_order[order_ind])
            order_ind += 1

        game_state.advance_turn(min(required_turns, max_turns - game_state.turns_taken))

    return game_state, order_ind


def check_fitness(x, game_state=None):
    # Evaluates fitness of given buy order based on money per turn
    r = {
        "value": x,
        "score": 0
    }

    if not game_state:
        game_state = Game()

    game_state, order_ind = simulate(game_state, MAX_GAME_TURNS, x)
    r["score"] = round(game_state.money_per_turn(), 1)

    return r


def breed(p1, p2):
    rands = [random.random() for _ in range(len(p1))]
    return [gen_buy() if r < MUTATE_RATE else (p1[i] if r < MUTATE_RATE_BI else p2[i]) for (i, r) in
            enumerate(rands)]


def select_parent(elders, tot_score):
    selection = random.random() * tot_score
    _sum = 0
    for e in elders:
        _sum += e["score"]
        if selection <= _sum:
            return e


def get_optimal_sequence(game_state, l=MAX_BUYS, generations=MAX_GENERATIONS):
    # Attempts to find the optimal build order of given length starting from given game state
    population = gen_pop(_len=l)
    generation = 0

    results = []
    while generation < generations:
        generation += 1
        results = sorted(list(map(lambda x: check_fitness(x, game_state), population)),
                         key=lambda x: x["score"], reverse=True)

        elders = results[:int(POP_SIZE * (1 - BREED_RATE))]
        population = [x["value"] for x in elders]
        tot_score = sum(x["score"] for x in elders)
        for i in range(int(POP_SIZE * BREED_RATE)):
            population.append(breed(select_parent(elders, tot_score)["value"],
                                    select_parent(elders, tot_score)["value"]))

    return results[0]["value"]


def main():
    population = gen_pop()
    generation = 0

    while generation < MAX_GENERATIONS:
        generation += 1
        results = sorted(list(map(check_fitness, population)), key=lambda x: x["score"], reverse=True)

        elders = results[:int(POP_SIZE * (1 - BREED_RATE))]
        population = [x["value"] for x in elders]
        tot_score = sum(x["score"] for x in elders)
        for i in range(int(POP_SIZE * BREED_RATE)):
            population.append(
                breed(select_parent(elders, tot_score)["value"], select_parent(elders, tot_score)["value"]))

        print("Gen {}, score: {}: {}".format(generation, results[0]["score"], "-".join(map(str, results[0]["value"]))))


if __name__ == '__main__':
    # import cProfile
    # cProfile.run("main()", sort="tottime")
    main()
