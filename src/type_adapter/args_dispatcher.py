from typing import Any, Callable, ParamSpec, TypeVar, Self
from type_adapter.type_adapter import TypeAdapter
from type_adapter.type_adapter_collection import TypeAdapterCollection


TReturn = TypeVar('TReturn')
TParam = ParamSpec('TParam')
class ArgsDispatcher[**TParam, TReturn]:
    """
    ArgsDispatcher is a class that using a list of type adapters
    select the best matching type adapters for a function's args
    and then proceed to implement useful method for function
    """

    @classmethod
    def initialize(
        cls, random, fn: Callable[TParam, TReturn], initial_guesses: dict[str, Any] | None = None
    ) -> Self:
        if initial_guesses is None:
            initial_guesses = {}
        annotations = fn.__annotations__
        annotations.pop('return', None) # don't care about the return value
        args: list[TypeAdapter] = []

        for arg_name, arg_type in annotations.items():
            adapted_type = TypeAdapter.parse_adapted_type(arg_type)
            raw_type = TypeAdapter.get_raw_time(adapted_type)
            adapter = TypeAdapterCollection.get_adapter_static(raw_type)
            initial_guess = initial_guesses.pop(arg_name, None)
            args.append(
                adapter.initialize(random, adapted_type, initial_guess)
            )
        return cls(args)

    def __init__(self, args: list[TypeAdapter]) -> None:
        self.args = args

    def get_args(self) -> tuple:
        """
        return a set of args that is compatible with the
        function we are trying explore
        """
        return tuple(x.get_value() for x in self.args)

    def mutate(self, random) -> None:
        for arg in self.args:
            arg.mutate(random)

    @classmethod
    def crossover(cls, random, a: Self, b: Self) -> Self:
        new_list = list[TypeAdapter]()
        for ia, ib in zip(a.args, b.args):
            adapter = ia.__class__
            new_list.append(adapter.crossover(random ,ia, ib))
        return cls(new_list)

