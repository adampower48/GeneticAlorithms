# Finds the optimum starting buy order for idle clicker games
# Current game parameters: Cookie Clicker - http://orteil.dashnet.org/cookieclicker/

import random

import Clicker.game

MAX_GAME_TURNS = 1000
MAX_BUYS = 30

# GA Parameters
POP_SIZE = 100
MUTATE_RATE = 0.05
BREED_RATE = 0.9

# Constants calculated at program start instead of per func call
MUTATE_RATE_BI = 0.5 * (1 + MUTATE_RATE)


def gen_buy(_min=0, _max=len(Clicker.game.Game.building_cost)):
    return random.randrange(_min, _max)


def gen_buy_order(n=MAX_BUYS):
    return [gen_buy() for _ in range(n)]


def gen_pop(n=POP_SIZE):
    return [gen_buy_order() for _ in range(n)]


def check_fitness(x):
    # Simulates game and evaluates fitness with money per turn
    r = {
        "value": x,
        "score": 0
    }

    game = Clicker.game.Game()

    order_ind = 0
    while game.turns_taken < MAX_GAME_TURNS and order_ind < len(x):
        if game.buy_building(x[order_ind]):
            order_ind += 1

        r["score"] += game.money_per_turn()

        game.advance_turn()

    r["score"] = round(r["score"], 1)
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


if __name__ == '__main__':
    population = gen_pop()
    generation = 0

    while generation < 100:
        generation += 1
        results = sorted(list(map(check_fitness, population)), key=lambda x: x["score"], reverse=True)

        elders = results[:int(POP_SIZE * (1 - BREED_RATE))]
        population = [x["value"] for x in elders]
        tot_score = sum(x["score"] for x in elders)
        for i in range(int(POP_SIZE * BREED_RATE)):
            population.append(
                breed(select_parent(elders, tot_score)["value"], select_parent(elders, tot_score)["value"]))

        print("Gen {}, score: {}: {}".format(generation, results[0]["score"], "".join(map(str, results[0]["value"]))))
