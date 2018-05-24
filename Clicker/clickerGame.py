import math
from functools import reduce
from operator import mul


class Game:
    # Base cost
    building_cost_base = (15,
                          100,
                          1100,
                          12000,
                          130000,
                          14 * 10 ** 5,
                          2 * 10 ** 7,
                          33 * 10 ** 7,
                          51 * 10 ** 8,
                          75 * 10 ** 9,
                          10 ** 12,
                          14 * 10 ** 12,
                          17 * 10 ** 13,
                          21 * 10 ** 14,
                          26 * 10 ** 15)
    # Base output
    building_output = (0.1,
                       1,
                       8,
                       47,
                       260,
                       1400,
                       7800,
                       44000,
                       26 * 10 ** 4,
                       16 * 10 ** 5,
                       10 ** 7,
                       65 * 10 ** 6,
                       43 * 10 ** 7,
                       29 * 10 ** 8,
                       21 * 10 ** 9)

    building_scaling = 1.15

    upgrade_cost = (
        (100, 500),  # + tuple(10000 * 100 ** n for n in range(9)),
        (1000,) + tuple(5000 * 100 ** n for n in range(8)),
        (11000, 55000) + tuple(550000 * 100 ** n for n in range(7)),
        (120000, 600000) + tuple((6 * 10 ** 6) * 100 ** n for n in range(7)),
        (13 * 10 ** 5, 65 * 10 ** 5) + tuple((65 * 10 ** 6) * 100 ** n for n in range(7)),
        (14 * 10 ** 6, 7 * 10 ** 7) + tuple((7 * 10 ** 8) * 100 ** n for n in range(7)),
        (2 * 10 ** 8, 10 ** 9) + tuple((10 ** 10) * 100 ** n for n in range(7)),
        (33 * 10 ** 8, 165 * 10 ** 8) + tuple((165 * 10 ** 9) * 100 ** n for n in range(7)),
        (51 * 10 ** 9, 255 * 10 ** 9) + tuple((255 * 10 ** 10) * 100 ** n for n in range(7)),
        (75 * 10 ** 10, 375 * 10 ** 10) + tuple((375 * 10 ** 11) * 100 ** n for n in range(7)),
        (10 ** 13, 5 * 10 ** 13) + tuple((10 ** 14) * 100 ** n for n in range(7)),
        (14 * 10 ** 13, 7 * 10 ** 14) + tuple((7 * 10 ** 15) * 100 ** n for n in range(7)),
        (17 * 10 ** 14, 85 * 10 ** 14) + tuple((85 * 10 ** 15) * 100 ** n for n in range(7)),
        (21 * 10 ** 15, 105 * 10 ** 15) + tuple((105 * 10 ** 16) * 100 ** n for n in range(7)),
        (26 * 10 ** 16, 13 * 10 ** 17) + tuple((13 * 10 ** 17) * 100 ** n for n in range(7)),
    )

    upgrade_multipliers = ((2, 2),) + ((2,) * 9,) * 14

    # @profile
    def __init__(self, money=None, building_count=None, upgrades_owned=None, turns_taken=0, copy=False):
        self.money = money if money else self.building_cost_base[0]
        self.building_count = building_count[:] if building_count else [0] * len(self.building_cost_base)
        self.upgrades_owned = [upgrades_owned[i][:] for i in range(len(upgrades_owned))] if upgrades_owned else [
            [False] * len(v) for v in self.upgrade_cost]
        self.turns_taken = turns_taken

        if not copy:
            self.building_cost_current = [self.calc_building_cost(bInd) for bInd in range(len(self.building_cost_base))]
            self.tot_upgrade_muls = [1] * len(self.building_count)
            self.buildings_mpt = self.calc_buildings_mpt()
            self.money_per_turn = self.calc_money_per_turn()

    def advance_turn(self, n=1):
        """
        Advances the game by given turns
        :param n: int - number of turns
        """
        self.money += self.money_per_turn * n
        self.turns_taken += n

    def calc_upgrade_effects(self):
        """
        Calculates total upgrade multipliers for each building
        [m1, m2, m3,...]
        """
        len_bc = len(self.building_count)
        len_um = len(self.upgrade_multipliers[0])

        self.tot_upgrade_muls = [reduce(mul, [
            (self.upgrade_multipliers[bInd][upInd] if self.upgrades_owned[bInd][upInd] else 1) for upInd in
            range(len_um)]) for bInd in range(len_bc)]

    def calc_money_per_turn(self):
        """
        Calculates total money per turn from buildings.
        :return: float - money per turn
        """
        return sum(self.buildings_mpt)

    def calc_building_mpt(self, bInd):
        """
        :param bInd: Index of building
        :return: float - money per turn
        """
        return self.building_count[bInd] * self.building_output[bInd] * self.tot_upgrade_muls[bInd]

    def calc_buildings_mpt(self):
        """
        Calculates money per turn for each building.
        :return: list - mpt for each building
        """
        return [self.calc_building_mpt(bInd) for bInd in range(len(self.building_cost_base))]

    def calc_building_cost(self, bInd):
        """
        :param bInd: Index of building
        :return: float - building cost
        """
        return math.ceil(self.building_cost_base[bInd] * self.building_scaling ** self.building_count[bInd])

    def get_upgrade_cost(self, bInd, upInd):
        """
        :param bInd: Index of building
        :param upInd: Index of upgrade
        :return: int - upgrade cost
        """
        return self.upgrade_cost[bInd][upInd]

    def turns_to_buy_building(self, bInd):
        """
        Calculates number of turns until there is enough money to purchase given building.
        :param bInd: Index of building
        :return: int - number of turns
        """
        cost = self.building_cost_current[bInd]
        if self.money >= cost:
            return 0
        else:
            try:
                return math.ceil((cost - self.money) / self.money_per_turn)
            except ZeroDivisionError:
                return 1000000

    def turns_to_buy_upgrade(self, bInd, upInd):
        """
        Calculates number of turns until there is enough money to purchase given upgrade.
        :param bInd: Index of building
        :param upInd: Index of upgrade
        :return: int - number of turns
        """
        if self.upgrades_owned[bInd][upInd]:
            return 1000000

        cost = self.get_upgrade_cost(bInd, upInd)
        if self.money >= cost:
            return 0
        else:
            try:
                return math.ceil((cost - self.money) / self.money_per_turn)
            except ZeroDivisionError:
                return 1000000

    # @profile
    def buy_building(self, bInd):
        """
        Purchases given building and calculates effects.
        :param bInd: Index of building
        """
        self.money -= self.building_cost_current[bInd]

        self.building_count[bInd] += 1
        self.buildings_mpt[bInd] = self.calc_building_mpt(bInd)
        self.building_cost_current[bInd] = self.calc_building_cost(bInd)

        self.money_per_turn = self.calc_money_per_turn()

        # if self.money < 0:
        #     raise EnvironmentError("BOUGHT BUILDING WITH NOT ENOUGH MONEY: b {}, m {}".format(bInd, self.money))

    def buy_upgrade(self, bInd, upInd):
        """
        Purchases given upgrade and calculates effects.
        :param bInd: Index of building
        :param upInd: Index of Upgrade
        """
        self.money -= self.upgrade_cost[bInd][upInd]

        self.upgrades_owned[bInd][upInd] = True
        self.calc_upgrade_effects()

        self.buildings_mpt[bInd] = self.calc_building_mpt(bInd)
        self.money_per_turn = self.calc_money_per_turn()

    def get_total_money_earned(self):
        """
        Calculates the total amount of money earned from the start of the game.
        :return: float - money earned
        """
        # This will not work once selling is implemented
        r = self.building_scaling
        return (sum(a * (1 - r ** n) / (1 - r) for (a, n) in zip(self.building_cost_base, self.building_count))
                + self.money)

    def copy(self):
        """
        Makes a copy of the current game.
        :return: Game - new copy
        """
        g = Game(money=self.money, building_count=self.building_count, upgrades_owned=self.upgrades_owned,
                 turns_taken=self.turns_taken, copy=True)
        g.building_cost_current = self.building_cost_current[:]
        g.tot_upgrade_muls = self.tot_upgrade_muls[:]
        g.buildings_mpt = self.buildings_mpt[:]
        g.money_per_turn = self.money_per_turn

        return g

    def __str__(self):
        return "Turn: {}, Money: {:.1f}, MPT: {}".format(self.turns_taken, self.money, self.money_per_turn)


if __name__ == '__main__':
    import cProfile

    game = Game()
    game.money = 10000
    # game.buy_upgrade(0, 0)
    cProfile.run("game.buy_upgrade(0,0)", sort="tottime")
