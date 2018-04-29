class Game:
    WIDTH = 6
    HEIGHT = 12

    def __init__(self):
        self.block_queue = []
        self.grid = [[0] * self.HEIGHT for _ in range(self.WIDTH)]

    def drop_block(self, col, block):
        i = 0
        while i < len(self.grid[col]) and self.grid[col][i] == 0:
            i += 1

        if i > 1:
            self.grid[col][i - 1] = self.grid[col][i - 2] = block
            return True

        return False
    

if __name__ == '__main__':
    game = Game()
    for _ in range(5):
        game.drop_block(2, 5)
    print(*game.grid, sep="\n")
