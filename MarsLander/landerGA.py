import copy
import random

from GeneralGA import GeneticAlgorithm
from MarsLander.landerGame import Game


class LanderGA(GeneticAlgorithm):
    MIN_ANGLE = -25
    MAX_ANGLE = 25
    MIN_POWER = 3
    MAX_POWER = 4

    # Finite number of user instructions to reduce search space
    possible_actions = (
        (-22, 4), (22, 4),
        (0, 3), (0, 4),
        (-45, 4), (45, 4)
    )

    def __init__(self, pop_size=100, generations=100, mutate_rate=0.02, breed_rate=0.95, genome_length=400,
                 max_turns=400, start_state=None, verbose_interval=10, **kwargs):
        super().__init__(pop_size=pop_size, generations=generations, mutate_rate=mutate_rate, breed_rate=breed_rate,
                         verbose_interval=verbose_interval, **kwargs)

        self.genome_length = genome_length
        self.max_turns = max_turns

        if start_state:
            self.game_state = start_state
        else:
            self.game_state = Game()

    def gen_bit(self):
        # Returns: (angle, power)
        # return random.randint(self.MIN_ANGLE, self.MAX_ANGLE), random.randint(self.MIN_POWER, self.MAX_POWER)
        return random.choice(self.possible_actions)

    def gen_genome(self):
        return [self.gen_bit() for _ in range(self.genome_length)]

    def check_fitness(self, genome):
        # Evaluates fitness of given instructions
        r = {
            "value": genome,
            "score": 0
        }

        end_state = simulate(self.game_state, self.max_turns, genome)

        # Possible scoring criteria
        # r["score"] = end_state.ship_pos[1]  # Height
        # r["score"] = end_state.turns  # Number of turns survived
        # r["score"] = - end_state.distance_to_landing_zone()  # Distance to landing zone
        # r["score"] = -end_state.distance_to_safe_velocity()  # How far off safe velocity
        # r["score"] = - int(not end_state.is_upright())  # Is ship upright

        r["score"] = - end_state.distance_to_landing_zone() - end_state.distance_to_safe_velocity() - int(
            not end_state.is_upright())

        return r


def simulate(game_state, max_turns, genome, verbose=False):
    # Plays game with given instruictions
    game_state = copy.deepcopy(game_state)

    genome_ind = 0
    while genome_ind < len(genome) and not game_state.game_stopped() and game_state.turns < max_turns:
        game_state.apply_order(*genome[genome_ind])
        game_state.advance_turn()

        genome_ind += 1

        if verbose:
            print(game_state)

    if verbose:
        print("crash: {}, Out of fuel: {}".format(game_state.crashed(), game_state.ship_fuel <= 0))
        print("Fitness criteria: distance -{}, velocity -{}, angle -{}".format(
            game_state.distance_to_landing_zone(), game_state.distance_to_safe_velocity(),
            int(not game_state.is_upright())))

    return game_state


if __name__ == '__main__':
    # Round 1
    # game = Game(
    #     terrain=[(0, 100), (1000, 500), (1500, 1500), (3000, 1000), (4000, 150), (5500, 150), (6999, 800)],
    #     ship_pos=(2500, 2700),
    #     ship_fuel=550,
    #     ship_velocity=(0, 0),
    #     ship_angle=0,
    #     ship_power=0,
    # )

    # Round 2
    # game = Game(
    #     terrain=[(0, 100), (1000, 500), (1500, 100), (3000, 100), (3500, 500), (3700, 200), (5000, 1500),
    #              (5800, 300), (6000, 1000), (6999, 2000)],
    #     ship_pos=(6500, 2800),
    #     ship_velocity=(-100, 0),
    #     ship_fuel=600,
    #     ship_angle=90,
    #     ship_power=0
    # )

    # Round 3
    # game = Game(
    #     terrain=[(0, 100), (1000, 500), (1500, 1500), (3000, 1000), (4000, 150), (5500, 150), (6999, 800)],
    #     ship_pos=(6500, 2800),
    #     ship_velocity=(-90, 0),
    #     ship_fuel=750,
    #     ship_angle=90,
    #     ship_power=0
    # )

    # Round 4
    # game = Game(
    #     terrain=[(0, 1000), (300, 1500), (350, 1400), (500, 2000), (800, 1800), (1000, 2500), (1200, 2100),
    #              (1500, 2400), (2000, 1000), (2200, 500), (2500, 100), (2900, 800), (3000, 500), (3200, 1000),
    #              (3500, 2000), (3800, 800), (4000, 200), (5000, 200), (5500, 1500), (6999, 2800)],
    #     ship_pos=(500, 2700),
    #     ship_velocity=(100, 0),
    #     ship_fuel=800,
    #     ship_angle=-90,
    #     ship_power=0
    # )

    # Round 5
    game = Game(
        terrain=[(0, 1000), (300, 1500), (350, 1400), (500, 2100), (1500, 2100), (2000, 200), (2500, 500), (2900, 300),
                 (3000, 200), (3200, 1000), (3500, 500), (3800, 800), (4000, 200), (4200, 800), (4800, 600),
                 (5000, 1200), (5500, 900), (6000, 500), (6500, 300), (6999, 500)],
        ship_pos=(6500, 2700),
        ship_velocity=(- 50, 0),
        ship_fuel=1000,
        ship_angle=90,
        ship_power=0
    )

    lga = LanderGA(start_state=game, generations=50, verbose_interval=5)
    best_orders = lga.run()
    simulate(game, 1000, best_orders, True)
    print(*list(zip(*best_orders)), sep="\n")
