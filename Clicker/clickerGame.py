import math


class Game:
    # Base cost
    building_cost_base = [15, 100, 1100, 12000, 130000, 1400 * 10 ** 3, 20 * 10 ** 6, 330 * 10 ** 6, 5100 * 10 ** 6,
                          75 * 10 ** 9, 10 ** 12, 14 * 10 ** 12, 170 * 10 ** 12, 2100 * 10 ** 12, 26 * 10 ** 15]
    # Base output
    building_output = [0.1, 1, 8, 47, 260, 1400, 7800, 44000, 260 * 10 ** 3, 1600 * 10 ** 3, 10 * 10 ** 6, 65 * 10 ** 6,
                       430 * 10 ** 6, 2900 * 10 ** 6, 21 * 10 ** 9]

    building_scaling = 1.15

    upgrade_cost = (
        (100, 500),
        (1000, 5000),
        (11000, 55000),
        (120000, 600000),
        (1300 * 10 ** 3, 6500 * 10 ** 3),
        (14 * 10 ** 6, 70 * 10 ** 6),
        (200 * 10 ** 6, 10 ** 9),
        (3300 * 10 ** 6, 16500 * 10 ** 6),
        (51 * 10 ** 9, 255 * 10 ** 9),
        (750 * 10 ** 9, 3750 * 10 ** 9),
        (10 * 10 ** 12, 50 * 10 ** 12),
        (140 * 10 ** 12, 700 * 10 ** 12),
        (1700 * 10 ** 12, 8500 * 10 ** 12),
        (21 * 10 ** 15, 105 * 10 ** 15),
        (260 * 10 ** 15, 1300 * 10 ** 15),
    )

    upgrade_multipliers = (
        (2, 2),
        (2, 2),
        (2, 2),
        (2, 2),
        (2, 2),
        (2, 2),
        (2, 2),
        (2, 2),
        (2, 2),
        (2, 2),
        (2, 2),
        (2, 2),
        (2, 2),
        (2, 2),
        (2, 2),
    )

    def __init__(self, money=None, building_count=None, upgrades_owned=None, turns_taken=0):
        self.money = money if money else self.building_cost_base[0]
        self.building_count = tuple(building_count) if building_count else tuple([0] * len(self.building_cost_base))
        self.upgrades_owned = tuple(upgrades_owned) if upgrades_owned else tuple(
            (False,) * len(v) for v in self.upgrade_cost)
        self.turns_taken = turns_taken

        self.building_cost_current = tuple(
            self.calc_building_cost(bInd) for bInd in range(len(self.building_cost_base)))
        self.tot_upgrade_muls = [1] * len(self.building_count)
        self.buildings_mpt = self.calc_buildings_mpt()
        self.money_per_turn = self.calc_money_per_turn()

    def advance_turn(self, n=1):
        self.money += self.money_per_turn * n
        self.turns_taken += n

    def calc_upgrade_effects(self):
        len_bc = len(self.building_count)
        len_um = len(self.upgrade_multipliers[0])

        self.tot_upgrade_muls = [1] * len_bc
        for bInd in range(len_bc):
            for upInd in range(len_um):
                if self.upgrades_owned[bInd][upInd]:
                    self.tot_upgrade_muls[bInd] *= self.upgrade_multipliers[bInd][upInd]

    def calc_money_per_turn(self):
        return sum(self.buildings_mpt)

    def calc_building_mpt(self, bInd):
        return self.building_count[bInd] * self.building_output[bInd] * self.tot_upgrade_muls[bInd]

    def calc_buildings_mpt(self):
        return tuple(self.calc_building_mpt(bInd) for bInd in range(len(self.building_cost_base)))

    def calc_building_cost(self, bInd):
        return math.ceil(self.building_cost_base[bInd] * self.building_scaling ** self.building_count[bInd])

    def get_upgrade_cost(self, bInd, upInd):
        return self.upgrade_cost[bInd][upInd]

    def turns_to_buy_building(self, bInd):
        cost = self.building_cost_current[bInd]
        if self.money >= cost:
            return 0
        else:
            try:
                return math.ceil((cost - self.money) / self.money_per_turn)
            except ZeroDivisionError:
                return 1000000

    def turns_to_buy_upgrade(self, bInd, upInd):
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
        self.money -= self.building_cost_current[bInd]

        # self.building_count[bInd] += 1
        self.building_count = self.building_count[:bInd] + (self.building_count[bInd] + 1,) + self.building_count[
                                                                                              bInd + 1:]

        # self.buildings_mpt[bInd] = self.calc_building_mpt(bInd)
        self.buildings_mpt = self.buildings_mpt[:bInd] + (self.calc_building_mpt(bInd),) + self.buildings_mpt[bInd + 1:]

        # self.building_cost_current[bInd] = self.calc_building_cost(bInd)
        self.building_cost_current = self.building_cost_current[:bInd] + (
            self.calc_building_cost(bInd),) + self.building_cost_current[bInd + 1:]

        self.money_per_turn = self.calc_money_per_turn()

        # if self.money < 0:
        #     raise EnvironmentError("BOUGHT BUILDING WITH NOT ENOUGH MONEY: b {}, m {}".format(bInd, self.money))

    def buy_upgrade(self, bInd, upInd):
        if self.money >= self.upgrade_cost[bInd][upInd]:
            self.money -= self.upgrade_cost[bInd][upInd]

            # self.upgrade_owned[bInd][upInd] = True
            self.upgrades_owned = self.upgrades_owned[:bInd] + (self.upgrades_owned[bInd][:upInd] + (
                self.upgrades_owned[bInd][upInd] + 1,) + self.upgrades_owned[bInd][upInd + 1:],
                                                                ) + self.upgrades_owned[bInd + 1:]
            self.calc_upgrade_effects()

            # self.buildings_mpt[bInd] = self.calc_building_mpt(bInd)
            self.buildings_mpt = self.buildings_mpt[:bInd] + (
                self.calc_building_mpt(bInd),) + self.buildings_mpt[bInd + 1:]
            self.money_per_turn = self.calc_money_per_turn()

            return True
        else:
            return False

    def get_total_money_earned(self):
        # This will not work once selling is implemented
        r = self.building_scaling
        return sum(
            a * (1 - r ** n) / (1 - r) for (a, n) in zip(self.building_cost_base, self.building_count)) + self.money

    def __str__(self):
        return "Turn: {}, Money: {:.1f}, MPT: {}".format(self.turns_taken, self.money, self.money_per_turn)


if __name__ == '__main__':
    import cProfile

    game = Game()
    game.money = 10000
    # game.buy_upgrade(0, 0)
    cProfile.run("game.buy_upgrade(0,0)", sort="tottime")
