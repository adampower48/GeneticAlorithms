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
    building_sell_mod = 0.5

    upgrade_cost = (
        (100, 500) + tuple(10000 * 100 ** n for n in range(9)),
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
    upgrade_cost += (tuple(u[1] for u in upgrade_cost[2::]),)  # Grandma upgrades: ind 15
    # todo: Cookie upgrades. NOTE - Multiplicative, not additive
    # List of completed: http://prntscr.com/jn087m
    #
    # tuple(10 ** n - 1 for n in range(6, 9))  # 1%
    # tuple(5 * 10 ** n - 5 for n in range(6, 8))  # 1%
    # tuple(10 ** n - 1 for n in range(9, 11))  # 2%
    # tuple(5 * 10 ** n - 5 for n in range(8, 11))  # 2%
    # (10 ** 11 - 1,) * 2  # 4%
    # tuple(5 * 10 ** n - 5 for n in range(11, 14))  # 2%
    # tuple(10 ** n - 1 for n in range(12, 14))  # 2%
    # ---------------

    upgrade_multipliers = ((2,) * 3,) + ((2,) * 9,) * 14
    cursor_additions = (0.1,) + tuple(0.5 * 10 ** n for n in range(8))
    grandma_upg_effects_base = tuple(0.01 / n for n in range(1, 14))  # Starts at bInd 2 (farm)
    grandma_upgrade_req_buildings = 15  # Number of buildings required to purchase upgrade

    # @profile
    def __init__(self, money=None, tot_money_earned=None, building_count=None, upgrades_owned=None, turns_taken=0,
                 copy=False):
        self.money = money if money is not None else self.building_cost_base[0]
        self.tot_money_earned = tot_money_earned if tot_money_earned is not None else 0
        self.building_count = building_count[:] if building_count else [0] * len(self.building_cost_base)
        self.upgrades_owned = [upgrades_owned[i][:] for i in range(len(upgrades_owned))] if upgrades_owned else [
            [False] * len(v) for v in self.upgrade_cost]
        self.turns_taken = turns_taken

        if not copy:
            self.non_cursors_owned = sum(self.building_count[1:])
            self.tot_cursor_add = sum([o * u for (o, u) in zip(self.upgrades_owned[0][3:], self.cursor_additions)])
            self.building_cost_current = [self.calc_building_cost(bInd) for bInd in range(len(self.building_cost_base))]

            self.calc_upgrade_effects()
            self.buildings_mpt = self.calc_buildings_mpt()
            self.money_per_turn = self.calc_money_per_turn()

    def advance_turn(self, n=1):
        """
        Advances the game by given turns
        :param n: int - number of turns
        """
        self.money += self.money_per_turn * n
        self.tot_money_earned += self.money_per_turn * n
        self.turns_taken += n

    def calc_upgrade_effects(self):
        """
        Calculates total upgrade multipliers for each building
        [m1, m2, m3,...]
        """
        len_bc = len(self.building_count)
        # len_um = len(self.upgrade_multipliers[0])

        # Basic upgrade multipliers
        self.tot_upgrade_muls = [reduce(mul, [
            (self.upgrade_multipliers[bInd][upInd] if self.upgrades_owned[bInd][upInd] else 1) for upInd in
            range(len(self.upgrade_multipliers[bInd]))]) for bInd in range(len_bc)]

        # Cursor upgrades handled in calc_building_mpt

        self.tot_grandma_upg_effects = self.calc_grandma_upg_effects()

    def calc_grandma_upg_effect(self, bInd):
        if bInd < 2:
            return 1

        return 1 + self.grandma_upg_effects_base[bInd - 2] * self.building_count[1] * self.upgrades_owned[15][
            bInd - 2]

    def calc_grandma_upg_effects(self):
        return [self.calc_grandma_upg_effect(bInd) for bInd in range(len(self.building_count))]

    def calc_money_per_turn(self):
        """
        Calculates total money per turn from buildings.
        :return: float - money per turn
        """
        return sum(self.buildings_mpt)

    # @profile
    def calc_building_mpt(self, bInd):
        """
        :param bInd: Index of building
        :return: float - money per turn
        """
        if bInd == 0:
            return self.building_count[bInd] * self.building_output[bInd] * self.tot_upgrade_muls[
                bInd] + self.non_cursors_owned * self.tot_cursor_add
        else:
            return self.building_count[bInd] * self.building_output[bInd] * self.tot_upgrade_muls[bInd] * \
                   self.tot_grandma_upg_effects[bInd]

    def calc_buildings_mpt(self):
        """
        Calculates money per turn for each building.
        :return: list - mpt for each building
        """
        return [self.calc_building_mpt(bInd) for bInd in range(len(self.building_cost_base))]

    def calc_building_cost(self, bInd):
        """
        :param bInd: Index of building
        :return: int - building cost
        """
        return math.ceil(self.building_cost_base[bInd] * self.building_scaling ** self.building_count[bInd])

    def calc_building_sell_price(self, bInd):
        """
        :param bInd: Index of building
        :return: int - building sell price
        """
        return math.ceil(self.building_cost_base[bInd] * self.building_scaling ** (
                self.building_count[bInd] - 1) * self.building_sell_mod)

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

    def turns_to_sell_building(self, bInd):
        if self.building_count[bInd] > 0:
            return 0
        else:
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

        if bInd == 15 and self.building_count[upInd] < 15:
            return 1000000

        cost = self.get_upgrade_cost(bInd, upInd)
        if self.money >= cost:
            return 0
        else:
            try:
                return math.ceil((cost - self.money) / self.money_per_turn)
            except ZeroDivisionError:
                return 1000000

    def buy_building(self, bInd):
        """
        Purchases given building and calculates effects.
        :param bInd: Index of building
        """
        self.money -= self.building_cost_current[bInd]
        self.building_count[bInd] += 1
        self.building_cost_current[bInd] = self.calc_building_cost(bInd)
        self.non_cursors_owned += 1

        if bInd == 1:
            self.tot_grandma_upg_effects = self.calc_grandma_upg_effects()
            self.buildings_mpt = self.calc_buildings_mpt()

        if self.tot_cursor_add > 0:
            self.buildings_mpt[0] = self.calc_building_mpt(0)  # Cursor
        self.buildings_mpt[bInd] = self.calc_building_mpt(bInd)

        self.money_per_turn = self.calc_money_per_turn()

        # if self.money < 0:
        #     raise EnvironmentError("BOUGHT BUILDING WITH NOT ENOUGH MONEY: b {}, m {}".format(bInd, self.money))

    def buy_upgrade(self, bInd, upInd):
        """
        Purchases given upgrade and calculates effects.
        :param bInd: Index of building (0-14), or upgrade type (15+)
        :param upInd: Index of Upgrade
        """
        self.money -= self.upgrade_cost[bInd][upInd]
        self.upgrades_owned[bInd][upInd] = True

        if bInd == 0 and upInd > 2:
            self.tot_cursor_add += self.cursor_additions[upInd - 3]
        elif bInd == 15:
            self.tot_grandma_upg_effects[upInd + 2] = self.calc_grandma_upg_effect(upInd + 2)
        else:
            self.tot_upgrade_muls[bInd] *= self.upgrade_multipliers[bInd][upInd]

        if bInd == 15:
            self.buildings_mpt[upInd + 2] = self.calc_building_mpt(upInd + 2)
        else:
            self.buildings_mpt[bInd] = self.calc_building_mpt(bInd)
        self.money_per_turn = self.calc_money_per_turn()

    def sell_building(self, bInd):
        """
        Sells given building and calculates effects.
        :param bInd: Index of building
        """
        self.money += self.calc_building_sell_price(bInd)

        self.building_count[bInd] -= 1
        self.buildings_mpt[bInd] = self.calc_building_mpt(bInd)
        self.building_cost_current[bInd] = self.calc_building_cost(bInd)
        self.non_cursors_owned -= 1

        self.money_per_turn = self.calc_money_per_turn()

    def get_total_money_earned(self):
        """
        Calculates the total amount of money earned from the start of the game.
        :return: float - money earned
        """
        # This will not work once selling is implemented
        r = self.building_scaling
        return (sum([a * (1 - r ** n) / (1 - r) for (a, n) in zip(self.building_cost_base, self.building_count)])
                + self.money)

    def copy(self):
        """
        Makes a copy of the current game.
        :return: Game - new copy
        """
        g = Game(money=self.money, tot_money_earned=self.tot_money_earned, building_count=self.building_count,
                 upgrades_owned=self.upgrades_owned, turns_taken=self.turns_taken, copy=True)

        g.building_cost_current = self.building_cost_current[:]
        g.tot_upgrade_muls = self.tot_upgrade_muls[:]
        g.buildings_mpt = self.buildings_mpt[:]
        g.tot_grandma_upg_effects = self.tot_grandma_upg_effects[:]

        g.money_per_turn = self.money_per_turn
        g.tot_cursor_add = self.tot_cursor_add
        g.non_cursors_owned = self.non_cursors_owned

        return g

    def __str__(self):
        return "Turn: {}, Money: {:.1f}, MPT: {}".format(self.turns_taken, self.money, self.money_per_turn)


if __name__ == '__main__':
    game = Game()
    game.money = 10000000
    game.buy_building(1)
    # game.buy_upgrade(15, 0)
    game.buy_building(2)
    print(game.buildings_mpt, game.upgrades_owned[15], game.tot_grandma_upg_effects, sep="\n")
