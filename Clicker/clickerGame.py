import math


class Game:
    building_cost = [15, 100, 1100, 12000, 130000, 1400 * 10 ** 3, 20 * 10 ** 6, 330 * 10 ** 6, 5100 * 10 ** 6,
                     75 * 10 ** 9, 10 ** 12, 14 * 10 ** 12, 170 * 10 ** 12, 2100 * 10 ** 12, 26 * 10 ** 15]
    building_output = [0.1, 1, 8, 47, 260, 1400, 7800, 44000, 260 * 10 ** 3, 1600 * 10 ** 3, 10 * 10 ** 6, 65 * 10 ** 6,
                       430 * 10 ** 6, 2900 * 10 ** 6, 21 * 10 ** 9]
    building_scaling = 1.15

    def __init__(self, money=None, building_count=None, turns_taken=0):
        self.money = money if money else self.building_cost[0]
        self.building_count = building_count[:] if building_count else [0] * len(self.building_cost)
        self.turns_taken = turns_taken

    def advance_turn(self, n=1):
        self.money += self.money_per_turn() * n
        self.turns_taken += n

    def money_per_turn(self):
        return sum(map((lambda n, p: n * p), self.building_count, self.building_output))

    def get_cost(self, bInd):
        return math.ceil(self.building_cost[bInd] * self.building_scaling ** self.building_count[bInd])

    def turns_to_buy(self, bInd):
        if self.money >= self.get_cost(bInd):
            return 0
        else:
            try:
                return math.ceil((self.get_cost(bInd) - self.money) / self.money_per_turn())
            except ZeroDivisionError:
                return 1

    def buy_building(self, bInd):
        if self.money >= self.get_cost(bInd):
            self.money -= self.get_cost(bInd)
            self.building_count[bInd] += 1

            return True
        else:
            return False

    def __str__(self):
        return "Turn: {}, Money: {:.1f}, MPT: {}".format(self.turns_taken, self.money, self.money_per_turn())


if __name__ == '__main__':
    game = Game()
    print(game)
    for _ in range(10):
        game.advance_turn()
        print(game)
