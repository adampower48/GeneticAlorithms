from clickerGame import Game

import Clicker.clickerGA as clickerGA

MAX_GAME_TURNS = 1800
SUBSEC_TURNS = 360
SUBSEC_BUYS = 100
SUBSEC_GENS = 200
SUBSEC_MAX_TIME = 15000 * SUBSEC_TURNS / MAX_GAME_TURNS


def main():
    cga = clickerGA.ClickerGA(max_turns=SUBSEC_TURNS, genome_length=SUBSEC_BUYS, pop_size=200,
                              generations=SUBSEC_GENS, mutate_rate=0.01, breed_rate=0.75, verbose=True,
                              max_time=SUBSEC_MAX_TIME)
    game = Game()

    optimal_order = []
    turns = 0
    while turns < MAX_GAME_TURNS:
        buys = cga.run()
        end_state, buys_ind = clickerGA.simulate(game, cga.max_turns, buys)
        end_state, _ = clickerGA.simulate(game, cga.max_turns, buys[:buys_ind])
        print(end_state, ", buys:", buys_ind, buys)

        optimal_order += buys[:buys_ind]
        game = Game(money=end_state.money, building_count=end_state.building_count[:],
                    upgrades_owned=end_state.upgrades_owned[:])
        cga.game_state = game
        turns += end_state.turns_taken

    print("Optimal buys:", optimal_order)
    print(*clickerGA.simulate(Game(), MAX_GAME_TURNS, optimal_order))


if __name__ == '__main__':
    main()
