# Finds the optimum starting buy order for idle clicker games
# Current game parameters: Cookie Clicker - http://orteil.dashnet.org/cookieclicker/

import copy
import random

from clickerGame import Game

from GeneralGA import GeneticAlgorithm


class ClickerGA(GeneticAlgorithm):
    def __init__(self, pop_size=200, generations=200, mutate_rate=0.05, breed_rate=0.9, genome_length=20,
                 max_turns=1000, start_state=None, **kwargs):
        super().__init__(pop_size=pop_size, generations=generations, mutate_rate=mutate_rate, breed_rate=breed_rate)

        self.genome_length = genome_length
        self.max_turns = max_turns

        if start_state:
            self.game_state = start_state
        else:
            self.game_state = Game()

        for k, v in kwargs.items():
            setattr(self, k, v)

    def gen_bit(self):
        return random.randrange(len(Game.building_cost))

    def gen_genome(self):
        return [self.gen_bit() for _ in range(self.genome_length)]

    def check_fitness(self, genome):
        # Evaluates fitness of given buy order based on money per turn
        r = {
            "value": genome,
            "score": 0
        }

        game_state, order_ind = simulate(self.game_state, self.max_turns, genome)
        r["score"] = round(game_state.money_per_turn(), 1)

        return r


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


if __name__ == '__main__':
    cga = ClickerGA(max_turns=5000, genome_length=50, pop_size=100, generations=500, mutate_rate=0.05, breed_rate=0.9)
    best_buys = cga.run()
    end_state, nbuys = simulate(Game(), 5000, best_buys)
    print("MPT: {}, Buys: {}".format(end_state.money_per_turn(), nbuys))
    print("Genome:", best_buys[:nbuys])
