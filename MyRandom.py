import numpy


class Randrange:
    def __init__(self, high):
        self.high = high

        self.gen_rands()

    def next(self):
        if self.r_ind == self.new_ind:
            self.gen_rands()

        self.r_ind += 1
        return self.r[self.r_ind - 1]

    def gen_rands(self):
        self.r = numpy.random.randint(self.high, size=10 ** 6)

        self.r_ind = 0
        self.new_ind = 10 ** 6
