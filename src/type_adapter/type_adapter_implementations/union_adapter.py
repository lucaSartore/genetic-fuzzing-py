from type_adapter.type_adapter import AdaptedType, TypeAdapter, Union
from typing import Any, Self
import random

class UnionAdapter(TypeAdapter[Union]):

    @classmethod
    def initialize(cls, adapted_type: AdaptedType, initial_value: Union[Any,Any] | None = None) -> Self:
        pass

    def get_value(self) -> Union[Any,Any]:
        pass

    @classmethod
    def crossover(cls, a: UnionAdapter, b: UnionAdapter) -> UnionAdapter: #type: ignore
        pass

    def mutate(self) -> None:
        pass


    def deep_copy(self) -> UnionAdapter: #type: ignore
        pass

    @classmethod
    def get_type(cls) -> type[Union[Any, Any]]:
        return Union #type: ignore
