from clickerGame import Game

import Clicker.clickerGA as clickerGA

MAX_GAME_TURNS = 7200
SUBSEC_TURNS = 1200
SUBSEC_BUYS = 75
SUBSEC_GENS = 200000
SUBSEC_MAX_TIME = 10000 * SUBSEC_TURNS / MAX_GAME_TURNS


def main():
    cga = clickerGA.ClickerGA(max_turns=SUBSEC_TURNS, genome_length=SUBSEC_BUYS, generations=SUBSEC_GENS,
                              max_time=SUBSEC_MAX_TIME, verbose=True, verbose_interval=50)
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
    print(*clickerGA.simulate(Game(), MAX_GAME_TURNS, optimal_order, graph=True))


if __name__ == '__main__':
    main()
