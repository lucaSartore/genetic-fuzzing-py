from abc import ABC, abstractmethod
from typing import Self

class TypeAdapter[T](ABC):
    '''
    Type adapter is a class that allow to implement the necessary functionality
    that a type must have to be usable inside a genetic algorithm.

    for example implementing an adapter for the type `int` (aka implementing TypeAdapter[int])
    means defining the two basic operation of mutations and crossover on the basic type
    '''
    pass

    @abstractmethod
    def __init__(self, initial_value: T | None = None) -> None:
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
    def mutations(self) -> None:
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
    def adapter_importance(cls) -> int:
        '''
        define the importance of the current adapter.
        When multiple adapters are available for the same type, the adapter
        that has the higher importance will be used
        '''
        return 1

    @classmethod
    def parameter_matching(cls) -> str:
        '''
        return a regex that indicate whether the current adapter
        can be used for a specific function argument.
        this is to have specialized type adapters for specific arguments to a function
        '''
        return ".+"
