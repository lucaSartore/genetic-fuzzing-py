from type_adapter.type_adapter import AdaptedType, TypeAdapter
from typing import Self

class BoolAdapter(TypeAdapter[bool]):

    @classmethod
    def initialize(cls, random, adapted_type: AdaptedType, initial_value: bool | None = None) -> Self:
        assert adapted_type == bool
        value = initial_value or random.choice[True, False]
        return cls(value)

    def __init__(self, value: bool) -> None:
        self.value = value

    def get_value(self) -> bool:
        return self.value

    @classmethod
    def crossover(cls, random, a: BoolAdapter, b: BoolAdapter) -> BoolAdapter: #type: ignore
        if random.randint(0,1) == 0:
            return a.deep_copy();
        else:
            return b.deep_copy();

    def mutate(self, random) -> None:
        if random.randint(0,1) == 0:
            self.value = not self.value


    def deep_copy(self) -> BoolAdapter: #type: ignore
        return BoolAdapter(self.value)

    @classmethod
    def get_type(cls) -> type[bool]:
        return bool
