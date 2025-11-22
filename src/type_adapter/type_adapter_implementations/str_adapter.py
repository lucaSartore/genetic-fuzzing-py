from type_adapter.type_adapter import AdaptedType, TypeAdapter
from typing import Self

class StrAdapter(TypeAdapter[str]):

    @classmethod
    def initialize(cls, random, adapted_type: AdaptedType, initial_value: str | None = None) -> Self:
        pass

    def get_value(self) -> str:
        pass

    @classmethod
    def crossover(cls, random, a: StrAdapter, b: StrAdapter) -> StrAdapter: #type: ignore
        pass

    def mutate(self, random) -> None:
        pass


    def deep_copy(self) -> StrAdapter: #type: ignore
        pass

    @classmethod
    def get_type(cls) -> type[str]:
        return str
