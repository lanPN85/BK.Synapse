import numpy as np


class UpdatingMetric(object):
    def __init__(self):
        self.sum = 0
        self.n = 0

    def update(self, val):
        self.sum += val
        self.n += 1

    @property
    def avg(self):
        try:
            return self.sum / self.n
        except ZeroDivisionError:
            return np.nan
