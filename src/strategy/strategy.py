from typing import Self, Literal
from dataset.functions_list import FunctionType
from abc import ABC, abstractmethod

StrategyEnum = Literal["random", "input_bag", "novelty_search"]

class Strategy[TSettings](ABC):
    @classmethod
    @abstractmethod
    def initialize(cls, function: FunctionType, settings: TSettings | None = None) -> Self:
        pass

    @abstractmethod
    def run(self) -> list[tuple]:
        pass

