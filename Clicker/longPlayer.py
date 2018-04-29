from clickerGame import Game

import Clicker.clickerGA as clickerGA

OPTIMAL_ORDER_LEN = 100
MAX_GAME_TURNS = 10000
BUYS_PER_SUBORDER = 100
GENS_PER_SUBORDER = 200

if __name__ == '__main__':
    cga = clickerGA.ClickerGA(max_turns=3000, genome_length=BUYS_PER_SUBORDER, pop_size=150,
                              generations=GENS_PER_SUBORDER, mutate_rate=0.03, breed_rate=0.85, verbose=True)
    game = Game()

    optimal_order = []
    turns = 0
    while turns < MAX_GAME_TURNS:
        buys = cga.run()
        end_state, buys_ind = clickerGA.simulate(game, cga.max_turns, buys)
        end_state, _ = clickerGA.simulate(game, cga.max_turns, buys[:buys_ind])
        print(end_state, ", buys:", buys_ind, buys)

        optimal_order += buys[:buys_ind]
        game = Game(money=end_state.money, building_count=end_state.building_count[:])
        cga.game_state = game
        turns += end_state.turns_taken

    print("Optimal buys:", optimal_order)
    print(*clickerGA.simulate(Game(), 10000, optimal_order))
