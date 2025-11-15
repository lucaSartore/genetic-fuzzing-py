from abc import ABC, abstractmethod
from annotationlib import get_annotate_from_class_namespace
from os import stat
from types import GenericAlias
from typing import Self, TypeAlias, TypeAliasType, Union, Any

AdaptedType = type | GenericAlias

class TypeAdapter[T](ABC):
    '''
    Type adapter is a class that allow to implement the necessary functionality
    that a type must have to be usable inside a genetic algorithm.

    for example implementing an adapter for the type `int` (aka implementing TypeAdapter[int])
    means defining the two basic operation of mutations and crossover on the basic type
    '''
    pass

    @classmethod
    @abstractmethod
    def initialize(cls, adapted_type: AdaptedType, initial_value: T | None = None) -> Self:
        '''
        create an instance of the current class.
        caller can optionally provide an initial value.
        '''
        pass

    @abstractmethod
    def get_value(self) -> T:
        '''
        return the original value obtained
        '''
        pass

    @classmethod
    @abstractmethod
    def crossover(cls, a: Self, b: Self) -> Self:
        '''
        define a crossover operation between two instances of the 
        following class
        '''
        pass

    @abstractmethod
    def mutate(self) -> None:
        '''
        mutate the current instance of the class
        '''
        pass

    @abstractmethod
    def deep_copy(self) -> Self:
        '''
        return a new deep copy of the current object.
        '''
        pass

    @classmethod
    @abstractmethod
    def get_type(cls) -> type[T]:
        '''
        return the type that the current adapter is generating
        '''
        pass
    
    @staticmethod
    def get_raw_time(adapted_type: AdaptedType) -> type:
        if type(adapted_type) == GenericAlias:
            inner_type = adapted_type.__origin__
            assert type(inner_type) == type, \
            'annotations must have concrete types in order to generate type adapter automatically'
            return inner_type
        assert isinstance(adapted_type, type)
        return adapted_type

    @staticmethod
    def parse_adapted_type(to_parse: Any) -> AdaptedType:
        if isinstance(to_parse, type):
            return to_parse
        if type(to_parse) == GenericAlias:
            return to_parse
        raise Exception(f'unable to parse type {to_parse}')

