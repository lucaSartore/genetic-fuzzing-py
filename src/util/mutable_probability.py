import numpy as np
from random import Random


class MutableProbability:
    def __init__(self, initial_probability: float, std: float):
        self.v = initial_probability
        self.std = std

    def mutate(self, random: Random):
        self.v += random.gauss(0,self.std)
        self.v = np.clip(self.v, 0, 1)

    @staticmethod
    def crossover(random: Random, a: MutableProbability, b: MutableProbability):
        v_min = min(a.v, b.v)
        v_max = max(a.v, b.v)

        std_min = min(a.std, b.std)
        std_max = max(a.std, b.std)

        v = random.random() * (v_max - v_min) + v_min
        std = random.random() * (std_max - std_min) + std_min

        return MutableProbability(v, std)

    def event(self, random: Random) -> bool:
        return random.random() < self.v


