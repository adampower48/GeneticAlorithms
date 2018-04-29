import copy
import random

from GeneralGA import GeneticAlgorithm
from MarsLander.landerGame import Game


class LanderGA(GeneticAlgorithm):
    MIN_ANGLE = -90
    MAX_ANGLE = 90
    MIN_POWER = 0
    MAX_POWER = 4

    def __init__(self, pop_size=100, generations=100, mutate_rate=0.1, breed_rate=0.9, genome_length=400,
                 max_turns=400, start_state=None, **kwargs):
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
        # Returns: (angle, power)
        return random.randint(self.MIN_ANGLE, self.MAX_ANGLE), random.randint(self.MIN_POWER, self.MAX_POWER)

    def gen_genome(self):
        return [self.gen_bit() for _ in range(self.genome_length)]

    def check_fitness(self, genome):
        # Evaluates fitness of given instructions based on height
        r = {
            "value": genome,
            "score": 0
        }

        end_state = simulate(self.game_state, self.max_turns, genome)
        r["score"] = end_state.ship_pos[1]

        return r


def simulate(game_state, max_turns, genome, verbose=False):
    game_state = copy.deepcopy(game_state)

    genome_ind = 0
    while genome_ind < len(genome) and not game_state.game_stopped() and game_state.turns < max_turns:
        game_state.apply_order(*genome[genome_ind])
        game_state.advance_turn()

        genome_ind += 1

        if verbose:
            print(game_state)
            print(genome)

    return game_state


if __name__ == '__main__':
    lga = LanderGA()
    best_orders = lga.run()
    print(simulate(Game(), 1000, best_orders, True))
    print(*list(zip(*best_orders)), sep="\n")
