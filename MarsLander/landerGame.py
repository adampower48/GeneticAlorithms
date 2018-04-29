import math


class Game:
    GRAVITY = -3.711
    MAX_ANGLE_CHANGE = 15

    MIN_ANGLE = -90
    MAX_ANGLE = 90
    MIN_POWER = 0
    MAX_POWER = 4

    TERRAIN_SEG = 10  # Controls granularity of height map generated at start

    def __init__(self):
        self.terrain = [(0, 1500), (1000, 2000), (2000, 500), (3500, 500), (5000, 1500), (6999, 1000)]
        self.landing_zone = (100, 150)

        self.ship_pos = (2500, 2700)
        self.ship_fuel = 550
        self.ship_velocity = (0, 0)
        self.ship_angle = 0
        self.ship_power = 0

        self.turns = 0

        self.terrain_heights = {}
        self.calc_terrain_heights()

    def advance_turn(self):
        # Apply changes here
        self.ship_velocity = (self.ship_velocity[0] + self.ship_power * -math.sin(math.radians(self.ship_angle)),
                              self.ship_velocity[1] + self.ship_power * math.cos(
                                  math.radians(self.ship_angle)) + self.GRAVITY)

        # Update info
        self.ship_fuel -= self.ship_power
        self.ship_pos = (self.ship_pos[0] + self.ship_velocity[0],
                         self.ship_pos[1] + self.ship_velocity[1])

        self.turns += 1

    def apply_order(self, angle, power):
        if power > self.ship_power:
            self.ship_power += 1
        elif power < self.ship_power:
            self.ship_power -= 1

        if angle > self.ship_angle:
            self.ship_angle += min(self.MAX_ANGLE_CHANGE, angle - self.ship_angle)
        elif angle < self.ship_angle:
            self.ship_angle -= min(self.MAX_ANGLE_CHANGE, self.ship_angle - angle)

        self.ship_power = max(self.MIN_POWER, min(self.MAX_POWER, self.ship_power))
        self.ship_angle = max(self.MIN_ANGLE, min(self.MAX_ANGLE, self.ship_angle))

    def game_stopped(self):
        # More conditions (crashed, landed, etc) to be added
        if self.ship_fuel <= 0 or self.crashed():
            return True

        return False

    def calc_terrain_heights(self):
        for i in range(len(self.terrain) - 1):
            l, r = self.terrain[i], self.terrain[i + 1]

            for x in range(l[0] // self.TERRAIN_SEG, r[0], self.TERRAIN_SEG):
                self.terrain_heights[x] = l[1] + ((r[1] - l[1]) / (r[0] - l[0])) * (x - l[0])

    def crashed(self):
        return self.ship_pos[1] <= self.terrain_heights.get(self.ship_pos[0] - self.ship_pos[0] % self.TERRAIN_SEG,
                                                            100000)

    def __str__(self):
        return "x {}, y {}, angle {}, power {}, fuel {}".format(
            *self.ship_pos, self.ship_angle, self.ship_power, self.ship_fuel)


if __name__ == '__main__':
    game = Game()

    ga = (
        -9, -42, 3, 89, 25, -62, 16, -47, 34, -43, -65, 44, 75, -1, 30, -35, 62, -77, -39, 79, 6, -30, -81, 3, 61, 5,
        -38,
        -7, 65, 10, 87, -56, -25, 9, -50, 22, 68, -40, 89, -46, 9, -37, 27, -71, -43, 73, 47, -54, -35, 17, 10, -83,
        -15,
        -83, 19, 8, -59, 79, -73, 17, 3, -26, 6, -73, 23, -45, -42, 24, 0, 45, -85, 7, -27, 1, -73, -60, 71, 89, -81,
        -58,
        52, 54, 6, 13, 49, 7, -61, -54, 5, 19, 26, -18, -67, 70, 3, -88, -2, -42, 5, 81, -64, 57, 10, 14, -81, 28, -30,
        54,
        -28, 14, 11, -43, 33, 34, -69, -27, -15, -37, 3, -55, 65, 52, -25, 64, 85, 46, -65, 2, 45, -13, 66, -50, 52,
        -80,
        -44, -59, 84, 71, -42, 23, -3, 59, -38, 6, 60, 1, 3, -85, 10, 67, -44, -48, 28, -68, 64, -80, -34, 43, 69, -21,
        -34, -44, 29, -27, 49, -12, 41, 12, 89, 36, -43, -80, -26, 71, -51, 86, -43, -27, 46, 1, -74, -90, 31, -87, -8,
        -9,
        73, -54, -79, 79, 68, -31, -39, -16, 9, 47, -56, -65, 24, 49)
    gp = (
        1, 3, 3, 2, 2, 1, 1, 2, 0, 0, 3, 1, 3, 2, 0, 0, 3, 1, 3, 1, 1, 0, 1, 2, 1, 2, 0, 1, 3, 1, 3, 1, 2, 1, 3, 1, 0,
        0, 0,
        2, 1, 1, 0, 1, 0, 1, 1, 3, 3, 3, 1, 1, 3, 3, 2, 2, 2, 0, 2, 3, 1, 3, 2, 0, 1, 0, 2, 0, 2, 0, 2, 2, 1, 2, 1, 0,
        1, 2,
        3, 0, 3, 3, 3, 0, 2, 2, 1, 0, 3, 1, 1, 3, 2, 0, 3, 0, 2, 3, 3, 0, 0, 2, 3, 0, 3, 1, 0, 2, 1, 0, 0, 3, 3, 0, 0,
        0, 1,
        3, 1, 2, 0, 1, 3, 0, 3, 2, 3, 3, 0, 1, 3, 1, 3, 1, 0, 1, 2, 1, 0, 3, 1, 2, 0, 1, 3, 1, 2, 3, 1, 3, 2, 2, 1, 0,
        2, 1,
        1, 0, 0, 0, 2, 3, 0, 3, 0, 2, 0, 3, 1, 1, 1, 2, 0, 0, 3, 1, 3, 3, 0, 3, 1, 2, 0, 3, 2, 2, 1, 0, 0, 2, 1, 0, 1,
        3, 3,
        2, 2, 0, 0, 3)

    for _ in range(20):
        print(game)
        game.apply_order(ga[_], gp[_])
        game.advance_turn()
