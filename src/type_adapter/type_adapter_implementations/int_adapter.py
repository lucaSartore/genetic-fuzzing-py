from type_adapter.type_adapter import AdaptedType, TypeAdapter
from typing import Self
import numpy as np



I_VALUE = 0
I_MUT_STD = 1
I_RESET_PROB = 2
I_RESET_LOWER_BOUND = 3
I_RESET_UPPER_BOUND = 4

INITIAL_LOWER_BOUND = -5
INITIAL_UPPER_BOUND = 100
INITIAL_MUT_STD = 5
INITIAL_RESET_PROB = 0.5

MUT_STD_MUTATION_RATE = 1
RESET_PROB_MUTATION_RATE = 0.05


class IntAdapter(TypeAdapter[int]):

    @classmethod
    def initialize(cls, random, adapted_type: AdaptedType, initial_value: int | None = None) -> Self:
        assert adapted_type == int

        value = np.zeros(shape=(5,), dtype=np.float64)
        value[I_VALUE] = initial_value if initial_value != None else random.randint(INITIAL_LOWER_BOUND, INITIAL_UPPER_BOUND)
        value[I_MUT_STD] = INITIAL_MUT_STD
        value[I_RESET_PROB] = INITIAL_RESET_PROB
        value[I_RESET_LOWER_BOUND] = INITIAL_LOWER_BOUND
        value[I_RESET_UPPER_BOUND] = INITIAL_UPPER_BOUND
        return cls(value)

    def __init__(self, value: np.ndarray) -> None:
        self.value: np.ndarray = value

    def get_value(self) -> int:
        return int(self.value[I_VALUE])

    @classmethod
    def crossover(cls, random, a: IntAdapter, b: IntAdapter) -> IntAdapter: #type: ignore
        # element-wise lower and upper bounds
        lo = np.minimum(a.value, b.value)
        hi = np.maximum(a.value, b.value)
        
        rng = np.random.default_rng(seed=random.randint(0,1_000_000))
        # generate random values uniformly within each pair
        r = lo + (hi - lo) * rng.random(a.value.shape)
        return IntAdapter(r)


    def deep_copy(self) -> 'IntAdapter': #type: ignore
        return IntAdapter(self.value)

    def mutate(self, random) -> None:
        # mutating the various probability
        reset_prob = self.value[I_RESET_PROB]
        reset_prob += random.gauss(0,RESET_PROB_MUTATION_RATE)
        reset_prob = np.clip(reset_prob, 0,1)
        self.value[I_RESET_PROB] = reset_prob;
        
        std = self.value[I_MUT_STD]
        std += random.gauss(0,MUT_STD_MUTATION_RATE)
        std = np.clip(std, 0,1)
        self.value[I_MUT_STD] = std;

        # reset resetting
        if random.random() < self.value[I_RESET_PROB]:
            self.value [I_MUT_STD] = random.randint(
                int(self.value[I_RESET_LOWER_BOUND]),
                int(self.value[I_RESET_UPPER_BOUND])
            )
        # regular mutation
        else:
            std = self.value[I_MUT_STD]
            self.value[I_VALUE] += random.gauss(0,std)
            self.value[I_RESET_LOWER_BOUND] += random.gauss(0,std)
            self.value[I_RESET_UPPER_BOUND] += random.gauss(0,std)


    def deep_copy(self) -> IntAdapter: #type: ignore
        return IntAdapter(np.array(self.value, copy=True))

    @classmethod
    def get_type(cls) -> type[int]:
        return int
