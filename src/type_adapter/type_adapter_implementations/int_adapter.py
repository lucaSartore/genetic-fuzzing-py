from type_adapter.type_adapter import AdaptedType, TypeAdapter
from typing import Self
import random

MUTATION_DELTA_RANGE = [-2, -1, 0, 0, 0, 1, 2]

class IntAdapter(TypeAdapter[int]):

    @classmethod
    def initialize(cls, adapted_type: AdaptedType, initial_value: int | None = None) -> Self:
        assert adapted_type == int
        value = initial_value if initial_value is not None else 0
        return cls(value)

    def __init__(self, value: int) -> None:
        self.value = value

    def get_value(self) -> int:
        return self.value

    @classmethod
    def crossover(cls, a: IntAdapter, b: IntAdapter) -> IntAdapter: #type: ignore
        new = random.randint(a.value, b.value)
        return IntAdapter(new)


    def deep_copy(self) -> 'IntAdapter': #type: ignore
        return IntAdapter(self.value)

    def mutate(self) -> None:
        delta = random.choice(MUTATION_DELTA_RANGE)
        self.value += delta

    def deep_copy(self) -> IntAdapter: #type: ignore
        return IntAdapter(self.value)

    @classmethod
    def get_type(cls) -> type[int]:
        return int
