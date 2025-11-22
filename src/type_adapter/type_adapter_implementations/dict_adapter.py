from type_adapter.type_adapter import AdaptedType, TypeAdapter
from typing import Self, TypeVar

class DictAdapter(TypeAdapter[dict]):

    @classmethod
    def initialize(cls, random, adapted_type: AdaptedType, initial_value: dict | None = None) -> Self:
        pass

    def get_value(self) -> dict:
        pass

    @classmethod
    def crossover(cls, random, a: DictAdapter, b: DictAdapter) -> DictAdapter: #type: ignore
        pass

    def mutate(self, random) -> None:
        pass


    def deep_copy(self) -> DictAdapter: #type: ignore
        pass

    @classmethod
    def get_type(cls) -> type[dict]:
        return dict
