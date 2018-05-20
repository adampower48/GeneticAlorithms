# Finds the optimum starting buy order for idle clicker games
# Current game parameters: Cookie Clicker - http://orteil.dashnet.org/cookieclicker/

import copy
import random

from Clicker.clickerGame import Game
from GeneralGA import GeneticAlgorithm


class ClickerGA(GeneticAlgorithm):
    def __init__(self, pop_size=100, generations=100, mutate_rate=0.02, breed_rate=0.95, genome_length=400,
                 max_turns=400, max_time=0, start_state=None, verbose_interval=10, **kwargs):
        super().__init__(pop_size=pop_size, generations=generations, mutate_rate=mutate_rate, breed_rate=breed_rate,
                         max_time=max_time, verbose_interval=verbose_interval, **kwargs)

        self.genome_length = genome_length
        self.max_turns = max_turns

        if start_state:
            self.game_state = start_state
        else:
            self.game_state = Game()

        for k, v in kwargs.items():
            setattr(self, k, v)

    def gen_bit(self):
        # Only buying buildings allowed
        # return random.randrange(len(Game.building_cost))

        # Buying buildinds/upgrades allowed
        # 0: buy building
        # 1: buy upgrade
        action = random.randrange(0, 2)
        if action == 0:
            bInd = random.randrange(len(Game.building_cost))
            return action, bInd

        if action == 1:
            bInd = random.randrange(len(Game.building_cost))
            upInd = random.randrange(len(Game.upgrade_cost[0]))
            return action, bInd, upInd

    def gen_genome(self):
        return [self.gen_bit() for _ in range(self.genome_length)]

    def check_fitness(self, genome):
        # Evaluates fitness of given buy order based on money per turn
        r = {
            "value": genome,
            "score": 0
        }

        game_state, order_ind = simulate(self.game_state, self.max_turns, genome)
        r["score"] = game_state.get_total_money_earned()

        return r


def simulate(game_state, max_turns, actions, graph=False):
    # Simulates game until out of buy instructions or given turns exceeded
    def calc_req_turns(action_ind):
        if actions[action_ind][0] == 0:
            return game_state.turns_to_buy_building(actions[action_ind][1])
        elif actions[action_ind][0] == 1:
            return game_state.turns_to_buy_upgrade(actions[action_ind][1], actions[action_ind][2])
        else:
            return 0

    def perform_action(action_ind):
        if actions[action_ind][0] == 0:
            game_state.buy_building(actions[action_ind][1])
        elif actions[action_ind][0] == 1:
            game_state.buy_upgrade(actions[action_ind][1], actions[action_ind][2])

    game_state = copy.copy(game_state)

    if graph:
        plot_points = []

    action_ind = 0
    required_turns = calc_req_turns(action_ind)
    while required_turns < max_turns - game_state.turns_taken and action_ind < len(actions):
        if required_turns <= 0:
            perform_action(action_ind)

            action_ind += 1
            if action_ind < len(actions):
                required_turns = calc_req_turns(action_ind)

            if graph:
                plot_points.append((game_state.turns_taken, game_state.money_per_turn))

        turns_to_take = min(required_turns, max_turns - game_state.turns_taken)
        game_state.advance_turn(turns_to_take)
        required_turns -= turns_to_take

    if graph:
        print("Plot points:", plot_points)

    return game_state, action_ind


def main():
    cga = ClickerGA(max_turns=3600, genome_length=200, pop_size=200, generations=1000, mutate_rate=0.1, breed_rate=0.75,
                    max_time=30000)
    best_buys = cga.run()
    end_state, nbuys = simulate(Game(), 3600, best_buys, graph=True)
    print("MPT: {}, Buys: {}".format(end_state.money_per_turn, nbuys))
    print("Genome:", best_buys[:nbuys])


if __name__ == '__main__':
    # cProfile.run("main()", sort="tottime")
    main()
