# Modelling Codingame's Mars Lander puzzle
# https://www.codingame.com/ide/puzzle/mars-lander-episode-2

import math


class Game:
    GRAVITY = -3.711
    MAX_ANGLE_CHANGE = 15

    MIN_ANGLE = -90
    MAX_ANGLE = 90
    MIN_POWER = 0
    MAX_POWER = 4

    TERRAIN_SEG = 10  # Controls granularity of height map generated at start

    # Landing stuff
    LAND_ANGLE = 0
    LAND_VX = 20
    LAND_VY = 40

    def __init__(self, terrain=((0, 0),), ship_pos=(0, 0), ship_velocity=(0, 0), ship_angle=0, ship_power=0,
                 ship_fuel=0):
        self.terrain = terrain
        self.ship_pos = ship_pos
        self.ship_velocity = ship_velocity
        self.ship_angle = ship_angle
        self.ship_power = ship_power
        self.ship_fuel = ship_fuel

        self.turns = 0

        self.landing_zone = self.find_landing_zone()
        self.terrain_heights = {}
        self.calc_terrain_heights()

    def advance_turn(self):
        # Velocity calculations
        vx_old, vy_old = self.ship_velocity
        vx = self.ship_velocity[0] + self.ship_power * -math.sin(math.radians(self.ship_angle))
        vy = self.ship_velocity[1] + self.ship_power * math.cos(math.radians(self.ship_angle)) + self.GRAVITY
        self.ship_velocity = (vx, vy)

        # Update info
        self.ship_fuel -= self.ship_power
        self.ship_pos = (self.ship_pos[0] + (vx + vx_old) / 2,  # (vx + vx_old) / 2 from eulerscheZahl from CG forum
                         self.ship_pos[1] + (vy + vy_old) / 2)

        # self.ship_pos = tuple(map(round, self.ship_pos))

        self.turns += 1

    def apply_order(self, angle, power):
        # Applies changes given by user
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
        # Generates heightmap from initial height points
        for i in range(len(self.terrain) - 1):
            l, r = self.terrain[i], self.terrain[i + 1]

            for x in range((l[0] // self.TERRAIN_SEG) * self.TERRAIN_SEG, r[0], self.TERRAIN_SEG):
                self.terrain_heights[x] = l[1] + ((r[1] - l[1]) / (r[0] - l[0])) * (x - l[0])

    def get_terrain_height(self, x):
        return self.terrain_heights.get(int(x - x % self.TERRAIN_SEG), 100000)

    def crashed(self):
        return self.ship_pos[1] <= self.get_terrain_height(self.ship_pos[0])

    def distance_to_landing_zone(self):
        land_x = sum(self.landing_zone) / 2
        land_y = self.get_terrain_height(land_x)

        if self.landing_zone[0] < self.ship_pos[0] < self.landing_zone[1]:
            return abs(self.ship_pos[1] - land_y)

        closest_land_x = min(self.landing_zone, key=lambda x: abs(self.ship_pos[0] - x))
        return math.hypot(closest_land_x - self.ship_pos[0], land_y - self.ship_pos[1])

    def distance_to_safe_velocity(self):
        x = max(0, abs(self.ship_velocity[0]) - self.LAND_VX)
        y = max(0, abs(self.ship_velocity[1]) - self.LAND_VY)
        return math.hypot(x, y)

    def is_upright(self):
        return self.ship_angle == 0

    def find_landing_zone(self):
        # Gets landing left & right x values from terrain
        for i in range(len(self.terrain) - 1):
            if self.terrain[i][1] == self.terrain[i + 1][1]:
                return self.terrain[i][0], self.terrain[i + 1][0]

    def get_input_str(self):
        return " ".join([*self.ship_pos, *self.ship_velocity, self.ship_fuel, self.ship_angle, self.ship_power])

    def __str__(self):
        return "x {}, y {}, vx {}, vy {}, fuel {}, angle {}, power {}".format(
            *self.ship_pos, *self.ship_velocity, self.ship_fuel, self.ship_angle, self.ship_power)


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
