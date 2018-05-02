from MarsLander.landerGA import LanderGA
from MarsLander.landerGame import Game


def main():
    num_land = int(input())
    land = [(x, y) for x, y in [map(int, input().split()) for _ in range(num_land)]]

    game = Game(terrain=land)

    setup = False
    very_best = None
    moves_taken = []

    while True and game.ship_fuel >= 0:
        if not setup:
            values = list(map(int, input().split()))
            game.ship_pos = values[:2]
            game.ship_velocity = values[2:4]
            game.ship_fuel = values[4]
            game.ship_angle = values[5]
            game.ship_power = values[6]
            setup = True
        else:
            # values = input()
            pass

        lga = LanderGA(start_state=game, pop_size=20, breed_rate=0.9, max_time=95, verbose=False)
        best = lga.run()
        best_r = lga.check_fitness(best)
        if not very_best or best_r["score"] > very_best["score"]:
            very_best = best_r

        print(*very_best["value"][0])
        moves_taken.append(very_best["value"][0])
        game.apply_order(*very_best["value"].pop(0))
        game.advance_turn()

        if game.game_stopped():
            print("0 0")
            break

    print(*list(zip(*moves_taken)), game, very_best["score"], sep="\n")
    # print(simulate(game, 1000, very_best, True))


if __name__ == '__main__':
    # cProfile.run("main()", sort="tottime")
    main()
