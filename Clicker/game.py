import math


class Game:
    building_cost = [15, 100, 1100, 12000]
    building_output = [0.1, 1, 8, 47]
    building_scaling = 1.15

    def __init__(self):
        self.money = self.building_cost[0]
        self.building_count = [0] * len(self.building_cost)
        self.turns_taken = 0

    def advance_turn(self):
        self.money += self.money_per_turn()
        self.turns_taken += 1

    def money_per_turn(self):
        return sum(map((lambda n, p: n * p), self.building_count, self.building_output))

    def get_cost(self, bInd):
        return math.ceil(self.building_cost[bInd] * self.building_scaling ** self.building_count[bInd])

    def buy_building(self, bInd):
        if self.money >= self.get_cost(bInd):
            self.money -= self.get_cost(bInd)
            self.building_count[bInd] += 1

            return True
        else:
            return False

    def __str__(self):
        return "Turn: {}, Money: {}, MPT: {}".format(self.turns_taken, self.money, self.money_per_turn())


if __name__ == '__main__':
    game = Game()
    print(game)
    for _ in range(10):
        game.advance_turn()
        print(game)
