from type_adapter.type_adapter import AdaptedType, TypeAdapter
from typing import Self

class FloatAdapter(TypeAdapter[float]):

    @classmethod
    def initialize(cls, random adapted_type: AdaptedType, initial_value: float | None = None) -> Self:
        pass

    def get_value(self) -> float:
        pass

    @classmethod
    def crossover(cls, random, a: FloatAdapter, b: FloatAdapter) -> FloatAdapter: #type: ignore
        pass

    def mutate(self, random) -> None:
        pass


    def deep_copy(self) -> FloatAdapter: #type: ignore
        pass

    @classmethod
    def get_type(cls) -> type[dict]:
        return dict
