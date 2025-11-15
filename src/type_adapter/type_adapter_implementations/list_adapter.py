from types import GenericAlias
from typing import Self, TYPE_CHECKING
from type_adapter.type_adapter import AdaptedType, TypeAdapter
from type_adapter.type_adapter_collection import TypeAdapterCollection

class ListAdapter(TypeAdapter[list]):
    '''
    Type adapter is a class that allow to implement the necessary functionality
    that a type must have to be usable inside a genetic algorithm.

    for example implementing an adapter for the type `int` (aka implementing TypeAdapter[int])
    means defining the two basic operation of mutations and crossover on the basic type
    '''

    @classmethod
    def initialize(cls,adapted_type: AdaptedType, initial_value: list | None = None) -> Self:
        assert isinstance(adapted_type, GenericAlias)
        assert adapted_type.__origin__ == list
        assert len(adapted_type.__args__) == 1
        inner_type = cls.parse_adapted_type(adapted_type.__args__[0])
        """
        generic type of the list
        """

        value: list[TypeAdapter] = []
        if initial_value != None:
            adapter = TypeAdapterCollection.get_adapter_static(
                cls.get_raw_time(inner_type)
            )
            value = [
                adapter.initialize(inner_type, x)
                for x in initial_value
            ]
        return cls(inner_type, value)
    
    def __init__(self, inner_type: AdaptedType, value: list) -> None:
        self.inner_type = inner_type
        self.value = value

    def get_value(self) -> list:
        return [
            x.get_value()
            for x in self.value
        ]

    @classmethod
    def crossover(cls, a: Self, b: Self) -> Self: #type: ignore
        # todo: implement real crossover strategy
        return a.deep_copy()

    def mutate(self) -> None:
        # todo:  implement strategies to mutate list length
        for x in self.value:
            x.mutate()
        return


    def deep_copy(self) -> Self:
        return self.__class__(
            self.inner_type,
            [x.deep_copy() for x in self.value]
        )

    @classmethod
    def get_type(cls) -> type[list]:
        return list
