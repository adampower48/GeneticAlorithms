class Game:
    GRID_HEIGHT = 5
    GRID_WIDTH = 5

    def __init__(self, player_pos=(0, 0), enemy_pos=(1, 1)):
        # -1: unplayable
        # 0-3: playable w/ tower height
        self.grid = [[0] * self.GRID_HEIGHT for j in range(self.GRID_WIDTH)]
        self.player_pos = player_pos
        self.enemy_pos = enemy_pos

    def apply_move(self, move, unit, direction):
        if move == "MOVE&BUILD":
            new_pos = tuple(a + b for (a, b) in zip(self.player_pos, direction))
            if self.is_legal(new_pos):
                self.grid[self.player_pos[0]][self.player_pos[1]] += 1
                self.player_pos = new_pos

    def is_legal(self, pos):
        # Actual validation to come
        return True
