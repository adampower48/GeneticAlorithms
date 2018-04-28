import geneticPlayer as gp
from clickerGame import Game

OPTIMAL_ORDER_LEN = 100
BUYS_PER_SUBORDER = 30
GENS_PER_SUBORDER = 100

if __name__ == '__main__':
    game = Game()
    optimal_order = []

    while len(optimal_order) < OPTIMAL_ORDER_LEN:
        buys = gp.get_optimal_sequence(game, BUYS_PER_SUBORDER, GENS_PER_SUBORDER)
        end_state, buys_ind = gp.simulate(game, gp.MAX_GAME_TURNS, buys)
        print(buys, end_state, ", buys:", buys_ind)

        optimal_order += buys[:buys_ind]
        game = Game(money=end_state.money, building_count=end_state.building_count[:])

    print("Optimal buys:", optimal_order)
    print(*gp.simulate(Game(), 100000, optimal_order))
