from clickerGame import Game

import Clicker.clickerGA as clickerGA

MAX_GAME_TURNS = 7200
SUBSEC_TURNS = 1200
SUBSEC_BUYS = 75
SUBSEC_GENS = 200000
SUBSEC_MAX_TIME = 600000 * SUBSEC_TURNS / MAX_GAME_TURNS


def main():
    cga = clickerGA.ClickerGA(max_turns=SUBSEC_TURNS, genome_length=SUBSEC_BUYS, generations=SUBSEC_GENS,
                              max_time=SUBSEC_MAX_TIME, verbose=True, verbose_interval=50)
    game = Game()

    optimal_order = []
    turns = 0
    while cga.max_turns <= MAX_GAME_TURNS:
        buys = cga.run()
        end_state, buys_ind = clickerGA.simulate(game, cga.max_turns + turns, buys)
        end_state, _ = clickerGA.simulate(game, cga.max_turns + turns, buys[:buys_ind])
        print(end_state, ", buys:", buys_ind, buys[:buys_ind])

        optimal_order += buys[:buys_ind]
        game = end_state.copy()
        cga.game_state = game
        cga.max_turns += SUBSEC_TURNS
        turns = end_state.turns_taken

    print("Optimal buys:", optimal_order)
    g, _ = clickerGA.simulate(Game(), MAX_GAME_TURNS, optimal_order, graph=True)
    print(g)


if __name__ == '__main__':
    # import cProfile
    #
    # cProfile.run("main()", sort="tottime")
    main()
